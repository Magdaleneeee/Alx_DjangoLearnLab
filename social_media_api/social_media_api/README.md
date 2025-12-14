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

## Deployment

This Django REST API is deployed to production using Render.

### Live URL
https://your-render-url.onrender.com

### Production Stack
- Django REST Framework
- Gunicorn (WSGI server)
- WhiteNoise for static files
- Render Cloud Hosting

### Notes
- Environment variables are managed via the hosting platform
- DEBUG is disabled in production
- Security headers are enabled
