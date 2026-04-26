from maxapi import Router, F
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from maxapi.enums import parse_mode
from states.states import LeadForm

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
