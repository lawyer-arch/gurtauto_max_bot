import re
import logging
from maxapi import Router, F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from maxapi.enums import parse_mode
from states.states import LeadForm
from database.repository.user_repo import UserRepository
from database.repository.lead_repo import LeadRepository
from services.lead_service import LeadService
from services.notify_service import NotifyService
from database.session import async_session
from keyboards.catalog_keyboards import (
    button_generator_drive,
    button_generator_fuel,
    button_generator_year,
    button_generator_repairs,
    button_generator_further
    )

router = Router()

""" Выбираем марку, модель, цвет кузова"""
@router.message_callback(F.callback.payload == 'fill_form')
async def start_handler(event: MessageCreated, context: MemoryContext):
    get_message = (
        "Укажите марку, модель, цвет кузова желаемого автомобиля.\n\n"
        "<b>Это ВАЖНО!</b>\n"
        "Обязательно в указанном порядке!"
    )
    await context.set_state(LeadForm.marka_model_color)
    await event.message.answer(
        text=get_message,
        format=parse_mode.ParseMode.HTML,)


"""Выбираем объем двигателя"""
@router.message_created(LeadForm.marka_model_color)
async def name_handler(event: MessageCreated, context: MemoryContext):
    parts = event.message.body.text.split()
    if len(parts) < 2:
        await event.message.answer(
            "❗ Укажите минимум: марка и модель (например: BMW X5)"
        )
        return
    
    get_message = (
        "Укажите объем двигателя."
    )
    await context.update_data(marka_model_color=parts)
    await context.set_state(LeadForm.engine)
    await event.message.answer(get_message)


"""Выбираем тип привода"""
@router.message_created(LeadForm.engine)
async def select_drive_type(event: MessageCreated, context: MemoryContext):
    """
    Обработчик выбора типа двигателя.
    Сохраняет выбранный тип двигателя и предлагает выбрать тип привода.
    """
    # олучаем предыдущее значение
    parts = event.message.body.text

    # Сохраняем выбранный тип двигателя в FSMContext
    await context.update_data(engine=parts)
    
    # Переходим к следующему шагу FSM
    await context.set_state(LeadForm.drive)
    
    # Предложение пользователю выбрать тип привода
    prompt = "Укажите тип привода."
    
    # Отправляем сообщение с клавиатурой выбора привода
    await event.message.answer(
        text=prompt,
        format=parse_mode.ParseMode.HTML,
        attachments=[button_generator_drive()]
    )


"""Выбираем тип топлива"""
@router.message_callback(
    F.callback.payload.in_(
        ["drive_4wd", "drive_front", "drive_rear"]
    ),
    LeadForm.drive
)
async def select_fuel_type(event: MessageCreated, context: MemoryContext):
    """
    Обработчик выбора типа привода.
    Сохраняет выбранный тип привода и предлагает выбрать тип топлива.
    """
    
    # получвем = "drive_4wd", "drive_front" или "drive_rear"
    payload = event.callback.payload
    
    # получаем "4wd", "front" или "rear"
    selected_drive = payload.split("_")[1]  
    
    # Сохраняем выбранный тип привода в FSMContext
    await context.update_data(drive=selected_drive)
    
    # Переходим к следующему шагу FSM
    await context.set_state(LeadForm.fuel)
    
    # Предложение пользователю выбрать тип топлива
    prompt = "Выберите тип топлива"
    
    # Отправляем сообщение с клавиатурой выбора топлива
    await event.message.answer(
        text=prompt,
        format=parse_mode.ParseMode.HTML,
        attachments=[button_generator_fuel()]
    )
    
    # закрываем индикатор кнопки
    await event.answer()


"""Выбираем пробег"""
@router.message_callback(
    F.callback.payload.in_(["fuel_petrol", "fuel_diesel", "fuel_electric"]),
    LeadForm.fuel
)
async def handler_mileage(event: MessageCreated, context: MemoryContext):
    # Получаем выбранное значение топлива из callback_data
    payload = event.callback.payload
    
    selected_fuel = payload.split("_")[1]  
    
    get_message = "Укажите желаемый пробег"
    
    # Запоминаем выбранное значение в состоянии
    await context.update_data(fuel=selected_fuel)
    
    # Переводим машину состояний дальше
    await context.set_state(LeadForm.mileage)
    await event.message.answer(text=get_message)


"""Выбераем возраст авто"""
@router.message_created(LeadForm.mileage)
async def handler_year(event: MessageCreated, context: MemoryContext):
    
    get_message = "Выберите желаемый диапазон возраста автомобиля"
    
    await context.update_data(mileage=event.message.body.text)
    await context.set_state(LeadForm.year)
    await event.message.answer(
        text=get_message,
        attachments=[button_generator_year()]
    )
    
    
"""Выбираем бюджет"""
@router.message_callback(
    F.callback.payload.in_(["year_3", "year_3-5", "year_more-than-5"]),
    LeadForm.year
)
async def handler_budget(event: MessageCreated, context: MemoryContext):
    # Получаем выбранное значение топлива из callback_data
    payload = event.callback.payload
    selected_year = payload.split("_")[1]  
    
    get_message = "Укажите желаемый бюджет"
    
    # Запоминаем выбранное значение в состоянии
    await context.update_data(year=selected_year)
    # Переводим машину состояний дальше
    await context.set_state(LeadForm.budget)
    await event.message.answer(text=get_message)
    await event.answer()


