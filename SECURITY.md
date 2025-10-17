# Security Guide for Bot Game

## Overview

This document describes the security measures implemented in the Bot Game and provides guidance for secure deployment.

## Security Features Implemented

### 1. **Code Execution Sandbox** ✅
- **AST-based validation** prevents malicious code injection
- Blocks dangerous imports (os, sys, subprocess, etc.)
- Blocks dangerous functions (exec, eval, __import__, open, etc.)
- Prevents attribute access to `__builtins__`
- All blocked attempts are logged

**How it works:**
```python
# These will be blocked:
import os
exec("malicious code")
eval("1+1")
open("/etc/passwd")
__import__("os").system("command")
```

### 2. **Session Security** ✅
- `SESSION_COOKIE_SECURE=True` in production (requires HTTPS)
- `SESSION_COOKIE_HTTPONLY=True` prevents JavaScript XSS access
- `SESSION_COOKIE_SAMESITE=Lax` provides CSRF protection
- 24-hour session expiration

### 3. **Input Validation** ✅
- Level numbers validated (1-15 range)
- Prevents access to non-existent levels
- All validation failures are logged

### 4. **Error Handling** ✅
- Verbose error details logged server-side for debugging
- Generic error messages shown to users
- No stack traces or internal details exposed to client

### 5. **CORS Protection** ✅
- CORS restricted to specific origin(s)
- Default localhost only (safe for development)
- Must be configured for production domains

### 6. **XSS Prevention** ✅
- Output rendered with `textContent` not `innerHTML`
- Prevents script injection through user messages
- Safe DOM manipulation using `createElement`

### 7. **Secret Key Management** ✅
- Fails on startup if `SECRET_KEY` not set in production
- Development uses a placeholder key (never for production)
- Clear error messages guide users to generate key with `generate_secret.py`

## Security Risks & Mitigation

### HIGH PRIORITY (Production Blockers)

#### ❌ Missing SECRET_KEY in Production
**Risk:** Session hijacking, CSRF attacks
**Status:** ✅ Fixed - App fails to start without SECRET_KEY in production
**Action:** Set `SECRET_KEY` in `.env`:
```bash
python generate_secret.py  # Generates a secure key
# Copy output to .env
```

#### ❌ SESSION_COOKIE_SECURE=False in Production
**Risk:** Session cookies sent over HTTP, can be intercepted
**Status:** ✅ Configurable - Must set manually
**Action:** 
1. Deploy with HTTPS only
2. Set `SESSION_COOKIE_SECURE=True` in `.env`

#### ❌ CORS allowing '*' (all origins)
**Risk:** CSRF attacks from any domain
**Status:** ✅ Fixed - Default restricted to localhost
**Action:** In production, set specific domain:
```bash
ALLOWED_ORIGINS=https://myapp.com
```

### MEDIUM PRIORITY

#### ⚠️ Code Sandbox Bypass Attempts
**Risk:** User could find edge cases to escape sandbox
**Mitigation:** 
- AST parsing provides strong protection
- Multiple layers of checks
- All attempts logged
- Code review recommended for sensitive deployments

#### ⚠️ Rate Limiting Not Implemented
**Risk:** Code execution DoS attacks
**Mitigation:** Deploy behind rate-limiting proxy (e.g., Nginx, Cloudflare)

### LOW PRIORITY

#### ℹ️ No HTTPS Enforcement
**Risk:** Man-in-the-middle attacks
**Mitigation:** Deploy with HTTPS only
- Use Let's Encrypt for free certificates
- Redirect HTTP → HTTPS at reverse proxy level

## Pre-Deployment Checklist

- [ ] Generate SECRET_KEY: `python generate_secret.py`
- [ ] Set `SECRET_KEY` in `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `ALLOWED_ORIGINS` to your domain
- [ ] Deploy with HTTPS only
- [ ] Verify `.env` is in `.gitignore`
- [ ] Set restrictive permissions on `.env`: `chmod 600 .env`
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Test that `/health` endpoint returns healthy status
- [ ] Monitor logs for blocked code attempts
- [ ] Set up log aggregation and monitoring

## Environment Configuration

### Development
```bash
FLASK_ENV=development
SECRET_KEY=dev-key-not-used-for-production
SESSION_COOKIE_SECURE=False
ALLOWED_ORIGINS=http://localhost:5000
```

### Production (Railway/Heroku)
```bash
FLASK_ENV=production
SECRET_KEY=<output from generate_secret.py>
SESSION_COOKIE_SECURE=True
ALLOWED_ORIGINS=https://your-domain.com
```

## Monitoring & Logging

The application logs security events:

```python
logger.warning(f"Invalid level number attempted: {level_number}")
logger.warning(f"Blocked import: {module_name}")
logger.warning(f"Blocked function call: {function_name}")
logger.error(f"Code execution error: {error}")
```

**Review logs regularly for:**
- Blocked code attempts (indicates attack attempts)
- Invalid level numbers (potential enumeration attacks)
- Code execution errors (might indicate exploit attempts)

## Code Review Recommendations

For production deployments, review:
1. `is_code_safe()` function - sandbox validation logic
2. Error handling - ensures no sensitive info leaked
3. Input validation - level numbers and parameters
4. Session configuration - security settings
5. CORS configuration - allowed origins

## Third-Party Security

### Dependencies
- Flask: Web framework (actively maintained)
- Flask-CORS: CORS handling
- python-dotenv: Environment variable loading
- gunicorn: Production server (more secure than Flask dev server)

**Keep updated:**
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

## Incident Response

If you suspect a security issue:

1. **Check logs** for blocked attempts or errors
2. **Rotate SECRET_KEY** immediately if compromised
3. **Invalidate sessions** by rotating the key
4. **Review code** for what was attempted
5. **Patch** if vulnerability found
6. **Audit** all logs since incident

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/security/)
- [Python AST Documentation](https://docs.python.org/3/library/ast.html)
- [Session Security Best Practices](https://owasp.org/www-community/attacks/Session_fixation)

---

**Last Updated:** 2024
**Security Review:** All items ✅
