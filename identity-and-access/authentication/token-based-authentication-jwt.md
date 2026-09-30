# Token-Based Authentication (JWT)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**Token-based authentication** is a modern method that uses digitally-signed tokens (e.g., JSON Web Tokens, or JWTs) to verify the identity of users and grant access to protected resources. It is stateless, scalable, and widely used in modern web applications and APIs.

### What is JWT?

**JWT (JSON Web Token)** is a compact, URL-safe token format used for securely transmitting information between parties. It is typically composed of three parts:

1. **Header:** Contains metadata about the token, including the signing algorithm (e.g., HMAC, RSA).
2. **Payload:** Contains claims, which are pieces of information about the user or system (e.g., `user_id`, `roles`).
3. **Signature:** A cryptographic signature generated using a secret or private key, ensuring the token's integrity.

## How it works?

1. **User Authentication:**
   - The user provides credentials (e.g., username and password) to the authentication server.
   - The server validates the credentials.
2. **Token Issuance:**
   - If credentials are valid, the server generates a JWT containing claims about the user and signs it with a secret or private key.
   - The token is sent back to the user.
3. **Token Storage:**
   - The client stores the token, typically in **localStorage**, **sessionStorage**, or as an **HTTP-only cookie**.
4. **Accessing Protected Resources:**
   - For subsequent requests, the client sends the JWT in the Authorization header as a Bearer
   - The server verifies the token's signature to confirm its authenticity and validity.
5. **Authorization:**
   - The server extracts claims from the token (e.g., user roles) to determine access permissions.
6. **Token Expiry and Refresh:**
   - JWTs usually have an expiration time (`exp` claim). Once expired, users must request a new token, often using a refresh token.

## Best practices

1. **Secure Token Storage:**
   - Use HTTP-only, Secure cookies for storing tokens to protect against XSS.
   - Avoid storing sensitive information in the token payload.
2. **Set Expiration Times:**
   - Include short-lived expiration times for access tokens to minimize misuse.
3. **Use HTTPS:**
   - Always transmit tokens over HTTPS to prevent interception.
4. **Implement Refresh Tokens:**
   - Use refresh tokens to maintain session longevity while keeping access tokens short-lived.
5. **Validate Token Signature:**
   - Verify tokens using the same secret or public/private key used to sign them.
6. **Restrict Token Scope:**
   - Include claims to specify permissions and avoid over-permissioned tokens.
7. **Revoke Tokens if Necessary:**
   - Use a blacklist or token versioning mechanism to invalidate compromised tokens.
8. **Adopt Strong Signing Algorithms:**
   - Use robust algorithms like RS256 (RSA) or HS256 (HMAC) for signing tokens.
9. **Audit and Monitor Usage:**
   - Log token usage to detect anomalies such as replay attacks.
10. **Prevent CSRF:**
11. Pair JWTs with CSRF tokens or implement same-site cookies for additional protection.

## Use Cases

1. **API Authentication:** Secures RESTful APIs by passing JWTs as bearer tokens in the Authorization header.
2. **Single Sign-On (SSO):** JWTs are used to transmit user credentials securely across multiple systems.
3. **Mobile and SPA Authentication:** Stateless authentication for mobile apps and Single Page Applications (SPAs).

## Limitations

1. **Payload Size:** Tokens can become large if too much information is embedded in the payload.
2. **Revocation Challenges:** JWTs are stateless, so revoking tokens before expiry can be complex.
3. **No Built-In Encryption:** JWTs are only signed, not encrypted, so sensitive data in the payload can be read if intercepted.

## Worked example

TODO: add a concrete, reproducible example that walks through the idea end to end.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
