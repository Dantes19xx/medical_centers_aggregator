"""
Tests for /api/v1/reviews — clinic and doctor reviews.

Endpoints (backend_developer.md):
  POST /api/v1/reviews              — submit review (auth required)
  GET  /api/v1/reviews              — list reviews (filter: clinic_id, doctor_id)

Review model constraints:
  - rating: integer 1–5
  - clinic_id OR doctor_id must be set (not both null)
  - is_moderated defaults to False (admin approves)

TODO: implement test methods once backend/app/routers/reviews.py is done.
"""

import pytest


@pytest.mark.integration
class TestCreateReviewAPI:
    """POST /api/v1/reviews."""

    # TODO: test_create_clinic_review_success_returns_201
    # TODO: test_create_doctor_review_success_returns_201
    # TODO: test_create_review_without_auth_returns_401
    # TODO: test_create_review_invalid_rating_below_1_returns_422
    # TODO: test_create_review_invalid_rating_above_5_returns_422
    # TODO: test_create_review_no_target_returns_422  # neither clinic_id nor doctor_id
    # TODO: test_create_review_nonexistent_clinic_returns_404


@pytest.mark.integration
class TestListReviewsAPI:
    """GET /api/v1/reviews."""

    # TODO: test_get_reviews_filter_by_clinic_id
    # TODO: test_get_reviews_filter_by_doctor_id
    # TODO: test_get_reviews_only_moderated_visible_to_public
    # TODO: test_get_reviews_unmoderated_visible_to_admin
