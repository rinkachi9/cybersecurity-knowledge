# JWT vs Session

## Summary

TODO: write two to four plain language sentences that say what this is and why it matters.

## Prerequisites

TODO: link the notes a reader should know first and state the assumed knowledge.



## Session-based

In this approach, you store the session information in a database or session store and hand over a session ID to the user.

Think of it like a passenger getting just the Ticket ID of their flight while all other details are stored in the airline’s database.

Here’s how it works:

1. The user makes a login request and the frontend app sends the request to the backend server.
2. The backend creates a session using a secret key and stores the data in session storage.
3. The server sends a cookie back to the client with the unique session ID.
4. The user makes a new request and the browser sends the session ID along with the request.
5. The server authenticates the user using the session ID.

## JWT-based

In the JWT-based approach, you don’t store the session information in the session store.

The entire information is available within the token.

Think of it like getting the flight ticket along with all the details available on the ticket but encoded.

Here’s how it works:

1. The user makes a login request and it goes to the backend server.
2. The server verifies the credentials and issues a JWT. The JWT is signed using a private key and no session storage is involved.
3. The JWT is passed to the client, either as a cookie or in the response body. Both approaches have their pros and cons but we’ve gone with the cookie approach.
4. For every subsequent request, the browser sends the cookie with the JWT.
5. The server verifies the JWT using the secret private key and extracts the user info.

![Comparison of session-based and JWT-based authentication flows, with a table: sessions need separate storage, are easy to invalidate and scale with the session store; JWTs need no separate storage, are not easy to invalidate and scale easily. Image credit: ByteByteGo.](../../assets/identity-and-access/jwt-vs-session-comparison.png)

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
