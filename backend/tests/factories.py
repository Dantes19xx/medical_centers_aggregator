"""
factory_boy factories for all SQLAlchemy models defined in backend_developer.md.

Models covered (6 total):
  Clinic · Doctor · Service · Appointment · Review · User

Usage (after backend/app/models/ is implemented):
  1. Uncomment the model imports below.
  2. In conftest.py, set each factory's sqlalchemy_session inside setup_factories().
  3. In tests, request the factory fixture and call Factory.create() or Factory.build().

Example:
  def test_clinic_detail(client, db, clinic_factory):
      clinic = clinic_factory.create()
      response = client.get(f"/api/v1/clinics/{clinic.id}")
      assert response.status_code == 200

Faker locale is set to ru_RU to produce realistic Almaty-specific seed data
(names, addresses, phone numbers).
"""

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

fake = Faker("ru_RU")

# ---------------------------------------------------------------------------
# TODO (backend_developer): uncomment once app/models/ is implemented
# from app.models.clinic import Clinic
# from app.models.doctor import Doctor
# from app.models.service import Service
# from app.models.appointment import Appointment
# from app.models.review import Review
# from app.models.user import User
# ---------------------------------------------------------------------------

# Almaty districts defined in frontend_developer.md filter spec
_ALMATY_DISTRICTS = [
    "Алмалинский",
    "Бостандыкский",
    "Медеуский",
    "Ауэзовский",
    "Жетысуский",
    "Турксибский",
    "Наурызбайский",
]

# Specialties from backend_developer.md seed data spec
_SPECIALTIES = [
    "Терапевт",
    "Кардиолог",
    "Невролог",
    "Педиатр",
    "Хирург",
    "Офтальмолог",
    "Дерматолог",
    "Гинеколог",
    "Ортопед",
    "Стоматолог",
]

# Service categories from frontend_developer.md tabs
_SERVICE_CATEGORIES = ["Диагностика", "Консультации", "Анализы", "Процедуры"]

# Appointment status enum from backend_developer.md
_APPOINTMENT_STATUSES = ["pending", "confirmed", "cancelled", "completed"]

# Time slots that the backend /slots endpoint is expected to return
_TIME_SLOTS = ["09:00", "09:30", "10:00", "10:30", "11:00", "14:00", "14:30", "15:00", "15:30", "16:00"]


class UserFactory(SQLAlchemyModelFactory):
    """
    Represents the User model.

    Fields (backend_developer.md):
      id, email, hashed_password, full_name, phone,
      role (patient|admin), is_active, created_at
    """

    class Meta:
        model = None  # TODO: replace with User
        sqlalchemy_session = None  # set per-test in conftest.setup_factories
        sqlalchemy_session_persistence = "commit"

    email = factory.Sequence(lambda n: f"user{n}@medfind.test")
    # In real tests use passlib to hash; plain string is fine for factories
    hashed_password = "$2b$12$placeholder_bcrypt_hash_replace_me"
    full_name = factory.LazyFunction(fake.name)
    phone = factory.LazyFunction(
        lambda: f"+7{fake.numerify('7#########')}"
    )
    role = "patient"
    is_active = True


class ClinicFactory(SQLAlchemyModelFactory):
    """
    Represents the Clinic model.

    Fields (backend_developer.md):
      id, name, description, address, city, district, phone, email,
      website, logo_url, photos, working_hours, rating, reviews_count,
      is_verified, created_at, updated_at
    """

    class Meta:
        model = None  # TODO: replace with Clinic
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    name = factory.Sequence(lambda n: f"Медицинский центр #{n}")
    description = factory.LazyFunction(fake.paragraph)
    address = factory.LazyFunction(fake.street_address)
    city = "Алматы"
    district = factory.Iterator(_ALMATY_DISTRICTS)
    phone = factory.LazyFunction(lambda: f"+7727{fake.numerify('######')}")
    email = factory.LazyAttribute(
        lambda o: f"info@{o.name.lower().replace(' ', '-').replace('#', '')}.kz"
    )
    website = factory.LazyAttribute(
        lambda o: f"https://{o.name.lower().replace(' ', '').replace('#', '')}.kz"
    )
    logo_url = factory.LazyAttribute(
        lambda o: f"https://cdn.medfind.kz/logos/{o.name.lower().replace(' ', '-')}.png"
    )
    photos = factory.LazyFunction(list)  # empty list; backend populates in seed
    # JSON field: {"monday": "08:00-20:00", ...}
    working_hours = factory.LazyFunction(
        lambda: {day: "08:00-20:00" for day in
                 ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]}
    )
    rating = factory.LazyFunction(lambda: round(fake.random.uniform(3.0, 5.0), 1))
    reviews_count = factory.LazyFunction(lambda: fake.random_int(0, 300))
    is_verified = True


