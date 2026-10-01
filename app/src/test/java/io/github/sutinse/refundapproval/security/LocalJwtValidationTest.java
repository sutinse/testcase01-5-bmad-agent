package io.github.sutinse.refundapproval.security;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

import java.time.Instant;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;

import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;

@QuarkusTest
@QuarkusTestResource(TestTokenFactory.class)
class LocalJwtValidationTest {
    @Test
    void acceptsValidatedIdentity() {
        given().auth().oauth2(TestTokenFactory.token("processor-one", List.of("refund-system")))
                .get("/test/claims").then().statusCode(200).body(equalTo("processor-one"));
        given().auth().oauth2(TestTokenFactory.token("approver-one", List.of("refund-approver")))
            .get("/test/claims/approver").then().statusCode(200).body(equalTo("approver-one"));
        given().auth().oauth2(TestTokenFactory.token("processor-one", List.of("refund-system")))
            .get("/test/claims/approver").then().statusCode(403);
    }

    @Test
    void rejectsWrongIssuerAudienceAndExpiry() {
        for (String claim : List.of("iss", "aud", "exp")) {
            Map<String, Object> claims = TestTokenFactory.claims();
            claims.put(claim, switch (claim) {
                case "iss" -> "other-issuer";
                case "aud" -> List.of("other-audience");
                default -> Instant.now().minusSeconds(60).getEpochSecond();
            });
            given().auth().oauth2(TestTokenFactory.sign(claims))
                    .get("/test/claims").then().statusCode(401);
            claims.remove(claim);
            given().auth().oauth2(TestTokenFactory.sign(claims))
                    .get("/test/claims").then().statusCode(401);
        }
        Map<String, Object> wrongAudienceList = TestTokenFactory.claims();
        wrongAudienceList.put("aud", List.of("other-audience", "another-audience"));
        given().auth().oauth2(TestTokenFactory.sign(wrongAudienceList))
            .get("/test/claims").then().statusCode(401);
        given().auth().oauth2(TestTokenFactory.signedWithAnotherKey())
            .get("/test/claims").then().statusCode(401);
        given().get("/test/claims").then().statusCode(401);
    }

    @Test
    void rejectsInvalidClaimContentsAndWrongRole() {
        for (String subject : new String[] {null, "", "   "}) {
            given().auth().oauth2(TestTokenFactory.token(subject, List.of("refund-system")))
                    .get("/test/claims").then().statusCode(401).contentType("application/problem+json");
        }
        for (List<String> groups : new List[] {null, List.of(), List.of("", "   ")}) {
            given().auth().oauth2(TestTokenFactory.token("processor-one", groups))
                    .get("/test/claims").then().statusCode(401).contentType("application/problem+json");
        }
        given().auth().oauth2(TestTokenFactory.token("processor-one", List.of(" ", "refund-system")))
                .get("/test/claims").then().statusCode(200);
        given().auth().oauth2(TestTokenFactory.token("processor-one", List.of("refund-approver")))
                .get("/test/claims").then().statusCode(403);
    }
}