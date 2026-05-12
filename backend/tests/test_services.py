"""
Tests for /api/v1/services endpoints.

Endpoints (backend_developer.md):
  GET /api/v1/services             — list (filters: clinic_id, category, price_max)
  GET /api/v1/services/{id}        — service detail
  GET /api/v1/services/categories  — distinct category list

TODO: implement test methods once backend/app/routers/services.py is done.
"""

import pytest


@pytest.mark.integration
class TestServicesListAPI:
    """GET /api/v1/services — list and filters."""

    # TODO: test_get_services_returns_paginated_response
    # TODO: test_get_services_filter_by_clinic_id
    # TODO: test_get_services_filter_by_category
    # TODO: test_get_services_filter_by_max_price
    # TODO: test_get_services_only_available_by_default


@pytest.mark.integration
class TestServiceDetailAPI:
    """GET /api/v1/services/{id}."""

    # TODO: test_get_service_by_id_returns_correct_fields
    # TODO: test_get_service_not_found_returns_404


@pytest.mark.integration
class TestServiceCategoriesAPI:
    """GET /api/v1/services/categories."""

    # TODO: test_categories_returns_list_of_strings
    # TODO: test_categories_matches_known_values
