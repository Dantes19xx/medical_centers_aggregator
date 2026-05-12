"""
Seed script for Medical Centers Aggregator.
Populates the database with realistic Almaty data.
Run: python seed.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.clinic import Clinic
from app.models.doctor import Doctor
from app.models.service import Service
from app.models.review import Review
from app.utils.auth import get_password_hash
import uuid
from datetime import datetime

db = SessionLocal()


def seed_users():
    existing = db.query(User).filter(User.email == "admin@medical.kz").first()
    if existing:
        print("Users already seeded, skipping.")
        return existing, []

    admin = User(
        id=uuid.uuid4(),
        email="admin@medical.kz",
        hashed_password=get_password_hash("admin123"),
        full_name="Администратор Системы",
        phone="+7 (727) 200-00-00",
        role=UserRole.admin,
        is_active=True,
    )
    db.add(admin)

    regular_users = [
        User(
            id=uuid.uuid4(),
            email="aizhan.bekova@gmail.com",
            hashed_password=get_password_hash("password123"),
            full_name="Айжан Бекова",
            phone="+7 (701) 234-56-78",
            role=UserRole.patient,
            is_active=True,
        ),
        User(
            id=uuid.uuid4(),
            email="dmitriy.kim@mail.ru",
            hashed_password=get_password_hash("password123"),
            full_name="Дмитрий Ким",
            phone="+7 (702) 345-67-89",
            role=UserRole.patient,
            is_active=True,
        ),
        User(
            id=uuid.uuid4(),
            email="gulnara.seitkali@yandex.kz",
            hashed_password=get_password_hash("password123"),
            full_name="Гульнара Сейткали",
            phone="+7 (705) 456-78-90",
            role=UserRole.patient,
            is_active=True,
        ),
    ]

    for u in regular_users:
        db.add(u)

    db.commit()
    print("Users seeded.")
    return admin, regular_users


def seed_clinics():
    existing = db.query(Clinic).first()
    if existing:
        print("Clinics already seeded, skipping.")
        return db.query(Clinic).all()

    working_hours_standard = {
        "mon": {"open": "09:00", "close": "18:00"},
        "tue": {"open": "09:00", "close": "18:00"},
        "wed": {"open": "09:00", "close": "18:00"},
        "thu": {"open": "09:00", "close": "18:00"},
        "fri": {"open": "09:00", "close": "18:00"},
        "sat": {"open": "10:00", "close": "16:00"},
        "sun": None,
    }

    working_hours_extended = {
        "mon": {"open": "08:00", "close": "20:00"},
        "tue": {"open": "08:00", "close": "20:00"},
        "wed": {"open": "08:00", "close": "20:00"},
        "thu": {"open": "08:00", "close": "20:00"},
        "fri": {"open": "08:00", "close": "20:00"},
        "sat": {"open": "09:00", "close": "18:00"},
        "sun": {"open": "10:00", "close": "15:00"},
    }

    working_hours_24h = {
        "mon": {"open": "00:00", "close": "23:30"},
        "tue": {"open": "00:00", "close": "23:30"},
        "wed": {"open": "00:00", "close": "23:30"},
        "thu": {"open": "00:00", "close": "23:30"},
        "fri": {"open": "00:00", "close": "23:30"},
        "sat": {"open": "00:00", "close": "23:30"},
        "sun": {"open": "00:00", "close": "23:30"},
    }

    clinics_data = [
        {
            "name": "Медицинский центр «Авиценна»",
            "description": "Многопрофильная частная клиника с современным оборудованием. Более 20 лет на рынке медицинских услуг Алматы. Квалифицированные специалисты, индивидуальный подход к каждому пациенту.",
            "address": "пр. Достык, 117/6",
            "city": "Алматы",
            "district": "Медеуский",
            "phone": "+7 (727) 311-22-33",
            "email": "info@avicenna.kz",
            "website": "https://avicenna.kz",
            "working_hours": working_hours_extended,
            "is_verified": True,
            "rating": 4.7,
            "reviews_count": 234,
        },
        {
            "name": "Клиника «Здоровье»",
            "description": "Государственная многопрофильная поликлиника Алмалинского района. Первичная медицинская помощь, диагностика и лечение широкого спектра заболеваний.",
            "address": "ул. Гоголя, 72",
            "city": "Алматы",
            "district": "Алмалинский",
            "phone": "+7 (727) 272-33-44",
            "email": "zdravoye@health.kz",
            "website": None,
            "working_hours": working_hours_standard,
            "is_verified": True,
            "rating": 3.9,
            "reviews_count": 156,
        },
        {
            "name": "Медицинский центр «Семейный доктор»",
            "description": "Семейная клиника полного цикла: от педиатрии до гериатрии. Индивидуальные программы здоровья для всей семьи. Современная диагностическая база.",
            "address": "мкр. Тастак-2, ул. Тулебаева, 14",
            "city": "Алматы",
            "district": "Алатауский",
            "phone": "+7 (727) 388-55-66",
            "email": "family@doctor.kz",
            "website": "https://familydoctor.kz",
            "working_hours": working_hours_extended,
            "is_verified": True,
            "rating": 4.5,
            "reviews_count": 189,
        },
        {
            "name": "Городская клиническая больница №1",
            "description": "Крупнейшая государственная многопрофильная больница Алматы. Стационарная и амбулаторная медицинская помощь, круглосуточное экстренное отделение.",
            "address": "ул. Байзакова, 280",
            "city": "Алматы",
            "district": "Бостандыкский",
            "phone": "+7 (727) 267-55-00",
            "email": "gkb1@almatyhospital.kz",
            "website": "https://gkb1.kz",
            "working_hours": working_hours_24h,
            "is_verified": True,
            "rating": 3.7,
            "reviews_count": 312,
        },
        {
            "name": "Стоматологическая клиника «Дент Люкс»",
            "description": "Современная стоматологическая клиника. Лечение зубов, ортодонтия, имплантация, эстетическая стоматология. Работаем с детьми и взрослыми.",
            "address": "пр. Аль-Фараби, 77/1",
            "city": "Алматы",
            "district": "Бостандыкский",
            "phone": "+7 (727) 311-44-55",
            "email": "dentlux@dent.kz",
            "website": "https://dentlux.kz",
            "working_hours": working_hours_standard,
            "is_verified": True,
            "rating": 4.8,
            "reviews_count": 421,
        },
        {
            "name": "Кардиологический центр «Жүрек»",
            "description": "Специализированный кардиологический центр. Диагностика и лечение заболеваний сердечно-сосудистой системы. Современное оборудование экспертного класса.",
            "address": "ул. Сейфуллина, 458",
            "city": "Алматы",
            "district": "Жетысуский",
            "phone": "+7 (727) 233-77-88",
            "email": "jurek@cardio.kz",
            "website": "https://jurek-cardio.kz",
            "working_hours": working_hours_extended,
            "is_verified": True,
            "rating": 4.6,
            "reviews_count": 178,
        },
        {
            "name": "Детская клиника «Балажан»",
            "description": "Специализированная детская медицинская клиника. Педиатрия, детская неврология, офтальмология, хирургия. Создаём комфортную атмосферу для маленьких пациентов.",
            "address": "мкр. Мамыр-4, дом 187",
            "city": "Алматы",
            "district": "Ауэзовский",
            "phone": "+7 (727) 399-11-22",
            "email": "balazhan@kids.kz",
            "website": "https://balazhan.kz",
            "working_hours": working_hours_standard,
            "is_verified": True,
            "rating": 4.9,
            "reviews_count": 267,
        },
        {
            "name": "Медицинский центр «Наурыз»",
            "description": "Многопрофильная клиника в Наурызбайском районе. Терапия, хирургия, гинекология, урология. Доступные цены, опытный персонал.",
            "address": "мкр. Акбулак, ул. Сыганак, 32",
            "city": "Алматы",
            "district": "Наурызбайский",
            "phone": "+7 (727) 244-66-77",
            "email": "nauryz@med.kz",
            "website": None,
            "working_hours": working_hours_standard,
            "is_verified": False,
            "rating": 4.1,
            "reviews_count": 89,
        },
        {
            "name": "Офтальмологическая клиника «Визус»",
            "description": "Специализированная офтальмологическая клиника. Диагностика и лечение заболеваний глаз, лазерная коррекция зрения, операции на катаракту.",
            "address": "пр. Райымбека, 212",
            "city": "Алматы",
            "district": "Турксибский",
            "phone": "+7 (727) 355-88-99",
            "email": "visus@eye.kz",
            "website": "https://visus.kz",
            "working_hours": working_hours_standard,
            "is_verified": True,
            "rating": 4.7,
            "reviews_count": 143,
        },
        {
            "name": "Медицинский центр «Асклепий»",
            "description": "Многопрофильная клиника с лабораторией. Консультации специалистов, УЗИ, ЭКГ, анализы. Запись онлайн и по телефону.",
            "address": "ул. Момышулы, 2/1",
            "city": "Алматы",
            "district": "Бостандыкский",
            "phone": "+7 (727) 322-00-11",
            "email": "asklepiy@med.kz",
            "website": "https://asklepiy.kz",
            "working_hours": working_hours_extended,
            "is_verified": True,
            "rating": 4.3,
            "reviews_count": 201,
        },
    ]

    clinics = []
    for data in clinics_data:
        clinic = Clinic(
            id=uuid.uuid4(),
            **data,
        )
        db.add(clinic)
        clinics.append(clinic)

    db.commit()
    print(f"Seeded {len(clinics)} clinics.")
    return clinics


def seed_doctors(clinics):
    existing = db.query(Doctor).first()
    if existing:
        print("Doctors already seeded, skipping.")
        return db.query(Doctor).all()

    clinic_map = {c.name: c for c in clinics}

    avicenna = clinic_map.get("Медицинский центр «Авиценна»")
    zdravoye = clinic_map.get("Клиника «Здоровье»")
    family = clinic_map.get("Медицинский центр «Семейный доктор»")
    gkb1 = clinic_map.get("Городская клиническая больница №1")
    dent = clinic_map.get("Стоматологическая клиника «Дент Люкс»")
    cardio = clinic_map.get("Кардиологический центр «Жүрек»")
    kids = clinic_map.get("Детская клиника «Балажан»")
    nauryz = clinic_map.get("Медицинский центр «Наурыз»")
    visus = clinic_map.get("Офтальмологическая клиника «Визус»")
    asklepiy = clinic_map.get("Медицинский центр «Асклепий»")

    doctors_data = [
        # Avicenna - терапевты, кардиолог, невролог
        {
            "clinic": avicenna,
            "first_name": "Айгуль",
            "last_name": "Нурланова",
            "patronymic": "Сериковна",
            "specialty": "терапевт",
            "experience_years": 15,
            "education": "Казахский национальный медицинский университет им. С.Д. Асфендиярова, 2008",
            "bio": "Врач-терапевт высшей категории. Специализируется на диагностике и лечении заболеваний внутренних органов, ведении пациентов с хроническими заболеваниями.",
            "consultation_price": 8000,
            "rating": 4.8,
            "reviews_count": 45,
        },
        {
            "clinic": avicenna,
            "first_name": "Серик",
            "last_name": "Джаксыбеков",
            "patronymic": "Маратович",
            "specialty": "кардиолог",
            "experience_years": 20,
            "education": "Алматинский государственный медицинский институт, 2003. Кардиология — стажировка в клинике Мюнхена, 2010.",
            "bio": "Кардиолог высшей категории, кандидат медицинских наук. Специализируется на диагностике и лечении ишемической болезни сердца, аритмий, сердечной недостаточности.",
            "consultation_price": 15000,
            "rating": 4.9,
            "reviews_count": 67,
        },
        {
            "clinic": avicenna,
            "first_name": "Мадина",
            "last_name": "Сейткалиева",
            "patronymic": "Бахытовна",
            "specialty": "невролог",
            "experience_years": 12,
            "education": "КазНМУ им. Асфендиярова, специальность «Неврология», 2011",
            "bio": "Невролог первой категории. Диагностика и лечение заболеваний нервной системы, головные боли, мигрени, остеохондроз, неврозы.",
            "consultation_price": 10000,
            "rating": 4.7,
            "reviews_count": 38,
        },
        # Zdravoye - терапевт, педиатр, гинеколог
        {
            "clinic": zdravoye,
            "first_name": "Болат",
            "last_name": "Искаков",
            "patronymic": "Ермекович",
            "specialty": "терапевт",
            "experience_years": 25,
            "education": "Казахский государственный медицинский институт, 1998",
            "bio": "Участковый терапевт с большим стажем работы. Ведение хронических больных, диспансеризация, консультативная помощь.",
            "consultation_price": 3500,
            "rating": 3.9,
            "reviews_count": 28,
        },
        {
            "clinic": zdravoye,
            "first_name": "Гульмира",
            "last_name": "Тастанбекова",
            "patronymic": "Нурлановна",
            "specialty": "педиатр",
            "experience_years": 18,
            "education": "КазНМУ им. Асфендиярова, педиатрический факультет, 2005",
            "bio": "Участковый педиатр, врач высшей категории. Ведение детей от рождения до 18 лет, профилактические осмотры, прививки.",
            "consultation_price": 4000,
            "rating": 4.2,
            "reviews_count": 51,
        },
        {
            "clinic": zdravoye,
            "first_name": "Жанна",
            "last_name": "Абенова",
            "patronymic": "Дауреновна",
            "specialty": "гинеколог",
            "experience_years": 14,
            "education": "Западно-Казахстанский государственный медицинский университет, 2009",
            "bio": "Акушер-гинеколог. Ведение беременности, лечение гинекологических заболеваний, плановые осмотры.",
            "consultation_price": 5000,
            "rating": 4.0,
            "reviews_count": 33,
        },
        # Family Doctor - терапевт, педиатр, ортопед
        {
            "clinic": family,
            "first_name": "Алибек",
            "last_name": "Дюсебаев",
            "patronymic": "Серикович",
            "specialty": "терапевт",
            "experience_years": 10,
            "education": "КазНМУ им. Асфендиярова, лечебное дело, 2013",
            "bio": "Семейный врач-терапевт. Диагностика и лечение острых и хронических заболеваний внутренних органов, диспансерное наблюдение.",
            "consultation_price": 7000,
            "rating": 4.5,
            "reviews_count": 42,
        },
        {
            "clinic": family,
            "first_name": "Светлана",
            "last_name": "Мороз",
            "patronymic": "Александровна",
            "specialty": "педиатр",
            "experience_years": 22,
            "education": "Алматинский государственный медицинский институт, педиатрия, 2001",
            "bio": "Педиатр высшей категории. Профилактика и лечение детских заболеваний, грудное вскармливание, нутрициология.",
            "consultation_price": 8000,
            "rating": 4.9,
            "reviews_count": 89,
        },
        {
            "clinic": family,
            "first_name": "Руслан",
            "last_name": "Байжанов",
            "patronymic": "Каиратович",
            "specialty": "ортопед",
            "experience_years": 8,
            "education": "КазНМУ им. Асфендиярова, хирургия, специализация «Ортопедия-травматология», 2015",
            "bio": "Ортопед-травматолог. Лечение заболеваний опорно-двигательного аппарата, суставов, позвоночника. Консервативное и оперативное лечение.",
            "consultation_price": 9000,
            "rating": 4.6,
            "reviews_count": 31,
        },
        # GKB1 - хирург, терапевт, невролог
        {
            "clinic": gkb1,
            "first_name": "Нурлан",
            "last_name": "Касымов",
            "patronymic": "Ержанович",
            "specialty": "хирург",
            "experience_years": 28,
            "education": "Казахский государственный медицинский институт, хирургия, 1995. Доктор медицинских наук.",
            "bio": "Хирург высшей категории, профессор. Абдоминальная хирургия, лапароскопические операции. Заведующий хирургическим отделением.",
            "consultation_price": 12000,
            "rating": 4.8,
            "reviews_count": 76,
        },
        {
            "clinic": gkb1,
            "first_name": "Лейла",
            "last_name": "Омарова",
            "patronymic": "Бейбитовна",
            "specialty": "терапевт",
            "experience_years": 16,
            "education": "КазНМУ им. Асфендиярова, 2007",
            "bio": "Врач-терапевт первой категории. Терапия внутренних заболеваний, ведение коморбидных пациентов.",
            "consultation_price": 5000,
            "rating": 4.1,
            "reviews_count": 29,
        },
        {
            "clinic": gkb1,
            "first_name": "Анатолий",
            "last_name": "Волков",
            "patronymic": "Игоревич",
            "specialty": "невролог",
            "experience_years": 30,
            "education": "Алматинский государственный медицинский институт, неврология, 1993. Кандидат медицинских наук.",
            "bio": "Невролог высшей категории. Эпилепсия, инсульт, нейродегенеративные заболевания, нейрореабилитация.",
            "consultation_price": 14000,
            "rating": 4.7,
            "reviews_count": 54,
        },
        # Dent Lux - стоматологи
        {
            "clinic": dent,
            "first_name": "Дина",
            "last_name": "Ахметова",
            "patronymic": "Маратовна",
            "specialty": "стоматолог",
            "experience_years": 13,
            "education": "КазНМУ им. Асфендиярова, стоматологический факультет, 2010",
            "bio": "Врач-стоматолог-терапевт. Лечение кариеса, эндодонтия, реставрация зубов, отбеливание. Работает с системой Cerec.",
            "consultation_price": 5000,
            "rating": 4.9,
            "reviews_count": 112,
        },
        {
            "clinic": dent,
            "first_name": "Максим",
            "last_name": "Петренко",
            "patronymic": "Олегович",
            "specialty": "стоматолог",
            "experience_years": 17,
            "education": "Алматинский государственный медицинский институт, стоматология, 2006. Специализация «Ортопедическая стоматология».",
            "bio": "Стоматолог-ортопед. Протезирование зубов, имплантация, виниры, коронки, мостовидные протезы.",
            "consultation_price": 7000,
            "rating": 4.8,
            "reviews_count": 98,
        },
        {
            "clinic": dent,
            "first_name": "Камила",
            "last_name": "Байсеитова",
            "patronymic": "Алибековна",
            "specialty": "стоматолог",
            "experience_years": 7,
            "education": "КазНМУ им. Асфендиярова, стоматология, 2016. Ортодонтия.",
            "bio": "Стоматолог-ортодонт. Исправление прикуса, брекеты, элайнеры, ретейнеры. Работает с детьми и взрослыми.",
            "consultation_price": 8000,
            "rating": 4.7,
            "reviews_count": 65,
        },
        # Cardio Center - кардиологи
        {
            "clinic": cardio,
            "first_name": "Кайрат",
            "last_name": "Алтынбеков",
            "patronymic": "Сейтжанович",
            "specialty": "кардиолог",
            "experience_years": 22,
            "education": "КазНМУ им. Асфендиярова, кардиология, 2001. Стажировка в Германии (кардиохирургия), 2008.",
            "bio": "Кардиолог высшей категории, доктор медицинских наук. Интервенционная кардиология, стентирование, коронарография.",
            "consultation_price": 20000,
            "rating": 4.9,
            "reviews_count": 87,
        },
        {
            "clinic": cardio,
            "first_name": "Татьяна",
            "last_name": "Сидорова",
            "patronymic": "Николаевна",
            "specialty": "кардиолог",
            "experience_years": 18,
            "education": "Алматинский государственный медицинский институт, 2005. Функциональная диагностика.",
            "bio": "Кардиолог-аритмолог. Диагностика и лечение нарушений ритма сердца, имплантация кардиостимуляторов.",
            "consultation_price": 18000,
            "rating": 4.8,
            "reviews_count": 63,
        },
        # Kids Clinic - педиатры, детский невролог
        {
            "clinic": kids,
            "first_name": "Зарина",
            "last_name": "Жунусова",
            "patronymic": "Маратовна",
            "specialty": "педиатр",
            "experience_years": 19,
            "education": "КазНМУ им. Асфендиярова, педиатрия, 2004",
            "bio": "Педиатр высшей категории. Неонатология, лечение детских болезней, аллергология, иммунология.",
            "consultation_price": 9000,
            "rating": 4.9,
            "reviews_count": 134,
        },
        {
            "clinic": kids,
            "first_name": "Марат",
            "last_name": "Кенжебеков",
            "patronymic": "Асланович",
            "specialty": "педиатр",
            "experience_years": 11,
            "education": "КазНМУ им. Асфендиярова, педиатрия, 2012",
            "bio": "Педиатр первой категории. Вакцинация, профилактические осмотры, ОРЗ и ОРВИ, кишечные инфекции.",
            "consultation_price": 7000,
            "rating": 4.7,
            "reviews_count": 78,
        },
        {
            "clinic": kids,
            "first_name": "Ирина",
            "last_name": "Чернова",
            "patronymic": "Васильевна",
            "specialty": "невролог",
            "experience_years": 24,
            "education": "Алматинский государственный медицинский институт, детская неврология, 1999",
            "bio": "Детский невролог высшей категории. ДЦП, эпилепсия, задержка развития, головные боли у детей.",
            "consultation_price": 12000,
            "rating": 4.9,
            "reviews_count": 92,
        },
        # Nauryz - терапевт, гинеколог, хирург
        {
            "clinic": nauryz,
            "first_name": "Асем",
            "last_name": "Каирбекова",
            "patronymic": "Бауыржановна",
            "specialty": "терапевт",
            "experience_years": 9,
            "education": "КазНМУ им. Асфендиярова, 2014",
            "bio": "Терапевт, ведение хронических больных, ЭКГ-диагностика, консультативная помощь.",
            "consultation_price": 4500,
            "rating": 4.1,
            "reviews_count": 21,
        },
        {
            "clinic": nauryz,
            "first_name": "Динара",
            "last_name": "Смагулова",
            "patronymic": "Ерлановна",
            "specialty": "гинеколог",
            "experience_years": 16,
            "education": "КазНМУ им. Асфендиярова, акушерство и гинекология, 2007",
            "bio": "Акушер-гинеколог первой категории. Ведение беременности, кольпоскопия, ультразвуковое исследование.",
            "consultation_price": 6000,
            "rating": 4.3,
            "reviews_count": 37,
        },
        {
            "clinic": nauryz,
            "first_name": "Азамат",
            "last_name": "Суюндыков",
            "patronymic": "Куанышевич",
            "specialty": "хирург",
            "experience_years": 13,
            "education": "КазНМУ им. Асфендиярова, хирургия, 2010",
            "bio": "Хирург первой категории. Плановая и экстренная хирургия, малоинвазивные операции.",
            "consultation_price": 8000,
            "rating": 4.2,
            "reviews_count": 19,
        },
        # Visus - офтальмологи
        {
            "clinic": visus,
            "first_name": "Гульсим",
            "last_name": "Ергалиева",
            "patronymic": "Нуровна",
            "specialty": "офтальмолог",
            "experience_years": 21,
            "education": "КазНМУ им. Асфендиярова, офтальмология, 2002. Лазерная микрохирургия глаза.",
            "bio": "Офтальмолог высшей категории. Лазерная коррекция зрения LASIK, лечение катаракты, глаукомы, диабетической ретинопатии.",
            "consultation_price": 12000,
            "rating": 4.8,
            "reviews_count": 76,
        },
        {
            "clinic": visus,
            "first_name": "Вячеслав",
            "last_name": "Иванченко",
            "patronymic": "Сергеевич",
            "specialty": "офтальмолог",
            "experience_years": 14,
            "education": "Алматинский государственный медицинский институт, офтальмология, 2009. Детская офтальмология.",
            "bio": "Офтальмолог-хирург. Детская и взрослая офтальмология, косоглазие, амблиопия, подбор очков и контактных линз.",
            "consultation_price": 10000,
            "rating": 4.7,
            "reviews_count": 58,
        },
        # Asklepiy - дерматолог, терапевт, ортопед
        {
            "clinic": asklepiy,
            "first_name": "Наталья",
            "last_name": "Берикова",
            "patronymic": "Аскаровна",
            "specialty": "дерматолог",
            "experience_years": 16,
            "education": "КазНМУ им. Асфендиярова, дерматовенерология, 2007",
            "bio": "Дерматолог-косметолог первой категории. Акне, псориаз, экзема, дерматиты, косметологические процедуры.",
            "consultation_price": 9000,
            "rating": 4.6,
            "reviews_count": 84,
        },
        {
            "clinic": asklepiy,
            "first_name": "Нурсулу",
            "last_name": "Байжанова",
            "patronymic": "Ахметовна",
            "specialty": "терапевт",
            "experience_years": 11,
            "education": "КазНМУ им. Асфендиярова, лечебное дело, 2012",
            "bio": "Терапевт первой категории. Ведение пациентов с сердечно-сосудистыми заболеваниями, диабетом, патологиями ЖКТ.",
            "consultation_price": 7500,
            "rating": 4.4,
            "reviews_count": 47,
        },
        {
            "clinic": asklepiy,
            "first_name": "Константин",
            "last_name": "Заиченко",
            "patronymic": "Павлович",
            "specialty": "ортопед",
            "experience_years": 19,
            "education": "Алматинский государственный медицинский институт, травматология и ортопедия, 2004",
            "bio": "Ортопед-травматолог высшей категории. Эндопротезирование суставов, лечение переломов, спортивная травматология.",
            "consultation_price": 11000,
            "rating": 4.7,
            "reviews_count": 61,
        },
        # Extra doctors for variety
        {
            "clinic": gkb1,
            "first_name": "Аскар",
            "last_name": "Жумагалиев",
            "patronymic": "Темирланович",
            "specialty": "хирург",
            "experience_years": 20,
            "education": "КазНМУ им. Асфендиярова, хирургия, 2003",
            "bio": "Торакальный хирург. Операции на органах грудной клетки, лёгких, плевры. Эндоскопическая хирургия.",
            "consultation_price": 13000,
            "rating": 4.8,
            "reviews_count": 43,
        },
        {
            "clinic": avicenna,
            "first_name": "Аружан",
            "last_name": "Тлеубергенова",
            "patronymic": "Бахытжановна",
            "specialty": "дерматолог",
            "experience_years": 8,
            "education": "КазНМУ им. Асфендиярова, дерматовенерология, 2015",
            "bio": "Дерматолог. Диагностика и лечение кожных заболеваний, аллергодерматозы, онкодерматология.",
            "consultation_price": 9500,
            "rating": 4.5,
            "reviews_count": 32,
        },
        {
            "clinic": family,
            "first_name": "Ерлан",
            "last_name": "Сатыбалдин",
            "patronymic": "Маратович",
            "specialty": "гинеколог",
            "experience_years": 17,
            "education": "КазНМУ им. Асфендиярова, акушерство и гинекология, 2006",
            "bio": "Акушер-гинеколог высшей категории. Лапароскопическая гинекология, эндометриоз, миома матки.",
            "consultation_price": 12000,
            "rating": 4.6,
            "reviews_count": 55,
        },
    ]

    doctors = []
    for data in doctors_data:
        clinic = data.pop("clinic")
        if clinic is None:
            continue
        doctor = Doctor(
            id=uuid.uuid4(),
            clinic_id=clinic.id,
            is_available=True,
            **data,
        )
        db.add(doctor)
        doctors.append(doctor)

    db.commit()
    print(f"Seeded {len(doctors)} doctors.")
    return doctors


def seed_services(clinics):
    existing = db.query(Service).first()
    if existing:
        print("Services already seeded, skipping.")
        return

    clinic_map = {c.name: c for c in clinics}
    avicenna = clinic_map["Медицинский центр «Авиценна»"]
    zdravoye = clinic_map["Клиника «Здоровье»"]
    family = clinic_map["Медицинский центр «Семейный доктор»"]
    gkb1 = clinic_map["Городская клиническая больница №1"]
    dent = clinic_map["Стоматологическая клиника «Дент Люкс»"]
    cardio = clinic_map["Кардиологический центр «Жүрек»"]
    kids = clinic_map["Детская клиника «Балажан»"]
    nauryz = clinic_map["Медицинский центр «Наурыз»"]
    visus = clinic_map["Офтальмологическая клиника «Визус»"]
    asklepiy = clinic_map["Медицинский центр «Асклепий»"]

    services_data = [
        # Avicenna
        {"clinic": avicenna, "name": "Консультация терапевта", "category": "Терапия", "price_from": 8000, "price_to": 10000, "duration_minutes": 30},
        {"clinic": avicenna, "name": "Консультация кардиолога", "category": "Кардиология", "price_from": 15000, "price_to": 20000, "duration_minutes": 45},
        {"clinic": avicenna, "name": "ЭКГ с расшифровкой", "category": "Диагностика", "price_from": 5000, "price_to": 6000, "duration_minutes": 20},
        {"clinic": avicenna, "name": "УЗИ органов брюшной полости", "category": "Диагностика", "price_from": 7000, "price_to": 9000, "duration_minutes": 30},
        {"clinic": avicenna, "name": "Консультация невролога", "category": "Неврология", "price_from": 10000, "price_to": 12000, "duration_minutes": 40},
        {"clinic": avicenna, "name": "Общий анализ крови", "category": "Диагностика", "price_from": 2000, "price_to": 2500, "duration_minutes": 10},

        # Zdravoye
        {"clinic": zdravoye, "name": "Прием терапевта (участковый)", "category": "Терапия", "price_from": 2500, "price_to": 3500, "duration_minutes": 20},
        {"clinic": zdravoye, "name": "Консультация педиатра", "category": "Педиатрия", "price_from": 3500, "price_to": 4000, "duration_minutes": 25},
        {"clinic": zdravoye, "name": "Консультация гинеколога", "category": "Гинекология", "price_from": 4500, "price_to": 5000, "duration_minutes": 30},
        {"clinic": zdravoye, "name": "Измерение давления и ЭКГ", "category": "Диагностика", "price_from": 1500, "price_to": 2000, "duration_minutes": 15},

        # Family Doctor
        {"clinic": family, "name": "Комплексный осмотр семейного врача", "category": "Терапия", "price_from": 10000, "price_to": 15000, "duration_minutes": 60},
        {"clinic": family, "name": "Педиатрический осмотр ребенка", "category": "Педиатрия", "price_from": 7000, "price_to": 9000, "duration_minutes": 40},
        {"clinic": family, "name": "Консультация ортопеда", "category": "Хирургия", "price_from": 8000, "price_to": 10000, "duration_minutes": 35},
        {"clinic": family, "name": "УЗИ суставов", "category": "Диагностика", "price_from": 6000, "price_to": 8000, "duration_minutes": 25},
        {"clinic": family, "name": "Программа «Здоровая семья» (базовый)", "category": "Диагностика", "price_from": 25000, "price_to": 35000, "duration_minutes": 120},

        # GKB1
        {"clinic": gkb1, "name": "Консультация хирурга", "category": "Хирургия", "price_from": 10000, "price_to": 12000, "duration_minutes": 30},
        {"clinic": gkb1, "name": "Консультация невролога", "category": "Неврология", "price_from": 12000, "price_to": 14000, "duration_minutes": 40},
        {"clinic": gkb1, "name": "МРТ головного мозга", "category": "Диагностика", "price_from": 35000, "price_to": 45000, "duration_minutes": 45},
        {"clinic": gkb1, "name": "КТ органов грудной клетки", "category": "Диагностика", "price_from": 28000, "price_to": 35000, "duration_minutes": 30},
        {"clinic": gkb1, "name": "Аппендэктомия (лапароскопия)", "category": "Хирургия", "price_from": 150000, "price_to": 200000, "duration_minutes": 60},

        # Dent Lux
        {"clinic": dent, "name": "Консультация стоматолога", "category": "Стоматология", "price_from": 3000, "price_to": 5000, "duration_minutes": 20},
        {"clinic": dent, "name": "Лечение кариеса (1 зуб)", "category": "Стоматология", "price_from": 12000, "price_to": 20000, "duration_minutes": 60},
        {"clinic": dent, "name": "Профессиональная чистка зубов", "category": "Стоматология", "price_from": 15000, "price_to": 20000, "duration_minutes": 60},
        {"clinic": dent, "name": "Отбеливание зубов (office bleaching)", "category": "Стоматология", "price_from": 40000, "price_to": 60000, "duration_minutes": 90},
        {"clinic": dent, "name": "Установка металлокерамической коронки", "category": "Стоматология", "price_from": 30000, "price_to": 45000, "duration_minutes": 60},
        {"clinic": dent, "name": "Имплантация зуба (под ключ)", "category": "Стоматология", "price_from": 150000, "price_to": 250000, "duration_minutes": 90},
        {"clinic": dent, "name": "Брекеты металлические (установка)", "category": "Стоматология", "price_from": 80000, "price_to": 120000, "duration_minutes": 120},

        # Cardio Center
        {"clinic": cardio, "name": "Консультация кардиолога", "category": "Кардиология", "price_from": 18000, "price_to": 22000, "duration_minutes": 45},
        {"clinic": cardio, "name": "ЭхоКГ (УЗИ сердца)", "category": "Кардиология", "price_from": 12000, "price_to": 15000, "duration_minutes": 30},
        {"clinic": cardio, "name": "Холтер-мониторинг ЭКГ (24 ч)", "category": "Кардиология", "price_from": 15000, "price_to": 18000, "duration_minutes": 20},
        {"clinic": cardio, "name": "Коронарография", "category": "Кардиология", "price_from": 120000, "price_to": 180000, "duration_minutes": 60},
        {"clinic": cardio, "name": "Стентирование коронарных артерий", "category": "Кардиология", "price_from": 350000, "price_to": 500000, "duration_minutes": 120},

        # Kids Clinic
        {"clinic": kids, "name": "Консультация педиатра", "category": "Педиатрия", "price_from": 8000, "price_to": 10000, "duration_minutes": 30},
        {"clinic": kids, "name": "Профилактический осмотр ребенка 1 год", "category": "Педиатрия", "price_from": 15000, "price_to": 20000, "duration_minutes": 90},
        {"clinic": kids, "name": "Консультация детского невролога", "category": "Неврология", "price_from": 11000, "price_to": 13000, "duration_minutes": 40},
        {"clinic": kids, "name": "Вакцинация (1 прививка)", "category": "Педиатрия", "price_from": 5000, "price_to": 8000, "duration_minutes": 15},

        # Nauryz
        {"clinic": nauryz, "name": "Прием терапевта", "category": "Терапия", "price_from": 4000, "price_to": 5000, "duration_minutes": 25},
        {"clinic": nauryz, "name": "Консультация гинеколога", "category": "Гинекология", "price_from": 5000, "price_to": 7000, "duration_minutes": 35},
        {"clinic": nauryz, "name": "Консультация хирурга", "category": "Хирургия", "price_from": 6000, "price_to": 8000, "duration_minutes": 30},
        {"clinic": nauryz, "name": "УЗИ органов малого таза", "category": "Гинекология", "price_from": 5000, "price_to": 7000, "duration_minutes": 20},

        # Visus
        {"clinic": visus, "name": "Консультация офтальмолога", "category": "Офтальмология", "price_from": 9000, "price_to": 12000, "duration_minutes": 35},
        {"clinic": visus, "name": "Проверка зрения и подбор очков", "category": "Офтальмология", "price_from": 5000, "price_to": 7000, "duration_minutes": 30},
        {"clinic": visus, "name": "Лазерная коррекция зрения LASIK (1 глаз)", "category": "Офтальмология", "price_from": 80000, "price_to": 120000, "duration_minutes": 30},
        {"clinic": visus, "name": "Операция при катаракте (1 глаз)", "category": "Офтальмология", "price_from": 150000, "price_to": 220000, "duration_minutes": 45},
        {"clinic": visus, "name": "Фотодинамическая терапия", "category": "Офтальмология", "price_from": 50000, "price_to": 80000, "duration_minutes": 30},

        # Asklepiy
        {"clinic": asklepiy, "name": "Консультация дерматолога", "category": "Дерматология", "price_from": 8000, "price_to": 10000, "duration_minutes": 30},
        {"clinic": asklepiy, "name": "Биопсия кожи", "category": "Дерматология", "price_from": 12000, "price_to": 15000, "duration_minutes": 30},
        {"clinic": asklepiy, "name": "Консультация терапевта", "category": "Терапия", "price_from": 7000, "price_to": 8000, "duration_minutes": 30},
        {"clinic": asklepiy, "name": "Консультация ортопеда", "category": "Хирургия", "price_from": 10000, "price_to": 12000, "duration_minutes": 35},
        {"clinic": asklepiy, "name": "Рентген (1 проекция)", "category": "Диагностика", "price_from": 3500, "price_to": 5000, "duration_minutes": 15},
        {"clinic": asklepiy, "name": "Комплекс анализов «Биохимия крови»", "category": "Диагностика", "price_from": 8000, "price_to": 12000, "duration_minutes": 10},
    ]

    count = 0
    for data in services_data:
        clinic = data.pop("clinic")
        service = Service(
            id=uuid.uuid4(),
            clinic_id=clinic.id,
            is_available=True,
            **data,
        )
        db.add(service)
        count += 1

    db.commit()
    print(f"Seeded {count} services.")


def seed_reviews(users, doctors, clinics):
    existing = db.query(Review).first()
    if existing:
        print("Reviews already seeded, skipping.")
        return

    if not users or len(users) < 3:
        print("Not enough users to seed reviews.")
        return

    user1, user2, user3 = users[0], users[1], users[2]
    clinic_map = {c.name: c for c in clinics}
    doctor_map = {f"{d.last_name} {d.first_name}": d for d in doctors}

    reviews_data = [
        # Clinic reviews
        {
            "user": user1,
            "clinic": clinic_map.get("Медицинский центр «Авиценна»"),
            "doctor": None,
            "rating": 5,
            "comment": "Отличная клиника! Очень вежливый персонал, чистые кабинеты, быстро приняли. Особенно понравилась кардиология.",
        },
        {
            "user": user2,
            "clinic": clinic_map.get("Медицинский центр «Авиценна»"),
            "doctor": None,
            "rating": 4,
            "comment": "Хорошая клиника, но немного дорого. Врачи профессиональные, оборудование современное.",
        },
        {
            "user": user3,
            "clinic": clinic_map.get("Стоматологическая клиника «Дент Люкс»"),
            "doctor": None,
            "rating": 5,
            "comment": "Лучшая стоматология в Алматы! Ходим всей семьей. Безболезненное лечение, доброжелательный персонал.",
        },
        {
            "user": user1,
            "clinic": clinic_map.get("Детская клиника «Балажан»"),
            "doctor": None,
            "rating": 5,
            "comment": "Привожу ребенка сюда уже 3 года. Педиатры замечательные, дети не боятся сюда ходить. Рекомендую всем родителям!",
        },
        {
            "user": user2,
            "clinic": clinic_map.get("Клиника «Здоровье»"),
            "doctor": None,
            "rating": 3,
            "comment": "Обычная районная поликлиника. Врачи есть хорошие, но очереди большие. Ждать пришлось 2 часа.",
        },
        # Doctor reviews
        {
            "user": user1,
            "clinic": None,
            "doctor": doctor_map.get("Джаксыбеков Серик"),
            "rating": 5,
            "comment": "Профессор Джаксыбеков — лучший кардиолог которого я встречал. Внимательный, точный диагноз, назначил правильное лечение.",
        },
        {
            "user": user3,
            "clinic": None,
            "doctor": doctor_map.get("Ахметова Дина"),
            "rating": 5,
            "comment": "Дина Маратовна — золотые руки! Вылечила мой страх у стоматолога. Процедуры абсолютно безболезненные.",
        },
        {
            "user": user2,
            "clinic": None,
            "doctor": doctor_map.get("Жунусова Зарина"),
            "rating": 5,
            "comment": "Зарина Маратовна наблюдает нашего ребенка с рождения. Очень компетентный врач, всегда найдет время объяснить.",
        },
        {
            "user": user1,
            "clinic": None,
            "doctor": doctor_map.get("Мороз Светлана"),
            "rating": 5,
            "comment": "Светлана Александровна — настоящий профессионал с большим опытом. Наш семейный педиатр уже 10 лет.",
        },
        {
            "user": user3,
            "clinic": None,
            "doctor": doctor_map.get("Алтынбеков Кайрат"),
            "rating": 5,
            "comment": "Кайрат Сейтжанович спас жизнь моему мужу. Великолепный специалист, настоящий профессионал своего дела.",
        },
    ]

    count = 0
    for data in reviews_data:
        clinic = data.pop("clinic")
        doctor = data.pop("doctor")
        user = data.pop("user")

        if clinic is None and doctor is None:
            continue

        review = Review(
            id=uuid.uuid4(),
            user_id=user.id,
            clinic_id=clinic.id if clinic else None,
            doctor_id=doctor.id if doctor else None,
            is_moderated=True,
            **data,
        )
        db.add(review)
        count += 1

    db.commit()
    print(f"Seeded {count} reviews.")


def main():
    print("Starting seed...")
    try:
        admin, regular_users = seed_users()
        clinics = seed_clinics()
        doctors = seed_doctors(clinics)
        seed_services(clinics)
        seed_reviews(regular_users, doctors, clinics)
        print("\nSeed completed successfully!")
        print(f"Admin credentials: admin@medical.kz / admin123")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
