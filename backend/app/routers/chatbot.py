import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from app.database import get_db
from app.models.clinic import Clinic
from app.models.doctor import Doctor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

SPECIALTY_KEYWORDS = {
    "терапевт": ["терапевт", "терапия", "общий врач", "обследование", "температура", "простуда", "грипп"],
    "кардиолог": ["кардиолог", "сердце", "давление", "аритмия", "кардио", "сосуды"],
    "невролог": ["невролог", "голова", "головная боль", "мигрень", "нервы", "позвоночник", "невро"],
    "педиатр": ["педиатр", "ребенок", "дети", "детский", "малыш", "педиатрия"],
    "хирург": ["хирург", "операция", "хирургия", "удаление", "разрез"],
    "офтальмолог": ["офтальмолог", "глаза", "зрение", "очки", "офтальмо", "глазной"],
    "дерматолог": ["дерматолог", "кожа", "сыпь", "дерматит", "акне", "кожный"],
    "гинеколог": ["гинеколог", "гинекология", "женский", "беременность", "женщина"],
    "ортопед": ["ортопед", "кости", "суставы", "колено", "позвоночник", "ортопедия"],
    "стоматолог": ["стоматолог", "зубы", "зуб", "десны", "стоматология"],
}

GREETING_KEYWORDS = ["привет", "здравствуйте", "добрый", "hello", "hi"]
GOODBYE_KEYWORDS = ["пока", "до свидания", "спасибо", "благодарю"]
HELP_KEYWORDS = ["помощь", "помоги", "как", "что", "информация", "помочь"]
PRICE_KEYWORDS = ["цена", "стоимость", "сколько стоит", "прайс", "тариф"]
ADDRESS_KEYWORDS = ["адрес", "где", "находится", "расположен", "местонахождение"]
APPOINTMENT_KEYWORDS = ["запись", "записаться", "прием", "назначить", "забронировать"]


class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str


def detect_specialty(message: str) -> Optional[str]:
    message_lower = message.lower()
    for specialty, keywords in SPECIALTY_KEYWORDS.items():
        for kw in keywords:
            if kw in message_lower:
                return specialty
    return None


def format_clinic_info(clinic: Clinic) -> str:
    info = f"**{clinic.name}**\n"
    info += f"Адрес: {clinic.address}, {clinic.city}\n"
    if clinic.district:
        info += f"Район: {clinic.district}\n"
    if clinic.phone:
        info += f"Телефон: {clinic.phone}\n"
    if clinic.rating and clinic.rating > 0:
        info += f"Рейтинг: {clinic.rating:.1f}/5 ({clinic.reviews_count} отзывов)\n"
    return info


def format_doctor_info(doctor: Doctor) -> str:
    full_name = f"{doctor.last_name} {doctor.first_name}"
    if doctor.patronymic:
        full_name += f" {doctor.patronymic}"
    info = f"**{full_name}** — {doctor.specialty}\n"
    if doctor.experience_years:
        info += f"Опыт: {doctor.experience_years} лет\n"
    if doctor.consultation_price:
        info += f"Стоимость консультации: {int(doctor.consultation_price)} тг\n"
    return info


