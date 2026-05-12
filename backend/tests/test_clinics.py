"""
Tests for GET/POST/PUT/DELETE /api/v1/clinics endpoints.

Endpoints (backend_developer.md):
  GET    /api/v1/clinics                  — paginated list with filters
  GET    /api/v1/clinics/{id}             — clinic detail
  GET    /api/v1/clinics/{id}/doctors     — clinic's doctor list
  GET    /api/v1/clinics/{id}/services    — clinic's service list
  GET    /api/v1/clinics/{id}/reviews     — clinic's reviews
  POST   /api/v1/clinics                  — create (admin only)
  PUT    /api/v1/clinics/{id}             — update (admin only)
  DELETE /api/v1/clinics/{id}             — delete (admin only)

Coverage targets (qa_engineer.md):
  - API endpoints: 100 %
  - Backend lines:  ≥ 80 %

TODO: implement test methods once backend/app/routers/clinics.py is done.
"""

import pytest


@pytest.mark.integration
class TestClinicsListAPI:
    """GET /api/v1/clinics — list, pagination, filtering, search."""

    # TODO: test_get_clinics_returns_paginated_response
    # TODO: test_get_clinics_pagination_limit
    # TODO: test_get_clinics_filter_by_city
    # TODO: test_get_clinics_filter_by_district
    # TODO: test_get_clinics_filter_by_specialty
    # TODO: test_get_clinics_filter_by_min_rating
    # TODO: test_get_clinics_search_by_name
    # TODO: test_get_clinics_empty_result_returns_empty_items


@pytest.mark.integration
class TestClinicDetailAPI:
    """GET /api/v1/clinics/{id} — single clinic."""

    # TODO: test_get_clinic_by_id_returns_correct_fields
    # TODO: test_get_clinic_not_found_returns_404


@pytest.mark.integration
class TestClinicRelationsAPI:
    """Nested resource endpoints under /api/v1/clinics/{id}/."""

    # TODO: test_get_clinic_doctors_returns_list
    # TODO: test_get_clinic_services_returns_list
    # TODO: test_get_clinic_reviews_returns_list


@pytest.mark.integration
class TestClinicWriteAPI:
    """POST / PUT / DELETE — admin-only mutations."""

    # TODO: test_create_clinic_without_auth_returns_401
    # TODO: test_create_clinic_as_patient_returns_403
    # TODO: test_create_clinic_as_admin_returns_201
    # TODO: test_update_clinic_as_admin_returns_200
    # TODO: test_delete_clinic_as_admin_returns_204
