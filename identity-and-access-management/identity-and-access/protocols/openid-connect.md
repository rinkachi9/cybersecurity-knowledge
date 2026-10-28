# OpenID Connect (OIDC)

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

**OpenID Connect (OIDC)** is a modern identity layer built on top of OAuth 2.0. While OAuth is primarily used for authorization, OIDC focuses on **authentication**, providing a secure way to verify a user's identity and retrieve user information.

### What is OpenID Connect?

OIDC allows applications (clients) to authenticate users via a trusted identity provider (IdP) without managing passwords directly. It provides a standardized mechanism for identity verification using **ID tokens** and enables single sign-on (SSO) across applications.

## Key concepts

1. **ID Token:**
   - A JWT (JSON Web Token) containing information about the authenticated user, such as their user ID and email.
   - Signed by the identity provider to ensure integrity and authenticity.
2. **Scopes:**
   - Define the information or permissions requested by the client (e.g., `openid`, `profile`, `email`).
   - Common scopes include:
     - `openid`: Mandatory for OIDC.
     - `profile`: Requests basic user information (name, gender, etc.).
     - `email`: Requests the user's email address.
3. **Endpoints:**
   - **Authorization Endpoint:** Used to authenticate the user and obtain authorization.
   - **Token Endpoint:** Used to exchange an authorization code for tokens.
   - **UserInfo Endpoint:** Provides additional user information (e.g., profile data).
4. **Claims:**
   - Pieces of information about the user included in the ID token or retrieved via the UserInfo endpoint.

## How it works

OIDC extends OAuth 2.0 by adding the concept of authentication. Here's how it typically works:

1. **Authentication Request:**
   - The client redirects the user to the authorization server with an `openid` scope.
2. **User Authentication:**
   - The user logs in to the identity provider (e.g., Google, Okta).
3. **Authorization Code:**
   - If authentication is successful, the server redirects the user back to the client with an authorization code.
4. **Token Exchange:**
   - The client exchanges the authorization code for an ID token and access token by calling the token endpoint.
5. **ID Token Validation:**
   - The client validates the ID token's signature, issuer (`iss`), audience (`aud`), and expiration (`exp`).
6. **Retrieve User Information (Optional):**
   - The client can use the access token to call the UserInfo endpoint for additional user details.

## Example

**Scenario:** A web application integrates with an identity provider (e.g., Google) to authenticate users.

1. **User Login:**
   - The user clicks "Sign in with Google."
   - The app redirects the user to Google’s authorization endpoint.
2. **Authentication:**
   - The user logs in to Google.
3. **Token Exchange:**
   - After successful login, the app exchanges the authorization code for tokens (ID token and access token).
4. **User Identification:**
   - The app decodes and validates the ID token to authenticate the user.
5. **Optional UserInfo Call:**
   - The app calls the UserInfo endpoint for additional user details if required.

## OIDC flows

OIDC supports several authentication flows based on the application type:

1. **Authorization Code Flow:** Used by server-side applications. Offers high security as tokens are not exposed to the browser.
2. **Implicit Flow (Deprecated):** Designed for Single Page Applications (SPAs) but now discouraged due to security risks.
3. **Hybrid Flow:** Combines the features of Authorization Code and Implicit flows.
4. **Device Flow:** For devices without browsers, such as smart TVs or IoT devices.
5. **PKCE (Proof Key for Code Exchange):** Secures the Authorization Code flow for public clients (SPAs, mobile apps).

## Best practices

1. **Use HTTPS:** Ensure all communication with the authorization server is encrypted.
2. **Implement PKCE:** Protect Authorization Code flows for SPAs and mobile apps.
3. **Validate ID Tokens:** Verify the token’s signature, issuer, audience, and expiration.
4. **Minimize Scopes:** Request only the scopes necessary for your application.
5. **Use Secure Storage:** Store tokens securely (e.g., HTTP-only cookies for web apps).
6. **Implement Refresh Tokens Securely:** Use refresh tokens for session persistence but store them securely.
7. **Monitor and Revoke Tokens:** Implement token revocation mechanisms and log token activity.
8. **Avoid Implicit Flow:** Use Authorization Code flow with PKCE instead of Implicit flow.

## Use cases

1. **Single Sign-On (SSO):** Allows users to log in once and access multiple applications seamlessly.
2. **Federated Identity:** Authenticate users across systems using a central identity provider (e.g., enterprise apps integrating with Okta).
3. **User Identity in APIs:** Use ID tokens to authenticate users in API calls.

## Advantages

1. **User-Friendly:** Simplifies login for users (e.g., "Sign in with Google").
2. **Standardized:** Provides a consistent approach to authentication across applications.
3. **Scalable:** Easily integrates with modern identity providers.
4. **Secure:** Combines OAuth’s authorization mechanisms with robust identity verification.

## Limitations

1. **Complex Implementation:** Requires understanding of JWTs, token validation, and flows.
2. **Reliance on IdP:** Downtime or compromise of the identity provider can impact authentication.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
