# Django Security Configuration

## Implemented Features

1. **Custom Permissions**
   - Added `can_view`, `can_create`, `can_edit`, and `can_delete` permissions in the `Book` model.
   - Used Django admin to assign these permissions to groups: Editors, Viewers, and Admins.

2. **Access Control**
   - Views are secured using the `@permission_required` decorator to restrict unauthorized access.

3. **CSRF Protection**
   - All templates include `{% csrf_token %}` to prevent CSRF attacks.

4. **Secure Settings**
   - `DEBUG = False`
   - `SECURE_BROWSER_XSS_FILTER = True`
   - `SECURE_CONTENT_TYPE_NOSNIFF = True`
   - `X_FRAME_OPTIONS = 'DENY'`
   - `CSRF_COOKIE_SECURE = True`
   - `SESSION_COOKIE_SECURE = True`
   - Added a simple Content Security Policy (CSP) for script and style control.

5. **Data Security**
   - Views use Django’s ORM safely to prevent SQL injection.

## Testing
- Tested with different user groups to confirm permissions.
- Verified that forms reject invalid CSRF tokens.
- Checked HTTPS-only cookies behavior.
