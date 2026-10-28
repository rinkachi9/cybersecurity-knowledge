# OAuth

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## What it is?

OAuth (**Open Authorization**) is a widely-used protocol for **authorization**, enabling secure access to resources without exposing user credentials. It allows third-party applications to access resources on behalf of a user by issuing access tokens.

### What is OAuth?

OAuth provides a secure mechanism for granting limited access to user resources. It is often used in scenarios like:

- Allowing apps to access your Google Drive files.
- Granting a service access to your GitHub repositories.

Instead of sharing credentials directly, OAuth enables users to delegate access by authorizing an application to act on their behalf.

## Key concepts

- **Resource Owner:** The user who owns the resources being accessed (e.g., user files, data).
- **Client:** The application requesting access to the resource (e.g., a mobile app).
- **Resource Server:** The server hosting the user's resources (e.g., Google Drive, GitHub).
- **Authorization Server:** Issues tokens to the client after the user approves access (e.g., Google Accounts, Facebook OAuth).
- **Access Token:** A short-lived token used by the client to access the resource server.
- **Refresh Token:** A long-lived token used to obtain a new access token without requiring user interaction.

## How it works

OAuth operates by allowing a user to delegate access without sharing credentials. A typical flow involves the following steps:

### 1. Authorization Request

The client redirects the user to the authorization server with details about the request (e.g., scopes, client ID, redirect URI).

#### 2. User Consent

The user logs in to the authorization server (if not already logged in) and approves or denies the client’s request.

##### 3. Authorization Code

If approved, the server redirects the user back to the client with an **authorization code**.

##### 4. Token Exchange

The client exchanges the authorization code for an access token and optionally a refresh token by making a server-side request to the authorization server.

##### 5. Accessing Resources

The client uses the access token to access the resource server.

##### 6. Token Expiry and Refresh

When the access token expires, the client uses the refresh token to request a new one.

## Grant types

1. **Authorization Code Grant:**
   - Used by web apps and server-side applications.
   - Example use case: Allowing a website to access your Google Calendar.
2. **Implicit Grant (Deprecated):**
   - Used by Single Page Applications (SPAs) but is now discouraged due to security risks.
3. **Client Credentials Grant:**
   - Used for machine-to-machine (M2M) communication.
   - Example use case: An API authenticates itself to another API.
4. **Resource Owner Password Credentials Grant:**
   - The client collects the user's username and password directly.
   - **Avoid using this grant** due to security concerns.
5. **Device Authorization Grant:**
   - Designed for devices without browsers (e.g., smart TVs).
   - The user logs in on a separate device to authorize.
6. **PKCE (Proof Key for Code Exchange):**
   - Enhances the Authorization Code flow, especially for SPAs and mobile apps, by mitigating token interception risks.

## Example

**Scenario:** A blogging platform wants to access a user's Google Drive to upload images.

1. **Authorization Request:** The blogging platform redirects the user to Google's OAuth server.
2. **User Consent:** The user logs into Google and grants permission to access their Google Drive.
3. **Authorization Code:** Google redirects the user back to the blogging platform with an authorization code.
4. **Token Exchange:** The blogging platform exchanges the code for an access token.
5. **Access Resource:** The blogging platform uses the token to upload images to Google Drive on the user’s behalf.

## Best practices

1. **Use HTTPS:** Always enforce HTTPS to prevent token interception.
2. **Implement PKCE:** Use PKCE to enhance security for public clients like mobile apps or SPAs.
3. **Short-Lived Tokens:** Keep access tokens short-lived to minimize their misuse.
4. **Secure Storage:** Store refresh tokens securely (e.g., encrypted storage).
5. **Restrict Scopes:** Request only the necessary permissions (scopes) to reduce risk.
6. **Use State Parameter:** Include a `state` parameter in the authorization request to prevent CSRF attacks.
7. **Monitor and Revoke Tokens:** Implement token revocation mechanisms and monitor usage for anomalies.

## Limitations

1. **Complex Implementation:** OAuth flows can be complex, requiring careful handling of redirects, tokens, and scopes.
2. **Token Misuse:** Access tokens can be intercepted or misused if not handled securely.
3. **Reliance on Third Parties:** OAuth depends on the availability and security of the authorization server.

## Use cases

1. **Third-Party App Access:** Allowing third-party apps to access user accounts without sharing credentials (e.g., "Sign in with Google").
2. **API Authorization:** Securing APIs by issuing scoped tokens for clients.
3. **Single Sign-On (SSO):** Enabling users to log in across multiple systems using a single identity provider.

## Trade offs and when to use it

TODO: cover benefits, costs, alternatives and the situations where this is the wrong choice.

## Common mistakes

TODO: list frequent misunderstandings and failure modes, each with its fix.

## Practice

TODO: add questions or small exercises, with answers or hints at the bottom.

## Further reading

TODO: add annotated links to primary sources.
