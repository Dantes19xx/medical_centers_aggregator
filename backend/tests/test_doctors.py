"""
Tests for /api/v1/doctors endpoints.

Endpoints (backend_developer.md):
  GET  /api/v1/doctors                — paginated list with filters
  GET  /api/v1/doctors/{id}           — doctor profile
  GET  /api/v1/doctors/{id}/reviews   — reviews for a doctor
  GET  /api/v1/doctors/specialties    — distinct specialties list
  GET  /api/v1/doctors/{id}/slots     — available time slots (?date=YYYY-MM-DD)
  POST /api/v1/doctors                — add doctor (admin)
  PUT  /api/v1/doctors/{id}           — update doctor (admin)

TODO: implement test methods once backend/app/routers/doctors.py is done.
"""

import pytest


@pytest.mark.integration
class TestDoctorsListAPI:
    """GET /api/v1/doctors — list, filters."""

    # TODO: test_get_doctors_returns_paginated_response
    # TODO: test_get_doctors_filter_by_specialty
    # TODO: test_get_doctors_filter_by_clinic_id
    # TODO: test_get_doctors_filter_by_max_price
    # TODO: test_get_doctors_filter_by_min_rating
    # TODO: test_get_doctors_search_by_name


@pytest.mark.integration
class TestDoctorDetailAPI:
    """GET /api/v1/doctors/{id}."""

    # TODO: test_get_doctor_by_id_returns_correct_fields
    # TODO: test_get_doctor_not_found_returns_404


@pytest.mark.integration
class TestDoctorSlotsAPI:
    """GET /api/v1/doctors/{id}/slots."""

    # TODO: test_get_slots_returns_list_of_times
    # TODO: test_get_slots_excludes_already_booked_times
    # TODO: test_get_slots_requires_date_param


@pytest.mark.integration
class TestDoctorSpecialtiesAPI:
    """GET /api/v1/doctors/specialties."""

    # TODO: test_specialties_returns_distinct_list
    # TODO: test_specialties_count_matches_seed_data


@pytest.mark.integration
class TestDoctorWriteAPI:
    """POST / PUT — admin-only."""

    # TODO: test_create_doctor_as_admin_returns_201
    # TODO: test_create_doctor_without_auth_returns_401
    # TODO: test_update_doctor_as_admin_returns_200
