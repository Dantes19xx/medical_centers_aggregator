/**
 * E2E tests for the Doctors list page — /doctors
 * and the Doctor detail page — /doctors/:id
 *
 * Filters (frontend_developer.md):
 *   specialty (select), experience (min years), price (slider 0–30000 ₸),
 *   rating (stars), clinic (select)
 *
 * DoctorCard fields:
 *   photo, full name, specialty, experience, rating, reviews, price, clinic link, "Записаться" btn
 *
 * Doctor detail page:
 *   large photo, bio, schedule / available slots, inline AppointmentForm, reviews
 *
 * API calls:
 *   GET /api/v1/doctors                — list
 *   GET /api/v1/doctors/specialties    — specialty dropdown options
 *   GET /api/v1/doctors/{id}           — profile
 *   GET /api/v1/doctors/{id}/slots     — time slots
 *   GET /api/v1/doctors/{id}/reviews   — reviews
 *
 * TODO: implement tests once frontend/src/pages/DoctorsPage.tsx
 *       and frontend/src/pages/DoctorDetailPage.tsx exist.
 */

import { test } from "@playwright/test";

test.describe("Doctors list page", () => {
  test.skip("test_page_loads_and_shows_doctor_cards", async () => {});
  test.skip("test_specialty_filter_narrows_results", async () => {});
  test.skip("test_price_slider_filters_by_max_price", async () => {});
  test.skip("test_doctor_card_shows_price_and_specialty", async () => {});
  test.skip("test_book_button_opens_appointment_flow", async () => {});
  test.skip("test_doctor_card_click_navigates_to_detail_page", async () => {});
});

test.describe("Doctor detail page", () => {
  test.skip("test_page_renders_doctor_name_and_specialty", async () => {});
  test.skip("test_experience_and_bio_displayed", async () => {});
  test.skip("test_available_slots_rendered_for_selected_date", async () => {});
  test.skip("test_appointment_form_embedded_on_page", async () => {});
  test.skip("test_reviews_section_visible", async () => {});
  test.skip("test_clinic_link_navigates_to_clinic_detail", async () => {});
});
