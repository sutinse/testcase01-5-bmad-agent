package io.github.sutinse.refundapproval.security;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.PrivateKey;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Base64;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.quarkus.test.common.QuarkusTestResourceLifecycleManager;

public class TestTokenFactory implements QuarkusTestResourceLifecycleManager {
    static final String ISSUER = "local-mvp-test";
    static final String AUDIENCE = "refund-approval-check";
    private static final KeyPair KEYS = generateKeys();

    private static KeyPair generateKeys() {
        try {
            KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
            generator.initialize(2048);
            return generator.generateKeyPair();
        } catch (Exception exception) {
            throw new IllegalStateException("Unable to generate test keypair", exception);
        }
    }

    @Override
    public Map<String, String> start() {
        String publicKey = "-----BEGIN PUBLIC KEY-----\n"
                + Base64.getMimeEncoder(64, new byte[] {'\n'}).encodeToString(KEYS.getPublic().getEncoded())
                + "\n-----END PUBLIC KEY-----";
        return Map.of("mp.jwt.verify.publickey", publicKey,
                "mp.jwt.verify.issuer", ISSUER,
                "mp.jwt.verify.audiences", AUDIENCE);
    }

    @Override
    public void stop() {
    }

    static String token(String subject, List<String> groups) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", ISSUER);
        claims.put("aud", List.of(AUDIENCE));
        claims.put("iat", Instant.now().getEpochSecond());
        claims.put("exp", Instant.now().plusSeconds(300).getEpochSecond());
        if (subject != null) claims.put("sub", subject);
        if (groups != null) claims.put("groups", groups);
        return sign(claims);
    }

    static String sign(Map<String, Object> claims) {
        return sign(claims, KEYS.getPrivate());
    }

    static String signedWithAnotherKey() {
        return sign(claims(), generateKeys().getPrivate());
    }

    private static String sign(Map<String, Object> claims, PrivateKey privateKey) {
        try {
            Base64.Encoder encoder = Base64.getUrlEncoder().withoutPadding();
            String header = encoder.encodeToString("{\"alg\":\"RS256\",\"typ\":\"JWT\"}".getBytes(StandardCharsets.UTF_8));
            String payload = encoder.encodeToString(new ObjectMapper().writeValueAsBytes(claims));
            String input = header + "." + payload;
            Signature signer = Signature.getInstance("SHA256withRSA");
            signer.initSign(privateKey);
            signer.update(input.getBytes(StandardCharsets.US_ASCII));
            return input + "." + encoder.encodeToString(signer.sign());
        } catch (Exception exception) {
            throw new IllegalStateException("Unable to sign test token", exception);
        }
    }

    static Map<String, Object> claims() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", ISSUER);
        claims.put("aud", List.of(AUDIENCE));
        claims.put("iat", Instant.now().getEpochSecond());
        claims.put("exp", Instant.now().plusSeconds(300).getEpochSecond());
        claims.put("sub", "processor-one");
        claims.put("groups", List.of("refund-system"));
        return claims;
    }
}