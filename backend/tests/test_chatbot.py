"""
Tests for POST /api/v1/chatbot/message — AI chatbot endpoint.

Endpoint spec (ai_engineer.md):
  POST /api/v1/chatbot/message

  Request:
    {
      "message": str,
      "session_id": str (UUID),
      "conversation_history": [{"role": "user"|"assistant", "content": str}]
    }

  Response:
    {
      "response": str,
      "session_id": str,
      "suggestions": [str],
      "cards": [{"type": str, "id": int, "name": str, ...}]
    }

Intents handled (ai_engineer.md):
  find_clinic, find_doctor, find_service, book_appointment,
  price_inquiry, working_hours, general_question, greeting

NOTE: tests against the live Anthropic API must be gated behind an env var
(e.g. ANTHROPIC_API_KEY) and skipped in CI if the key is absent, to avoid
flakiness and accidental billing. The chatbot router should also accept a
mock/stub mode for unit-level testing without real API calls.

TODO: implement test methods once backend/app/routers/chatbot.py and
      backend/app/services/chatbot_service.py are done.
"""

import os
import pytest

# Skip live API tests when key is not present in the environment
requires_anthropic = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set — skipping live chatbot tests",
)


@pytest.mark.integration
class TestChatbotEndpointStructure:
    """Validate response shape regardless of AI content."""

    # TODO: test_message_returns_required_fields (response, session_id, suggestions, cards)
    # TODO: test_missing_message_field_returns_422
    # TODO: test_empty_message_returns_422
    # TODO: test_session_id_echoed_in_response
    # TODO: test_suggestions_is_list_of_strings
    # TODO: test_cards_is_list


@pytest.mark.integration
@requires_anthropic
class TestChatbotIntentHandling:
    """Validate intent-specific behaviour (requires ANTHROPIC_API_KEY)."""

    # TODO: test_greeting_intent_returns_non_empty_response
    # TODO: test_find_doctor_intent_returns_doctor_cards
    # TODO: test_find_clinic_intent_returns_clinic_cards
    # TODO: test_price_inquiry_returns_price_suggestions
    # TODO: test_book_appointment_returns_booking_suggestion


@pytest.mark.integration
class TestChatbotSecurity:
    """Guard against prompt-injection and abuse (ai_engineer.md requirement)."""

    # TODO: test_prompt_injection_attempt_does_not_leak_system_prompt
    # TODO: test_medical_diagnosis_request_returns_disclaimer
