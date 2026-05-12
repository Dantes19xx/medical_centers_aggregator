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

import { test, expect } from "@playwright/test";

test.describe("Chatbot widget", () => {
  // TODO: test_toggle_button_visible_on_all_pages
  // TODO: test_click_toggle_opens_chat_window
  // TODO: test_click_toggle_again_closes_chat_window
  // TODO: test_pre_set_suggestions_visible_on_open
  // TODO: test_clicking_suggestion_sends_user_message
  // TODO: test_typing_message_and_pressing_enter_sends_it
  // TODO: test_typing_indicator_appears_while_waiting
  // TODO: test_bot_message_appears_after_response
  // TODO: test_bot_response_may_include_suggestion_chips
  // TODO: test_bot_response_may_include_clinic_or_doctor_cards
});
