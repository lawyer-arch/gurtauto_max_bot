from maxapi.types import LinkButton, ButtonsPayload
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.types.attachments.buttons import CallbackButton

"""Модуль содержит кнопки интерактива отображаемых для пользователя""" 


async def button_generator_application():
    """Генерирует кнопки заявки"""
    builder = InlineKeyboardBuilder()
    builder.row(
        CallbackButton(text="📝 Заполнить форму", payload="fill_form")
    )
    
    return builder.as_markup()


def button_generator_comments():
    """Генерирует кнопки-ссылки на источники отзывов"""
    
    builder = InlineKeyboardBuilder()
    
    builder.row(
        LinkButton(text="Вконтакте", url="https://vk.com/gurt_auto"),
        LinkButton(text="Telegram", url="https://t.me/gurt_auto"),
        LinkButton(
            text="2GIS",
            url="https://2gis.ru/krasnodar/geo/70000001104157255"
        )
    )

    return builder.as_markup()


def button_generator_drive():
    
    """Генерирует кнопки выбора привода передний, полный, задний"""
    
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="4WD", payload="drive_4wd"),
        CallbackButton(text="Передний привод", payload="drive_front"),
        CallbackButton(text="Задний привод", payload="drive_rear")
    )
    
    return builder.as_markup()
    

def button_generator_fuel():
    
    """Генерирует кнопки выбора топлива бензин, дизель, гибрид, элетрический"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="Бензин", payload="fuel_petrol"),
        CallbackButton(text="Дизель", payload="fuel_diesel"),
        CallbackButton(text="Электрический", payload="fuel_electric")
    )
    
    return builder.as_markup()


def button_generator_year():
    
    """Генерирует кнопки выбора года"""
    
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="До 3-х лет", payload="year_3"),
        CallbackButton(text="3-5 лет", payload="year_3-5"),
        CallbackButton(text="Старше 5 лет", payload="year_more-than-5")
    )
    
    return builder.as_markup()


def button_generator_repairs():
    
    """Генерирует кнопки выбора допустимости повреждений авто"""
    
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="Допустимо", payload="repairs_yes"),
        CallbackButton(text="Не допустимо", payload="repairs_no"),
    )
    
    return builder.as_markup()


def button_generator_further():
    
    """Генерирует кнопки далее"""
    
    builder = InlineKeyboardBuilder()
    
    builder.row(
        CallbackButton(text="Пропустить", payload="further")
    )
    
    return builder.as_markup()
