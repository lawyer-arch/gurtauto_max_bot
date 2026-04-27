from maxapi import Router, F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from maxapi.enums import parse_mode
from states.states import LeadForm
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