"""Выбираем допустимы или нет повреждения"""
@router.message_created(LeadForm.budget)
async def handler_repairs(event: MessageCreated, context: MemoryContext):
    selected_budget = event.message.body.text
    get_message = "Выбирите допустимость повреждений"
    await context.update_data(budget=selected_budget)
    await context.set_state(LeadForm.repairs)
    await event.message.answer(
            text=get_message,
            attachments=[button_generator_repairs()]
        )


"""Предлагаем оставить ссылку на сайт"""
@router.message_callback(
    F.callback.payload.in_(["repairs_yes", "repairs_no"]),
    LeadForm.repairs
)
async def handler_url(event: MessageCreated, context: MemoryContext):
    # Получаем выбранное значение топлива из callback_data
    payload = event.callback.payload
    selected_repairs = payload.split("_")[1]
    get_message = (
        "По желанию оставьте ссылку на выбранный автомобиль Авито, Дром и т.д.\n"
        "Или нажмите «Пропустить», если не хотите прикреплять."
    )
    # Запоминаем выбранное значение в состоянии
    await context.update_data(repairs=selected_repairs)
    # Переводим машину состояний дальше
    await context.set_state(LeadForm.url)
    await event.message.answer(
        text=get_message,
        format=parse_mode.ParseMode.HTML,
        attachments=[button_generator_further()]
    )
    await event.answer()


"""Ловит кнопку далее"""
@router.message_callback(
    F.callback.payload == "further",
    LeadForm.url
)
async def skip_url_or_image(event: MessageCreated, context: MemoryContext):
    # Сохраняем None для обоих полей — пользователь ничего не прикрепил
    await context.update_data(url=None)
    await context.set_state(LeadForm.phone)
    # Отправляем сообщение с запросом телефона
    await event.message.answer(
        text="Оставьте контактный номер телефона"
    )


"""Предлагаем оставить телефон"""
@router.message_created(LeadForm.url)
async def handler_url_or_image(event: MessageCreated, context: MemoryContext):
    try:
        text = event.message.body.text.strip()
        # Проверяем, является ли текст ссылкой
        if re.match(r'https?://\S+', text):
            await context.update_data(url=text)
            # Явно сообщаем о переходе к следующему шагу
            text = "Ссылка сохранена. Оставьте контактный номер телефона"
            await event.message.answer(
                    text=text
                )
        else:
            # Если текст не ссылка — считаем, что пользователь ошибся
            "Это не похоже на ссылку. Отправьте ссылку или нажмите «Пропустить»."
            await event.message.answer(
                    "Это не похоже на ссылку. Отправьте ссылку или нажмите «Пропустить»."
                )
            return
        # Переходим к следующему шагу только если данные корректны
        await context.set_state(LeadForm.phone)

    except Exception as e:
        logging.error(f"Error processing url: {e}")
        await event.message.answer(
            "Произошла ошибка. Отправьте ссылку, либо нажмите «Пропустить»."
        )


@router.message_created(LeadForm.phone)
async def phone_handler(event: MessageCreated, context: MemoryContext):

    if not event.message.body.text:
        await event.message.answer("❗ Введите телефон")
        return

    # Нормализация
    phone = re.sub(r"[^\d]", "", event.message.body.text)
    phone = "+" + phone

    # Валидация
    if not re.match(r"^\+7\d{10}$", phone):
        await event.message.answer(
            "❗ Некорректный телефон. Введите ещё раз (пример: +79991234567)"
        )
        return

    data = await context.get_data()

    async with async_session() as session:

        user_repo = UserRepository(session)
        user = await user_repo.get_or_create(
            event.from_user.user_id,
            event.from_user.username or "",
            event.from_user.full_name or event.from_user.first_name or ""
        )
        
        print(user)
        
        lead_repo = LeadRepository(session)
        service = LeadService(lead_repo)
        
        try:
            await service.create_lead({
                "user_id": user.id,
                "phone": phone,
                "marka": data.get("marka"),
                "model": data.get("model"),
                "color": data.get("color", "не указано"),
                "engine": data.get("engine", "не указано"),
                "drive": data.get("drive", "не указано"),
                "fuel": data.get("fuel", "не указано"),
                "mileage": data.get("mileage", "не указано"),
                "year": data.get("year", "не указано"),
                "budget": data.get("budget", "не указано"),
                "repairs": data.get("repairs", "не указано"),
                "url": data.get("url"),
                "image_data": data.get("image_data")
            })
        except Exception as e:
            logging.error(f"DB error: {e}", exc_info=True)
            await event.message.answer(
                "❗ Ошибка сохранения заявки. Попробуйте позже."
            )
            return

    notify = NotifyService(event.message.bot)

    try:
        await notify.send_new_lead(
            event.message.from_user.full_name,
            phone,
            data
        )
    except Exception as e:
        logging.error(f"Notify error: {e}")

    await event.message.answer("✅ Заявка отправлена")
    await context.clear()
