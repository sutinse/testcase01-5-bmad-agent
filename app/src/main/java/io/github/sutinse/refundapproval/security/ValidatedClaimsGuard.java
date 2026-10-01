package io.github.sutinse.refundapproval.security;

import java.util.Map;
import java.util.Set;

import org.eclipse.microprofile.jwt.JsonWebToken;

import jakarta.enterprise.context.ApplicationScoped;
import io.quarkus.security.identity.SecurityIdentity;
import io.quarkus.vertx.http.runtime.security.HttpSecurityPolicy;
import io.smallrye.mutiny.Uni;
import io.vertx.ext.web.RoutingContext;
import jakarta.ws.rs.core.Response;

@ApplicationScoped
public class ValidatedClaimsGuard implements HttpSecurityPolicy {

    @Override
    public String name() {
        return "validated-claims";
    }

    @Override
    public Uni<CheckResult> checkPermission(RoutingContext context, Uni<SecurityIdentity> identity,
            AuthorizationRequestContext requestContext) {
        return identity.onItem().transform(current -> {
            if (current.isAnonymous() || !(current.getPrincipal() instanceof JsonWebToken token)
                    || !hasClaims(token)) {
                if (!context.response().ended()) {
                    context.response().setStatusCode(401)
                            .putHeader("Content-Type", "application/problem+json")
                                .end("{\"type\":\"about:blank\",\"title\":\"Unauthorized\",\"status\":401,"
                                    + "\"detail\":\"Required identity claims are missing or blank\"}");
                }
                return CheckResult.DENY;
            }
            return CheckResult.PERMIT;
        });
    }

    public String requireSubject(JsonWebToken token) {
        if (!hasClaims(token)) {
            throw new InvalidClaimsException();
        }
        return token.getSubject();
    }

    private boolean hasClaims(JsonWebToken token) {
        String subject = token.getSubject();
        Set<String> groups = token.getGroups();
        return subject != null && !subject.isBlank() && token.containsClaim("groups") && groups != null
                && groups.stream().anyMatch(group -> group != null && !group.isBlank());
    }

    public static final class InvalidClaimsException extends RuntimeException {
        public Response toResponse() {
            return Response.status(Response.Status.UNAUTHORIZED)
                    .type("application/problem+json")
                    .entity(Map.of("type", "about:blank", "title", "Unauthorized", "status", 401,
                            "detail", "Required identity claims are missing or blank"))
                    .build();
        }
    }
}
