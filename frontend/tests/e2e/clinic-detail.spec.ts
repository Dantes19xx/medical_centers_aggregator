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

import { test } from "@playwright/test";

test.describe("Clinic detail page", () => {
  test.skip("test_page_renders_clinic_name_and_address", async () => {});
  test.skip("test_page_renders_rating_and_review_count", async () => {});
  test.skip("test_working_hours_displayed", async () => {});
  test.skip("test_phone_call_button_visible", async () => {});
  test.skip("test_tab_doctors_shows_doctor_cards", async () => {});
  test.skip("test_tab_services_shows_service_cards", async () => {});
  test.skip("test_tab_reviews_shows_review_list", async () => {});
  test.skip("test_tab_about_shows_description", async () => {});
  test.skip("test_book_button_anchors_to_appointment_form", async () => {});
  test.skip("test_nonexistent_clinic_id_shows_404", async () => {});
});
