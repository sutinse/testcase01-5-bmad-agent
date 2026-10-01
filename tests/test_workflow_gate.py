import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import workflow_gate as gate


class WorkflowGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.root_patch = patch.object(gate, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.path = "bmad-output/sample/prd.md"
        self.source_path = "bmad-output/sample/input/rovo-feature.md"
        target = self.root / self.path
        target.parent.mkdir(parents=True)
        target.write_bytes(b"Approved PRD\r\n")
        source = self.root / "bmad-output/sample/input/rovo-feature.md"
        source.parent.mkdir()
        source.write_text("Source URL: https://example.com/feature\nRetrieved: 2026-01-01T00:00:00Z\n")
        rubric = self.root / "docs/qg1/feature-readiness.md"
        rubric.parent.mkdir(parents=True)
        rubric.write_text("QG1 rubric")
        self.pr = {"merged_at": "2026-01-01T12:00:00Z", "merge_commit_sha": "merge",
                   "head": {"sha": "head"}, "base": {"ref": "main"},
                   "user": {"login": "author"}}
        self.reviews = [{"state": "APPROVED", "commit_id": "head",
                         "submitted_at": "2026-01-01T11:00:00Z",
                         "user": {"login": "reviewer", "type": "User"}}]
        self.policy = {"required_pull_request_reviews": {"dismiss_stale_reviews": True,
                          "required_approving_review_count": 1},
                       "required_status_checks": {"contexts": ["workflow-gate"]}}

    def github(self, endpoint):
        if endpoint.endswith("/pulls/7"):
            return self.pr
        if "/reviews?" in endpoint:
            return self.reviews
        if endpoint.endswith("/protection"):
            return self.policy
        if "/files?" in endpoint:
            return [{"filename": self.path}, {"filename": self.source_path}]
        if "/contents/" in endpoint:
            content = (self.root / self.source_path).read_bytes() if self.source_path in endpoint else b"Approved PRD\r\n"
            return {"encoding": "base64", "content": base64.b64encode(content).decode()}
        raise AssertionError(endpoint)

    def record(self):
        with patch.object(gate, "github", side_effect=self.github):
            return gate.record_approval("sample", "prd", 7, [self.path, self.source_path], "org/repo")

    def check_architecture(self):
        with patch.object(gate, "github", side_effect=self.github):
            gate.check("sample", "architecture", "org/repo")

    def test_missing_gate_blocks(self):
        with self.assertRaisesRegex(gate.GateError, "WAITING_FOR_PRD_APPROVAL"):
            self.check_architecture()

    def test_missing_source_blocks_prd(self):
        (self.root / "docs/qg1/feature-readiness.md").unlink()
        with self.assertRaisesRegex(gate.GateError, "WAITING_FOR_ROVO_SNAPSHOT_AND_QG1_RUBRIC"):
            gate.check("sample", "prd", "org/repo")

    def test_human_approved_merge_unlocks_next_stage(self):
        self.record()
        self.check_architecture()
        self.assertEqual(self.record(), "Already recorded")
        self.assertEqual(len(list((self.root / ".bmad/features/sample/events").glob("*.yaml"))), 1)

    def test_draft_or_unmerged_pr_blocks(self):
        for change in ({"merged_at": None}, {"merge_commit_sha": None}):
            with self.subTest(change=change):
                self.pr.update(change)
                with self.assertRaises(gate.GateError):
                    self.record()
                self.pr.update(merged_at="2026-01-01T12:00:00Z", merge_commit_sha="merge")

    def test_author_bot_old_head_and_revoked_review_block(self):
        for user, sha, state in (("author", "head", "APPROVED"), ("bot", "head", "APPROVED"),
                                 ("reviewer", "old", "APPROVED"), ("reviewer", "head", "CHANGES_REQUESTED")):
            with self.subTest(user=user, sha=sha, state=state):
                self.reviews[0]["user"] = {"login": user, "type": "Bot" if user == "bot" else "User"}
                self.reviews[0]["commit_id"] = sha
                self.reviews[0]["state"] = state
                with self.assertRaisesRegex(gate.GateError, "WAITING_FOR_HUMAN_APPROVAL"):
                    self.record()

    def test_changed_artifact_and_approval_revocation_block(self):
        self.record()
        (self.root / self.path).write_bytes(b"Changed\n")
        with self.assertRaisesRegex(gate.GateError, "Approved artifact changed"):
            self.check_architecture()
        (self.root / self.path).write_bytes(b"Approved PRD\r\n")
        self.reviews.append({"state": "DISMISSED", "commit_id": "head",
                             "submitted_at": "2026-01-02T11:00:00Z",
                             "user": {"login": "reviewer", "type": "User"}})
        with self.assertRaisesRegex(gate.GateError, "No human approval"):
            self.check_architecture()

    def test_missing_policy_or_unlisted_artifact_blocks(self):
        self.policy["required_pull_request_reviews"]["dismiss_stale_reviews"] = False
        with self.assertRaisesRegex(gate.GateError, "stale approvals"):
            self.record()
        self.policy["required_pull_request_reviews"]["dismiss_stale_reviews"] = True
        with self.assertRaisesRegex(gate.GateError, "Provide distinct"):
            with patch.object(gate, "github", side_effect=self.github):
                gate.record_approval("sample", "prd", 7, [], "org/repo")

    def test_ci_verification_does_not_need_branch_protection_api(self):
        self.record()

        def ci_github(endpoint):
            if endpoint.endswith("/protection"):
                raise gate.GateError("Resource not accessible by integration")
            return self.github(endpoint)

        with patch.object(gate, "github", side_effect=ci_github):
            with self.assertRaisesRegex(gate.GateError, "Resource not accessible"):
                gate.validate_history("sample", "org/repo")
            gate.validate_history("sample", "org/repo", require_protection=False)
            self.reviews[0]["state"] = "DISMISSED"
            with self.assertRaisesRegex(gate.GateError, "No human approval"):
                gate.validate_history("sample", "org/repo", require_protection=False)

    def test_merged_bytes_must_match(self):
        self.record()
        original = self.github

        def changed_merge(endpoint):
            if "/contents/" in endpoint:
                return {"encoding": "base64", "content": base64.b64encode(b"other").decode()}
            return original(endpoint)

        with patch.object(gate, "github", side_effect=changed_merge):
            with self.assertRaisesRegex(gate.GateError, "Merge commit"):
                gate.check("sample", "architecture", "org/repo")

    def test_prd_hash_is_raw_bytes(self):
        self.record()
        record = gate.events("sample")[0]
        self.assertEqual(record["artifacts"][self.path], hashlib.sha256(b"Approved PRD\r\n").hexdigest())

    def test_development_requires_entire_planning_chain(self):
        with self.assertRaisesRegex(gate.GateError, "WAITING_FOR_PRD_APPROVAL"):
            with patch.object(gate, "github", side_effect=self.github):
                gate.check("sample", "development", "org/repo")
        self.record()
        with self.assertRaisesRegex(gate.GateError, "WAITING_FOR_ARCHITECTURE_APPROVAL"):
            with patch.object(gate, "github", side_effect=self.github):
                gate.check("sample", "development", "org/repo")

    def test_changes_requested_invalidates_active_approval(self):
        self.record()
        self.reviews.append({"state": "CHANGES_REQUESTED", "commit_id": "head",
                             "submitted_at": "2026-01-02T11:00:00Z",
                             "user": {"login": "reviewer", "type": "User"}})
        with patch.object(gate, "github", side_effect=self.github):
            gate.request_changes("sample", "prd", 7, "org/repo")
        with self.assertRaisesRegex(gate.GateError, "WAITING_FOR_PRD_APPROVAL"):
            self.check_architecture()
        self.assertEqual(len(gate.events("sample")), 2)

    def test_request_changes_without_human_review_blocks(self):
        self.record()
        with patch.object(gate, "github", side_effect=self.github):
            with self.assertRaisesRegex(gate.GateError, "No human changes-requested"):
                gate.request_changes("sample", "prd", 7, "org/repo")

    def test_event_modified_or_deleted_blocks_snapshot(self):
        for mutation in ("modify", "delete"):
            with self.subTest(mutation=mutation):
                feature = self.root / ".bmad/features/sample"
                if feature.exists():
                    for path in (feature / "events").glob("*.yaml"):
                        path.unlink()
                    (feature / "workflow.yaml").unlink()
                self.record()
                event = next((feature / "events").glob("*.yaml"))
                if mutation == "modify":
                    event.write_text(event.read_text() + "\n# changed\n")
                else:
                    event.unlink()
                with self.assertRaisesRegex(gate.GateError, "snapshot"):
                    self.check_architecture()

    def test_incomplete_github_page_blocks(self):
        with patch.object(gate, "github", return_value=[{}] * 100):
            with self.assertRaisesRegex(gate.GateError, "pagination"):
                gate.page("repos/org/repo/pulls/7/reviews?per_page=100")

    def test_planning_manifest_rejects_empty_scope_and_parallel_overlap(self):
        base = self.root / "bmad-output/sample"
        for name in ("epics.md", "sprint-status.yaml", "1.1.first.story.md", "1.2.second.story.md"):
            (base / name).write_text(name)
        manifest = base / "handoff-manifest.json"
        first = {"id": "1.1.first", "storyFilePath": "bmad-output/sample/1.1.first.story.md",
                 "status": "ready-for-dev", "ownedScope": ["app/src/main"], "wave": 1, "dependencies": []}
        second = {"id": "1.2.second", "storyFilePath": "bmad-output/sample/1.2.second.story.md",
                  "status": "ready-for-dev", "ownedScope": ["app/src/test"], "wave": 1, "dependencies": []}
        data = {"schemaVersion": "1.0", "stories": [first, second]}
        manifest.write_text(json.dumps(data))
        paths = gate.required_artifacts("sample", "planning")
        gate.validate_paths("sample", "planning", paths)
        second["ownedScope"] = []
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(gate.GateError, "nonempty ownedScope"):
            gate.validate_paths("sample", "planning", paths)
        second["ownedScope"] = ["app/src/main/service"]
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(gate.GateError, "share ownedScope"):
            gate.validate_paths("sample", "planning", paths)
        second["wave"] = 2
        second["dependencies"] = ["1.1.first"]
        manifest.write_text(json.dumps(data))
        gate.validate_paths("sample", "planning", paths)

    def test_application_change_without_approved_feature_blocks(self):
        with patch.object(gate, "run", return_value="app/src/main/Refund.java"):
            with self.assertRaisesRegex(gate.GateError, "no approved planning feature"):
                gate.validate_code_changes("origin/main", "org/repo")

    def test_application_change_matches_approved_glob_but_not_other_files(self):
        feature = self.root / ".bmad/features/sample"
        feature.mkdir(parents=True)
        manifest = self.root / "bmad-output/sample/handoff-manifest.json"
        manifest.write_text(json.dumps({"stories": [{"ownedScope": [
            "app/src/main/java/**/refundapproval/security/ValidatedClaimsGuard.java"
        ]}]}))
        with (patch.object(gate, "approvals", return_value={"planning": True}),
              patch.object(gate, "check"),
              patch.object(gate, "run", return_value=
                           "app/src/main/java/io/github/sutinse/refundapproval/security/ValidatedClaimsGuard.java")):
            gate.validate_code_changes("origin/main", "org/repo")
        with (patch.object(gate, "approvals", return_value={"planning": True}),
              patch.object(gate, "check"),
              patch.object(gate, "run", return_value=
                           "app/src/main/java/io/github/sutinse/refundapproval/security/Unreviewed.java")):
            with self.assertRaisesRegex(gate.GateError, "outside approved ready story scope"):
                gate.validate_code_changes("origin/main", "org/repo")
        manifest.write_text(json.dumps({"stories": [{"ownedScope": [
            "app/src/main/java/*/refundapproval/security/ValidatedClaimsGuard.java"
        ]}]}))
        with (patch.object(gate, "approvals", return_value={"planning": True}),
              patch.object(gate, "check"),
              patch.object(gate, "run", return_value=
                           "app/src/main/java/io/github/sutinse/refundapproval/security/ValidatedClaimsGuard.java")):
            with self.assertRaisesRegex(gate.GateError, "outside approved ready story scope"):
                gate.validate_code_changes("origin/main", "org/repo")


if __name__ == "__main__":
    unittest.main()