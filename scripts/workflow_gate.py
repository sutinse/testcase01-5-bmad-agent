"""Fail-closed, GitHub-backed approval for BMAD stage artifacts."""

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STAGES = ("prd", "architecture", "planning")
CHECKPOINTS = STAGES + ("development", "review")
PREVIOUS = {"prd": None, "architecture": "prd", "planning": "architecture",
            "development": "planning", "review": "planning"}


class GateError(Exception):
    pass


def run(*args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode:
        raise GateError(f"Command failed: {args[0]} {' '.join(args[1:3])}: {result.stderr.strip()}")
    return result.stdout.strip()


def github(endpoint):
    return json.loads(run("gh", "api", endpoint))


def page(endpoint):
    result = github(endpoint)
    if not isinstance(result, list) or len(result) >= 100:
        raise GateError("GitHub result pagination required; refusing incomplete evidence")
    return result


def feature_dir(feature):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", feature):
        raise GateError("Invalid feature identifier")
    return ROOT / ".bmad" / "features" / feature


def required_artifacts(feature, stage):
    base = Path("bmad-output") / feature
    if stage == "prd":
        return {(base / "prd.md").as_posix(), (base / "input" / "rovo-feature.md").as_posix()}
    if stage == "architecture":
        return {(base / "architecture.md").as_posix()}
    stories = {path.relative_to(ROOT).as_posix() for path in (ROOT / base).rglob("*.story.md")}
    if not stories:
        raise GateError("Planning package contains no stories")
    return stories | {(base / name).as_posix() for name in
                      ("epics.md", "sprint-status.yaml", "handoff-manifest.json")}


def artifact(path):
    relative = Path(path)
    if not relative.parts or relative.is_absolute() or ".." in relative.parts or relative.parts[0] != "bmad-output":
        raise GateError(f"Invalid artifact path: {path}")
    actual = (ROOT / relative).resolve()
    if not actual.is_relative_to(ROOT.resolve()) or not actual.is_file():
        raise GateError(f"Missing artifact: {path}")
    return hashlib.sha256(actual.read_bytes()).hexdigest()


def validate_paths(feature, stage, paths):
    expected = required_artifacts(feature, stage)
    if set(paths) != expected or len(paths) != len(expected):
        raise GateError(f"{stage} requires exactly these artifacts: {', '.join(sorted(expected))}")
    if stage == "planning":
        validate_manifest(feature, expected)


def validate_manifest(feature, expected):
    path = ROOT / "bmad-output" / feature / "handoff-manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    stories = manifest.get("stories")
    if manifest.get("schemaVersion") != "1.0" or not isinstance(stories, list) or not stories:
        raise GateError("Handoff manifest must contain ready-for-dev stories with schemaVersion 1.0")
    by_id = {}
    for story in stories:
        story_id = story.get("id")
        story_path = story.get("storyFilePath")
        scope = story.get("ownedScope")
        wave = story.get("wave")
        if not story_id or story_id in by_id or story_path not in expected or not story_path.endswith(".story.md"):
            raise GateError("Handoff story id or path is invalid or duplicated")
        if story.get("status") != "ready-for-dev" or not isinstance(scope, list) or not scope:
            raise GateError(f"Story {story_id} must be ready-for-dev with nonempty ownedScope")
        if not isinstance(wave, int) or isinstance(wave, bool) or wave < 1:
            raise GateError(f"Story {story_id} has invalid wave")
        for owned in scope:
            if not isinstance(owned, str) or not owned.startswith("app/") or ".." in Path(owned).parts:
                raise GateError(f"Story {story_id} owns a path outside app/")
        by_id[story_id] = story
    for story in stories:
        dependencies = story.get("dependencies")
        if not isinstance(dependencies, list) or any(
                dep not in by_id or by_id[dep]["wave"] >= story["wave"] for dep in dependencies):
            raise GateError(f"Story {story['id']} has unresolved or same-wave dependencies")
    for index, first in enumerate(stories):
        for second in stories[index + 1:]:
            if first["wave"] == second["wave"] and any(
                    left.rstrip("/") == right.rstrip("/") or
                    left.rstrip("/").startswith(right.rstrip("/") + "/") or
                    right.rstrip("/").startswith(left.rstrip("/") + "/")
                    for left in first["ownedScope"] for right in second["ownedScope"]):
                raise GateError(f"Parallel stories {first['id']} and {second['id']} share ownedScope")


def events(feature):
    directory = feature_dir(feature) / "events"
    records = []
    for path in sorted(directory.glob("*.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or record.get("feature") != feature:
            raise GateError(f"Invalid event: {path}")
        records.append(record)
    if directory.is_dir() and any(path.suffix != ".yaml" for path in directory.iterdir()):
        raise GateError("Unexpected file in event directory")
    return records


def snapshot(feature):
    directory = feature_dir(feature)
    event_dir = directory / "events"
    return {"schemaVersion": 1, "feature": feature,
            "events": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in sorted(event_dir.glob("*.yaml"))},
            "stages": {stage: "approved" if approvals(feature).get(stage) else "pending"
                       for stage in STAGES}}


def verify_snapshot(feature):
    expected = snapshot(feature)
    path = feature_dir(feature) / "workflow.yaml"
    if not path.is_file():
        if expected["events"]:
            raise GateError("Missing workflow snapshot")
        return
    if yaml.safe_load(path.read_text(encoding="utf-8")) != expected:
        raise GateError("Workflow snapshot does not match event history")


def approved_review(pr, reviews):
    latest = {}
    for review in reviews:
        user = review.get("user", {})
        if user.get("login") and review.get("submitted_at"):
            latest[user["login"]] = review
    return next((review for review in latest.values()
                 if review["state"] == "APPROVED" and review.get("commit_id") == pr["head"]["sha"]
                 and review["user"].get("type") == "User"
                 and review["user"]["login"] != pr["user"]["login"]), None)


def protection(pr, repo):
    branch = pr["base"]["ref"]
    policy = github(f"repos/{repo}/branches/{branch}/protection")
    reviews = policy.get("required_pull_request_reviews") or {}
    if not reviews.get("dismiss_stale_reviews") or reviews.get("required_approving_review_count", 0) < 1:
        raise GateError("Base branch needs required reviews with stale approvals dismissed")
    if not (policy.get("required_status_checks") or {}).get("contexts"):
        raise GateError("Base branch needs required status checks")


def merged_content(repo, path, sha):
    response = github(f"repos/{repo}/contents/{path}?ref={sha}")
    if response.get("encoding") != "base64":
        raise GateError(f"Cannot verify merge content: {path}")
    return base64.b64decode(response["content"])


def approvals(feature):
    state = {}
    for record in events(feature):
        stage = record.get("stage")
        action = record.get("action")
        if stage not in STAGES or action not in ("approved", "changes_requested"):
            raise GateError("Unknown stage or event action")
        if action == "approved":
            if state.get(stage):
                raise GateError(f"Duplicate stage approval: {stage}")
            state[stage] = record
        else:
            if not state.get(stage):
                raise GateError(f"No approval to invalidate for {stage}")
            state[stage] = None
    return state


def verify_event(record, repo, active=True):
    if record["action"] == "changes_requested":
        pr = github(f"repos/{repo}/pulls/{record['pr']}")
        reviews = page(f"repos/{repo}/pulls/{record['pr']}/reviews?per_page=100")
        if not any(
                review.get("state") == "CHANGES_REQUESTED" and review.get("commit_id") == record["headSha"]
                and review.get("submitted_at") == record["reviewedAt"]
                and review.get("user", {}).get("login") == record["reviewer"]
                and review.get("user", {}).get("type") == "User"
                and record["reviewer"] != pr["user"]["login"] for review in reviews):
            raise GateError("No GitHub changes-requested review matching event")
        return
    if active:
        validate_paths(record["feature"], record["stage"], record["artifacts"])
    if record["stage"] == "prd" and active:
        rubric = ROOT / "docs/qg1/feature-readiness.md"
        if not rubric.is_file() or hashlib.sha256(rubric.read_bytes()).hexdigest() != record.get("rubricHash"):
            raise GateError("Approved QG1 rubric changed or is missing")
    pr = github(f"repos/{repo}/pulls/{record['pr']}")
    if pr.get("merged_at") is None or pr.get("merge_commit_sha") != record["mergeSha"]:
        raise GateError("Approval PR is not merged at recorded commit")
    if pr["head"]["sha"] != record["headSha"] or pr["user"]["login"] == record["reviewer"]:
        raise GateError("PR head changed or author approved own work")
    protection(pr, repo)
    reviews = page(f"repos/{repo}/pulls/{record['pr']}/reviews?per_page=100")
    review = approved_review(pr, reviews) if active else next((item for item in reviews
        if item.get("state") == "APPROVED" and item.get("commit_id") == record["headSha"]
        and item.get("submitted_at") == record["approvedAt"]
        and item.get("user", {}).get("login") == record["reviewer"]), None)
    if not review or review["user"]["login"] != record["reviewer"] or review["submitted_at"] != record["approvedAt"]:
        raise GateError("No human approval for exact PR head")
    changed = {item["filename"] for item in page(f"repos/{repo}/pulls/{record['pr']}/files?per_page=100")}
    for path, digest in record["artifacts"].items():
        if path not in changed:
            raise GateError(f"Artifact not in approved PR: {path}")
        if active and artifact(path) != digest:
            raise GateError(f"Approved artifact changed: {path}")
        if hashlib.sha256(merged_content(repo, path, record["mergeSha"])).hexdigest() != digest:
            raise GateError(f"Merge commit does not contain approved artifact: {path}")


def check(feature, stage, repo):
    if stage == "prd":
        source = ROOT / "bmad-output" / feature / "input" / "rovo-feature.md"
        rubric = ROOT / "docs" / "qg1" / "feature-readiness.md"
        if not source.is_file() or not rubric.is_file():
            raise GateError("WAITING_FOR_ROVO_SNAPSHOT_AND_QG1_RUBRIC")
    verify_snapshot(feature)
    current = approvals(feature)
    for record in events(feature):
        verify_event(record, repo, active=record == current.get(record["stage"]))
    preceding_stages = STAGES[:STAGES.index(stage)] if stage in STAGES else STAGES
    for preceding in preceding_stages:
        record = current.get(preceding)
        if not record:
            raise GateError(f"WAITING_FOR_{preceding.upper()}_APPROVAL")


def record_approval(feature, stage, pr_number, paths, repo):
    check(feature, stage, repo)
    current = approvals(feature)
    if current.get(stage):
        verify_event(current[stage], repo)
        if current[stage]["pr"] == pr_number:
            return "Already recorded"
        raise GateError("Stage already approved; request changes before reapproval")
    if not paths or len(paths) != len(set(paths)):
        raise GateError("Provide distinct artifact paths")
    validate_paths(feature, stage, paths)
    pr = github(f"repos/{repo}/pulls/{pr_number}")
    if pr.get("merged_at") is None or not pr.get("merge_commit_sha"):
        raise GateError("Approval PR must be merged")
    protection(pr, repo)
    reviews = page(f"repos/{repo}/pulls/{pr_number}/reviews?per_page=100")
    reviewer = approved_review(pr, reviews)
    if not reviewer:
        raise GateError("WAITING_FOR_HUMAN_APPROVAL on current PR head")
    hashes = {path: artifact(path) for path in sorted(paths)}
    record = {"schemaVersion": 1, "feature": feature, "stage": stage, "action": "approved",
              "pr": pr_number, "headSha": pr["head"]["sha"], "mergeSha": pr["merge_commit_sha"],
              "reviewer": reviewer["user"]["login"], "approvedAt": reviewer["submitted_at"],
              "artifacts": hashes}
    if stage == "prd":
        rubric = ROOT / "docs/qg1/feature-readiness.md"
        if not rubric.is_file():
            raise GateError("Missing authentic QG1 rubric")
        record["rubricHash"] = hashlib.sha256(rubric.read_bytes()).hexdigest()
    verify_event(record, repo)
    write_event(feature, record)
    return f"Recorded {stage} approval from PR #{pr_number}"


def request_changes(feature, stage, pr_number, repo):
    verify_snapshot(feature)
    current = approvals(feature)
    if not current.get(stage):
        raise GateError(f"No active {stage} approval to invalidate")
    pr = github(f"repos/{repo}/pulls/{pr_number}")
    reviews = page(f"repos/{repo}/pulls/{pr_number}/reviews?per_page=100")
    review = next((item for item in reversed(reviews)
                   if item.get("state") == "CHANGES_REQUESTED" and item.get("commit_id") == pr["head"]["sha"]
                   and item.get("user", {}).get("type") == "User"
                   and item["user"]["login"] != pr["user"]["login"]), None)
    if not review:
        raise GateError("No human changes-requested review on current PR head")
    write_event(feature, {"schemaVersion": 1, "feature": feature, "stage": stage,
                          "action": "changes_requested", "pr": pr_number,
                          "headSha": pr["head"]["sha"], "reviewer": review["user"]["login"],
                          "reviewedAt": review["submitted_at"]})
    return f"Invalidated {stage} approval via PR #{pr_number}"


def write_event(feature, record):
    directory = feature_dir(feature) / "events"
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = directory / f"{timestamp}-{uuid.uuid4().hex}.yaml"
    with path.open("x", encoding="utf-8") as output:
        yaml.safe_dump(record, output, sort_keys=False, allow_unicode=True)
    (feature_dir(feature) / "workflow.yaml").write_text(
        yaml.safe_dump(snapshot(feature), sort_keys=False), encoding="utf-8")


def unchanged_event_history(base_ref):
    changes = run("git", "diff", "--name-status", f"{base_ref}...HEAD", "--", ".bmad/features")
    for line in changes.splitlines():
        action, *paths = line.split("\t")
        if any("/events/" in path.replace("\\", "/") for path in paths) and action != "A":
            raise GateError(f"Existing event modified or deleted: {line}")


def validate_code_changes(base_ref, repo):
    changed = [path.replace("\\", "/") for path in
               run("git", "diff", "--name-only", f"{base_ref}...HEAD", "--", "app").splitlines()]
    if not changed:
        return
    features = ROOT / ".bmad" / "features"
    if not features.is_dir():
        raise GateError("Application change has no approved planning feature")
    scopes = set()
    for directory in features.iterdir():
        if directory.is_dir() and approvals(directory.name).get("planning"):
            check(directory.name, "development", repo)
            manifest = ROOT / "bmad-output" / directory.name / "handoff-manifest.json"
            for story in json.loads(manifest.read_text(encoding="utf-8"))["stories"]:
                scopes.update(story["ownedScope"])
    for path in changed:
        if not any(path == owned.rstrip("/") or path.startswith(owned.rstrip("/") + "/")
                   for owned in scopes):
            raise GateError(f"Application change outside approved ready story scope: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "check", "record-approved", "request-changes", "validate-history"))
    parser.add_argument("feature")
    parser.add_argument("stage", nargs="?", choices=CHECKPOINTS)
    parser.add_argument("--pr", type=int)
    parser.add_argument("--artifacts", nargs="+")
    parser.add_argument("--repo", help="GitHub owner/repository (defaults to gh repo view)")
    options = parser.parse_args()
    try:
        repo = run("gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
        if options.repo and options.repo != repo:
            raise GateError("Supplied repository does not match the checkout")
        if os.environ.get("GATE_BASE_REF"):
            unchanged_event_history(os.environ["GATE_BASE_REF"])
        if options.command in ("check", "record-approved", "request-changes") and not options.stage:
            raise GateError("Stage is required")
        if options.command in ("record-approved", "request-changes") and options.stage not in STAGES:
            raise GateError("Only planning stages have recorded approvals")
        if options.command == "check":
            check(options.feature, options.stage, repo)
        elif options.command == "record-approved":
            if not options.pr:
                raise GateError("--pr is required")
            print(record_approval(options.feature, options.stage, options.pr, options.artifacts, repo))
        elif options.command == "request-changes":
            if not options.pr:
                raise GateError("--pr is required")
            print(request_changes(options.feature, options.stage, options.pr, repo))
        else:
            verify_snapshot(options.feature)
            current = approvals(options.feature)
            for record in events(options.feature):
                verify_event(record, repo, active=record == current.get(record["stage"]))
            if options.command == "status":
                print({stage: "approved" if approvals(options.feature).get(stage) else "pending" for stage in STAGES})
        print("PASS")
    except (GateError, OSError, KeyError, ValueError, yaml.YAMLError) as error:
        print(f"STOP: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())