"""
Tests for /api/v1/appointments — the critical booking path.

Endpoints (backend_developer.md):
  POST  /api/v1/appointments               — create booking (auth optional)
  GET   /api/v1/appointments               — list user's bookings (auth required)
  GET   /api/v1/appointments/{id}          — booking detail
  PATCH /api/v1/appointments/{id}/cancel   — cancel booking

Validation rules (frontend_developer.md):
  - patient_phone: Kazakhstan format +7 (XXX) XXX-XX-XX
  - patient_email: valid email
  - patient_name: min 2 chars
  - appointment_date: must not be in the past

Coverage target: 100 % of this module (critical path — qa_engineer.md).

TODO: implement test methods once backend/app/routers/appointments.py is done.
"""

import pytest


@pytest.mark.integration
class TestCreateAppointmentAPI:
    """POST /api/v1/appointments — happy path and validation."""

    # TODO: test_create_appointment_success_returns_201_with_pending_status
    # TODO: test_create_appointment_invalid_phone_returns_422
    # TODO: test_create_appointment_invalid_email_returns_422
    # TODO: test_create_appointment_past_date_returns_422
    # TODO: test_create_appointment_missing_required_field_returns_422
    # TODO: test_create_appointment_nonexistent_doctor_returns_404
    # TODO: test_create_appointment_nonexistent_clinic_returns_404
    # TODO: test_create_appointment_unauthenticated_succeeds  # auth is optional


@pytest.mark.integration
class TestListAppointmentsAPI:
    """GET /api/v1/appointments — auth-gated user list."""

    # TODO: test_list_appointments_requires_auth
    # TODO: test_list_appointments_returns_only_own_records
    # TODO: test_list_appointments_paginated


@pytest.mark.integration
class TestCancelAppointmentAPI:
    """PATCH /api/v1/appointments/{id}/cancel."""

    # TODO: test_cancel_own_appointment_returns_200_with_cancelled_status
    # TODO: test_cancel_already_cancelled_appointment_returns_400
    # TODO: test_cancel_other_users_appointment_returns_403
    # TODO: test_cancel_nonexistent_appointment_returns_404
