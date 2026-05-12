/**
 * E2E tests for the Clinic detail page — /clinics/:id
 *
 * Tabs (frontend_developer.md):
 *   - Врачи      — DoctorCard list
 *   - Услуги     — ServiceCard list
 *   - Отзывы     — ReviewCard list + ReviewForm
 *   - О клинике  — description, photo gallery, map
 *
 * API calls:
 *   GET /api/v1/clinics/{id}
 *   GET /api/v1/clinics/{id}/doctors
 *   GET /api/v1/clinics/{id}/services
 *   GET /api/v1/clinics/{id}/reviews
 *
 * TODO: implement tests once frontend/src/pages/ClinicDetailPage.tsx exists.
 */

import { test, expect } from "@playwright/test";

test.describe("Clinic detail page", () => {
  // TODO: test_page_renders_clinic_name_and_address
  // TODO: test_page_renders_rating_and_review_count
  // TODO: test_working_hours_displayed
  // TODO: test_phone_call_button_visible
  // TODO: test_tab_doctors_shows_doctor_cards
  // TODO: test_tab_services_shows_service_cards
  // TODO: test_tab_reviews_shows_review_list
  // TODO: test_tab_about_shows_description
  // TODO: test_book_button_anchors_to_appointment_form
  // TODO: test_nonexistent_clinic_id_shows_404
});
