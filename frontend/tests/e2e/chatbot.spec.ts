/**
 * E2E tests for the ChatbotWidget — floating chat component.
 *
 * Widget behaviour (frontend_developer.md + ai_engineer.md):
 *   - Toggle button in bottom-right corner (always visible)
 *   - Click opens chat window
 *   - Pre-set quick-reply suggestions: "Найти клинику", "Записаться к врачу", "Узнать цены"
 *   - User message → POST /api/v1/chatbot/message → bot message + suggestion chips + cards
 *   - Typing indicator (three dots) while waiting for response
 *   - session_id stored in localStorage, conversation_history kept in component state (last 10)
 *
 * API calls:
 *   POST /api/v1/chatbot/message
 *
 * data-testid values must match ChatbotWidget.tsx:
 *   "chatbot-toggle", "chatbot-window", "chatbot-input",
 *   "user-message", "bot-message", "suggestion-btn", "typing-indicator"
 *
 * NOTE: these tests call the real backend chatbot endpoint. To avoid flaky
 * tests due to LLM non-determinism, only assert on *structure* (message
 * appears, suggestion chips render) — not on exact text content.
 *
 * TODO: implement tests once frontend/src/components/chatbot/ChatbotWidget.tsx exists.
 */

import { test } from "@playwright/test";

test.describe("Chatbot widget", () => {
  test.skip("test_toggle_button_visible_on_all_pages", async () => {});
  test.skip("test_click_toggle_opens_chat_window", async () => {});
  test.skip("test_click_toggle_again_closes_chat_window", async () => {});
  test.skip("test_pre_set_suggestions_visible_on_open", async () => {});
  test.skip("test_clicking_suggestion_sends_user_message", async () => {});
  test.skip("test_typing_message_and_pressing_enter_sends_it", async () => {});
  test.skip("test_typing_indicator_appears_while_waiting", async () => {});
  test.skip("test_bot_message_appears_after_response", async () => {});
  test.skip("test_bot_response_may_include_suggestion_chips", async () => {});
  test.skip("test_bot_response_may_include_clinic_or_doctor_cards", async () => {});
});
