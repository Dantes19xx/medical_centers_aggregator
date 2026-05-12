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

import { test, expect } from "@playwright/test";

test.describe("Doctors list page", () => {
  // TODO: test_page_loads_and_shows_doctor_cards
  // TODO: test_specialty_filter_narrows_results
  // TODO: test_price_slider_filters_by_max_price
  // TODO: test_doctor_card_shows_price_and_specialty
  // TODO: test_book_button_opens_appointment_flow
  // TODO: test_doctor_card_click_navigates_to_detail_page
});

test.describe("Doctor detail page", () => {
  // TODO: test_page_renders_doctor_name_and_specialty
  // TODO: test_experience_and_bio_displayed
  // TODO: test_available_slots_rendered_for_selected_date
  // TODO: test_appointment_form_embedded_on_page
  // TODO: test_reviews_section_visible
  // TODO: test_clinic_link_navigates_to_clinic_detail
});
