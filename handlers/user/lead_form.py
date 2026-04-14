from maxapi import Router
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated, Command
from states.states import LeadForm

router = Router()

""" Выбираем марку, модель, цвет кузова"""
@router.message_created(Command('start'))
async def start_handler(event: MessageCreated, context: MemoryContext):
    get_message = (
        "Укажите марку, модель, цвет кузова желаемого автомобиля.\n"
        "Обязательно в указанном порядке! Это ВАЖНО!"
    )
    await context.set_state(LeadForm.marka_model_color)
    await event.message.answer(get_message)


"""Выбираем объем двигателя"""
@router.message_created(LeadForm.marka_model_color)
async def name_handler(event: MessageCreated, context: MemoryContext):
    parts = event.message.body.text.split()
    if len(parts) < 2:
        await event.message.answer("❗ Укажите минимум: марка и модель (например: BMW X5)")
        return
    
    get_message = (
        "Укажите объем двигателя."
    )
    await context.update_data(marka_model_color=parts)
    await context.set_state(LeadForm.engine)
    await event.message.answer(get_message)




# переделвть
@dp.message_created(LeadForm.engine)
async def age_handler(event: MessageCreated, context: MemoryContext):
    data = await context.get_data()
    await event.message.answer(
        f"Приятно познакомиться, {data['name']}! "
        f"Вам {event.message.body.text} лет."
    )
    await context.set_state(None)  # Сброс состояния