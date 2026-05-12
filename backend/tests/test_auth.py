"""
Tests for /api/v1/auth — registration, login, token refresh, /me.

Endpoints (backend_developer.md):
  POST /api/v1/auth/register   — create new user account
  POST /api/v1/auth/login      — returns JWT access token
  POST /api/v1/auth/refresh    — refresh expired token
  GET  /api/v1/auth/me         — return current authenticated user

Token format: Bearer JWT (python-jose / HS256, stored in localStorage on FE).

TODO: implement test methods once backend/app/routers/auth.py is done.
"""

import pytest


@pytest.mark.integration
class TestRegisterAPI:
    """POST /api/v1/auth/register."""

    # TODO: test_register_success_returns_201_with_user_id
    # TODO: test_register_duplicate_email_returns_400
    # TODO: test_register_invalid_email_format_returns_422
    # TODO: test_register_short_password_returns_422
    # TODO: test_register_missing_full_name_returns_422


@pytest.mark.integration
class TestLoginAPI:
    """POST /api/v1/auth/login — OAuth2 password flow."""

    # TODO: test_login_success_returns_access_token
    # TODO: test_login_wrong_password_returns_401
    # TODO: test_login_unknown_email_returns_401
    # TODO: test_login_inactive_user_returns_401


@pytest.mark.integration
class TestRefreshAPI:
    """POST /api/v1/auth/refresh."""

    # TODO: test_refresh_with_valid_token_returns_new_token
    # TODO: test_refresh_with_expired_token_returns_401


@pytest.mark.integration
class TestMeAPI:
    """GET /api/v1/auth/me."""

    # TODO: test_me_returns_current_user_data
    # TODO: test_me_without_auth_returns_401
    # TODO: test_me_returns_correct_role_field
