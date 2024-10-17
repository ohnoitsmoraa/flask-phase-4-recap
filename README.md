# API
- Helps applications to communicate with each other.
- Examples of APIs:
    - GET/ GET ALL / GET BY ID
    - POST
    - PATCH
    - DELETE
    - PUT

- HTTP requests that DON'T require ID => GET ALL & POST
- HTTP requets that require ID => GET BY ID, DELETE, PATCH

example: users
GET/api/users
POST/api/users

## AUTHENTICATION & AUTHORIZATION
- **Authentication** is  proving one's identity to an application in order to access protected information; logging in.

- **Authorization** is allowing or disallowing access to resources based on a user's attributes.

### JWT AUTHENTICATION
- SETUP AUTH => install, secret key, initialkize it with our app

### LOGIN
- Create access token and refresh token
- Protecting the API endpoints
- Handles JWT authentication errors
- Logout

