from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import CallbackButton


async def generate_main_menu_markup():
    """
    Генерирует и возвращает объект InlineKeyboardMarkup для главного меню.
    Функция НЕ отправляет сообщения, а только создает интерфейс.
    """
    builder = InlineKeyboardBuilder()
    # Создаем кнопки.
    
    builder.row(
        CallbackButton(
            text="📢 Оставить заявку на покупку авто",
            payload="leave_request"
        )
    )
    
    builder.row(
        CallbackButton(text="☎️ Контакты", payload="contacts"),
        CallbackButton(text="✨ Отзывы", payload="reviews"),
    )
    builder.row(
        CallbackButton(text="📄 О нас", payload="about_us")
    )
    
    return builder.as_markup()
