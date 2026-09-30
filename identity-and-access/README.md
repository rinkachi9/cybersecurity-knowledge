# Identity and access

How systems establish who a user is (authentication) and what that user may do (authorization), including token and federation protocols.

## Notes

- [Authentication vs Authorization](authentication-vs-authorization.md): Side by side comparison of the two concepts.
- [Authorization](authorization.md): Allowing or refusing access to resources after authentication.

### Authentication

Proving identity: methods, tokens and sessions.

Entry point: [authentication](authentication/README.md).

- [Authentication methods](authentication/authentication-methods.md): Common ways of proving identity.
- [Token-Based Authentication (JWT)](authentication/token-based-authentication-jwt.md): Signed tokens (JWT) as a way to verify identity.
- [JWT vs Session](authentication/jwt-vs-session.md): Stateless tokens compared with server-side sessions.

### Protocols

Delegated authorization and federated identity protocols.

Entry point: [protocols](protocols/README.md).

- [OAuth](protocols/oauth.md): The OAuth delegated authorization protocol.
- [OpenID Connect (OIDC)](protocols/openid-connect.md): The OpenID Connect identity layer on top of OAuth 2.0.

## Planned topics

These topics are not written yet. They are listed so the scope of the area is visible.

- Multi-factor authentication in depth
- Single sign-on and SAML
- Session management
- Privileged access management
- Access control models

Back to the [table of contents](../ToC.md).
