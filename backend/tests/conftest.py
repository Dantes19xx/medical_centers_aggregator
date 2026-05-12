"""
Shared pytest fixtures for the medical-clinic-aggregator backend.

Fixture hierarchy (outermost → innermost):
  setup_db (session-scope)
    └── db (function-scope)           — isolated SQLAlchemy session per test
          ├── client (function-scope) — unauthenticated FastAPI TestClient
          ├── auth_client             — client with Bearer token (patient role)
          └── admin_client            — client with Bearer token (admin role)

Factory fixtures (e.g. clinic_factory, doctor_factory) are defined in
factories.py and wired to the per-test `db` session inside `setup_factories`.

TODO (backend_developer): implement backend/app/ before these imports resolve.
  Required modules:
    - app.main          → FastAPI app instance
    - app.database      → Base, get_db
    - app.models.*      → ORM models (Clinic, Doctor, Service, Appointment, Review, User)
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------------
# Database URL — mirrors devops_engineer CI config (backend-ci.yml)
# Override via env var TEST_DATABASE_URL for local dev
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://testuser:testpass@localhost:5432/medical_test",
)

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# TODO: uncomment once backend/app/ exists
# from app.main import app
# from app.database import Base, get_db
# from tests.factories import (
#     ClinicFactory, DoctorFactory, ServiceFactory,
#     AppointmentFactory, ReviewFactory, UserFactory,
# )
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create all tables once per test session, drop them on teardown."""
    # TODO: replace placeholder with real Base once models are implemented
    # Base.metadata.create_all(bind=engine)
    # yield
    # Base.metadata.drop_all(bind=engine)
    yield  # no-op until app.database.Base is available


@pytest.fixture(scope="function")
def db():
    """
    Per-test database session.
    Rolls back all changes after each test for isolation.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db):
    """
    Unauthenticated FastAPI TestClient wired to the per-test DB session.

    The `get_db` dependency is overridden so every request in this test uses
    the same session as the `db` fixture — changes are visible across both.

    TODO: uncomment once app.main and app.database exist.
    """
    # from fastapi.testclient import TestClient

    # def override_get_db():
    #     yield db

    # app.dependency_overrides[get_db] = override_get_db
    # with TestClient(app) as c:
    #     yield c
    # app.dependency_overrides.clear()

    raise NotImplementedError(
        "`client` fixture requires backend/app/ — implement app.main first."
    )


@pytest.fixture(scope="function")
def auth_client(client, db):
    """
    TestClient authenticated as a regular patient user.

    Registers a fresh user per test so email uniqueness is guaranteed.
    The auth endpoints used here are defined in backend_developer.md:
      POST /api/v1/auth/register
      POST /api/v1/auth/login
    """
    reg_payload = {
        "email": "testpatient@medfind.test",
        "password": "Testpass_123",
        "full_name": "Test Patient",
    }
    client.post("/api/v1/auth/register", json=reg_payload)

    login_resp = client.post(
        "/api/v1/auth/login",
        data={
            "username": reg_payload["email"],
            "password": reg_payload["password"],
        },
    )
    token = login_resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture(scope="function")
def admin_client(client, db):
    """
    TestClient authenticated as an admin user (role='admin').

    TODO: implement once the User model supports role assignment and
    the backend exposes an admin-seeding utility or migration fixture.
    """
    raise NotImplementedError(
        "`admin_client` fixture — implement after User.role and auth are done."
    )


# ---------------------------------------------------------------------------
# Factory fixtures
# Each factory is scoped per-function and receives the per-test db session.
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function", autouse=False)
def setup_factories(db):
    """
    Wire all factory_boy factories to the current test's DB session.

    Called automatically only when a test requests a specific factory fixture
    (e.g. `clinic_factory`). autouse=False avoids the session overhead for
    tests that don't create any model instances.

    TODO: uncomment the factory imports in factories.py once models exist.
    """
    # ClinicFactory._meta.sqlalchemy_session = db
    # DoctorFactory._meta.sqlalchemy_session = db
    # ServiceFactory._meta.sqlalchemy_session = db
    # AppointmentFactory._meta.sqlalchemy_session = db
    # ReviewFactory._meta.sqlalchemy_session = db
    # UserFactory._meta.sqlalchemy_session = db
    yield


@pytest.fixture
def clinic_factory(setup_factories):
    """Returns the ClinicFactory class, session-wired."""
    # TODO: from tests.factories import ClinicFactory; return ClinicFactory
    raise NotImplementedError("Requires app.models.clinic")


@pytest.fixture
def doctor_factory(setup_factories):
    """Returns the DoctorFactory class, session-wired."""
    # TODO: from tests.factories import DoctorFactory; return DoctorFactory
    raise NotImplementedError("Requires app.models.doctor")


@pytest.fixture
def service_factory(setup_factories):
    """Returns the ServiceFactory class, session-wired."""
    # TODO: from tests.factories import ServiceFactory; return ServiceFactory
    raise NotImplementedError("Requires app.models.service")


@pytest.fixture
def appointment_factory(setup_factories):
    """Returns the AppointmentFactory class, session-wired."""
    # TODO: from tests.factories import AppointmentFactory; return AppointmentFactory
    raise NotImplementedError("Requires app.models.appointment")


@pytest.fixture
def review_factory(setup_factories):
    """Returns the ReviewFactory class, session-wired."""
    # TODO: from tests.factories import ReviewFactory; return ReviewFactory
    raise NotImplementedError("Requires app.models.review")


@pytest.fixture
def user_factory(setup_factories):
    """Returns the UserFactory class, session-wired."""
    # TODO: from tests.factories import UserFactory; return UserFactory
    raise NotImplementedError("Requires app.models.user")
