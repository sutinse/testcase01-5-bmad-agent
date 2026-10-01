package io.github.sutinse.refundapproval.security;

import jakarta.inject.Inject;
import jakarta.annotation.security.RolesAllowed;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import org.eclipse.microprofile.jwt.JsonWebToken;

@Path("/test/claims")
public class TestClaimsResource {
    @Inject
    ValidatedClaimsGuard guard;
    @Inject
    JsonWebToken token;

    @GET
    @RolesAllowed("refund-system")
    public String claims() {
        return guard.requireSubject(token);
    }

    @GET
    @Path("/approver")
    @RolesAllowed("refund-approver")
    public String approverClaims() {
        return guard.requireSubject(token);
    }
}