@router.post("/message", response_model=ChatResponse)
def chatbot_message(
    chat_input: ChatMessage,
    db: Session = Depends(get_db),
):
    message = chat_input.message.strip()
    session_id = chat_input.session_id or str(uuid4())
    message_lower = message.lower()

    logger.info(f"Chatbot message received: session={session_id}, message={message[:100]}")

    # Greeting
    if any(kw in message_lower for kw in GREETING_KEYWORDS):
        reply = (
            "Здравствуйте! Я помогу вам найти клинику или врача в Алматы. "
            "Вы можете спросить меня о:\n"
            "- Клиниках и врачах по специальности (например: 'кардиолог', 'стоматолог')\n"
            "- Адресах и контактах клиник\n"
            "- Ценах на консультации\n"
            "- Записи на прием\n\n"
            "Чем я могу вам помочь?"
        )
        return ChatResponse(reply=reply, session_id=session_id)

    # Goodbye
    if any(kw in message_lower for kw in GOODBYE_KEYWORDS):
        reply = "Рады были помочь! Если у вас возникнут вопросы — обращайтесь. Будьте здоровы!"
        return ChatResponse(reply=reply, session_id=session_id)

    # Appointment booking guidance
    if any(kw in message_lower for kw in APPOINTMENT_KEYWORDS):
        reply = (
            "Чтобы записаться на прием:\n"
            "1. Выберите клинику или врача на нашем сайте\n"
            "2. Нажмите кнопку 'Записаться'\n"
            "3. Выберите удобную дату и время\n"
            "4. Укажите контактные данные\n\n"
            "Хотите найти врача определённой специальности? Напишите, например: 'кардиолог' или 'стоматолог'."
        )
        return ChatResponse(reply=reply, session_id=session_id)

    # Specialty-based search
    specialty = detect_specialty(message)
    if specialty:
        doctors = db.query(Doctor).filter(
            Doctor.specialty.ilike(f"%{specialty}%"),
            Doctor.is_available == True,
        ).limit(5).all()

        clinics_with_specialty_ids = {d.clinic_id for d in doctors}
        clinics = db.query(Clinic).filter(
            Clinic.id.in_(clinics_with_specialty_ids)
        ).limit(3).all()

        if not doctors:
            reply = (
                f"К сожалению, в данный момент я не нашёл врачей специальности '{specialty}' "
                f"в нашей базе данных. Попробуйте воспользоваться поиском на сайте."
            )
        else:
            reply = f"Я нашёл врачей по специальности **{specialty}**:\n\n"
            for doctor in doctors[:3]:
                reply += format_doctor_info(doctor)
                reply += "\n"

            if clinics:
                reply += "\nКлиники с таким специалистом:\n\n"
                for clinic in clinics[:2]:
                    reply += format_clinic_info(clinic)
                    reply += "\n"

            reply += "\nВы можете найти больше специалистов в разделе 'Врачи' на нашем сайте."

        return ChatResponse(reply=reply, session_id=session_id)

    # Address/location query
    if any(kw in message_lower for kw in ADDRESS_KEYWORDS):
        clinics = db.query(Clinic).filter(Clinic.is_verified == True).limit(5).all()
        if not clinics:
            clinics = db.query(Clinic).limit(5).all()

        if clinics:
            reply = "Вот некоторые наши клиники в Алматы:\n\n"
            for clinic in clinics[:3]:
                reply += format_clinic_info(clinic)
                reply += "\n"
            reply += "Полный список клиник доступен в разделе 'Клиники' на нашем сайте."
        else:
            reply = "Список клиник доступен в разделе 'Клиники' на нашем сайте."

        return ChatResponse(reply=reply, session_id=session_id)

    # Price query
    if any(kw in message_lower for kw in PRICE_KEYWORDS):
        doctors = db.query(Doctor).filter(
            Doctor.consultation_price != None,
            Doctor.is_available == True,
        ).order_by(Doctor.consultation_price).limit(5).all()

        if doctors:
            prices = [int(d.consultation_price) for d in doctors if d.consultation_price]
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0
            reply = (
                f"Стоимость консультаций в наших клиниках варьируется от {min_price} до {max_price} тенге, "
                f"в зависимости от специальности врача и клиники.\n\n"
                f"Примеры цен:\n"
            )
            for doctor in doctors[:3]:
                reply += f"- {doctor.specialty}: от {int(doctor.consultation_price)} тг\n"
            reply += "\nТочные цены уточняйте на странице конкретного врача или клиники."
        else:
            reply = "Информацию о ценах на консультации вы можете найти на страницах врачей и клиник."

        return ChatResponse(reply=reply, session_id=session_id)

    # Search clinics/doctors by name keyword
    clinics_by_name = db.query(Clinic).filter(
        Clinic.name.ilike(f"%{message}%")
    ).limit(3).all()

    if clinics_by_name:
        reply = f"Я нашёл клиники по вашему запросу '{message}':\n\n"
        for clinic in clinics_by_name:
            reply += format_clinic_info(clinic)
            reply += "\n"
        return ChatResponse(reply=reply, session_id=session_id)

    # Generic help response
    reply = (
        "Я не совсем понял ваш вопрос. Я могу помочь вам с:\n\n"
        "- **Поиском врача** по специальности (напишите, например: 'терапевт', 'кардиолог', 'стоматолог')\n"
        "- **Адресами клиник** (напишите: 'адреса клиник')\n"
        "- **Ценами** на консультации (напишите: 'сколько стоит консультация')\n"
        "- **Записью на прием** (напишите: 'как записаться')\n\n"
        "Попробуйте сформулировать вопрос иначе или воспользуйтесь поиском на сайте."
    )
    return ChatResponse(reply=reply, session_id=session_id)
