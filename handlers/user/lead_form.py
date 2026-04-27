from maxapi import Router, F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from maxapi.enums import parse_mode
from states.states import LeadForm
from keyboards.catalog_keyboards import button_generator_drive

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
    parts = event.message.body.text.split()
    
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