class DoctorFactory(SQLAlchemyModelFactory):
    """
    Represents the Doctor model.

    Fields (backend_developer.md):
      id, clinic_id (FK→Clinic), first_name, last_name, patronymic,
      specialty, experience_years, education, bio, photo_url, rating,
      reviews_count, consultation_price, is_available, created_at

    Price range: 3 000–25 000 ₸ (backend seed spec)
    """

    class Meta:
        model = None  # TODO: replace with Doctor
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    clinic = factory.SubFactory(ClinicFactory)
    first_name = factory.LazyFunction(fake.first_name_male)
    last_name = factory.LazyFunction(fake.last_name_male)
    patronymic = factory.LazyFunction(fake.middle_name_male)
    specialty = factory.Iterator(_SPECIALTIES)
    experience_years = factory.LazyFunction(lambda: fake.random_int(1, 35))
    education = factory.LazyFunction(
        lambda: "Казахский национальный медицинский университет"
    )
    bio = factory.LazyFunction(fake.paragraph)
    photo_url = factory.Sequence(
        lambda n: f"https://cdn.medfind.kz/doctors/{n}.jpg"
    )
    rating = factory.LazyFunction(lambda: round(fake.random.uniform(3.5, 5.0), 1))
    reviews_count = factory.LazyFunction(lambda: fake.random_int(0, 150))
    consultation_price = factory.LazyFunction(
        lambda: fake.random_int(3, 25) * 1000
    )
    is_available = True


class ServiceFactory(SQLAlchemyModelFactory):
    """
    Represents the Service model.

    Fields (backend_developer.md):
      id, clinic_id (FK→Clinic), name, description, category,
      price_from, price_to, duration_minutes, is_available
    """

    class Meta:
        model = None  # TODO: replace with Service
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    clinic = factory.SubFactory(ClinicFactory)
    name = factory.Sequence(lambda n: f"Услуга #{n}")
    description = factory.LazyFunction(fake.sentence)
    category = factory.Iterator(_SERVICE_CATEGORIES)
    price_from = factory.LazyFunction(lambda: fake.random_int(1, 10) * 1000)
    price_to = factory.LazyAttribute(
        lambda o: o.price_from + fake.random_int(1, 5) * 1000
    )
    duration_minutes = factory.Iterator([15, 20, 30, 45, 60])
    is_available = True


class AppointmentFactory(SQLAlchemyModelFactory):
    """
    Represents the Appointment model.

    Fields (backend_developer.md):
      id, user_id (FK), doctor_id (FK), clinic_id (FK), service_id (FK, nullable),
      appointment_date, appointment_time,
      status (pending|confirmed|cancelled|completed),
      patient_name, patient_phone, patient_email, notes, created_at

    Default status is 'pending' — matches the POST /api/v1/appointments response spec.
    """

    class Meta:
        model = None  # TODO: replace with Appointment
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)
    doctor = factory.SubFactory(DoctorFactory)
    # clinic should match doctor.clinic; override explicitly in tests when needed
    clinic = factory.SubFactory(ClinicFactory)
    service = None  # nullable FK — set explicitly if testing service-linked appointments
    appointment_date = "2026-06-01"
    appointment_time = factory.Iterator(_TIME_SLOTS)
    status = "pending"
    patient_name = factory.LazyFunction(fake.name)
    patient_phone = factory.LazyFunction(
        lambda: f"+7700{fake.numerify('######')}"
    )
    patient_email = factory.LazyFunction(fake.email)
    notes = ""


class ReviewFactory(SQLAlchemyModelFactory):
    """
    Represents the Review model.

    Fields (backend_developer.md):
      id, user_id (FK), clinic_id (FK, nullable), doctor_id (FK, nullable),
      rating (1-5), comment, is_moderated, created_at

    By default the review is for a clinic. To create a doctor review:
      ReviewFactory.create(clinic=None, doctor=doctor_instance)
    """

    class Meta:
        model = None  # TODO: replace with Review
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    user = factory.SubFactory(UserFactory)
    clinic = factory.SubFactory(ClinicFactory)
    doctor = None  # nullable; override to test doctor reviews
    rating = factory.LazyFunction(lambda: fake.random_int(1, 5))
    comment = factory.LazyFunction(fake.paragraph)
    is_moderated = False
