
# Ответ бота на команду /start
@dp.message_created(Command('start'))
async def hello(event: MessageCreated):
    await event.message.answer('Привет чат-бот для Max! Напиши мне.')


# Обработчик только текстовых сообщений
@dp.message_created(F.message.body.text)
async def text_handler(event: MessageCreated):
    text = event.message.body.text
    await event.message.answer(f"Длина вашего сообщения: {len(text)} символов")