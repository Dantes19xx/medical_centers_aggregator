/**
 * E2E tests for the Appointment wizard — AppointmentForm component.
 *
 * This is a CRITICAL PATH test (qa_engineer.md — 100 % E2E coverage required).
 *
 * Wizard steps (frontend_developer.md — AppointmentForm):
 *   Step 1: Select clinic (if not pre-selected)
 *   Step 2: Select doctor / service
 *   Step 3: Select date (calendar) + time slot
 *   Step 4: Patient details (name, phone, email, note)
 *   Step 5: Confirmation screen with appointment number
 *
 * Validation rules (frontend_developer.md):
 *   - patient_phone: Kazakhstan format  +7 (XXX) XXX-XX-XX
 *   - patient_email: valid email
 *   - patient_name: min 2 chars
 *   - appointment_date: must not be in the past
 *
 * API calls:
 *   POST /api/v1/appointments
 *
 * data-testid values must match AppointmentForm.tsx, TimeSlotPicker.tsx:
 *   "btn-book", "doctor-option", "btn-next", "calendar-day",
 *   "time-slot", "btn-submit", "success-message", "appointment-number",
 *   "error-phone", "error-email", "error-name"
 *
 * TODO: implement tests once frontend/src/components/appointment/AppointmentForm.tsx exists.
 */

import { test } from "@playwright/test";

test.describe("Appointment booking wizard — happy path", () => {
  test.skip("test_full_booking_flow_completes_and_shows_confirmation", async () => {});
  test.skip("test_confirmation_screen_shows_appointment_number", async () => {});
  test.skip("test_add_to_calendar_button_visible_after_success", async () => {});
});

test.describe("Appointment booking wizard — validation", () => {
  test.skip("test_invalid_phone_format_shows_error_message", async () => {});
  test.skip("test_invalid_email_shows_error_message", async () => {});
  test.skip("test_name_too_short_shows_error_message", async () => {});
  test.skip("test_past_date_not_selectable_in_calendar", async () => {});
  test.skip("test_cannot_proceed_without_selecting_time_slot", async () => {});
});

test.describe("Appointment booking wizard — navigation", () => {
  test.skip("test_back_button_returns_to_previous_step", async () => {});
  test.skip("test_progress_indicator_updates_per_step", async () => {});
});
