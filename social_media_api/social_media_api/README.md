## Posts & Comments API

### Posts
- GET /api/posts/
- POST /api/posts/
- PUT /api/posts/{id}/
- DELETE /api/posts/{id}/

### Comments
- GET /api/comments/
- POST /api/comments/
- PUT /api/comments/{id}/
- DELETE /api/comments/{id}/

### Permissions
- Only authors can edit or delete their posts and comments
- Authentication is required for all endpoints

## Follow & Feed API

### Follow a user
POST /api/accounts/follow/{user_id}/

### Unfollow a user
POST /api/accounts/unfollow/{user_id}/

### Feed
GET /api/feed/

The feed returns posts from users that the authenticated user follows, ordered by most recent first.
