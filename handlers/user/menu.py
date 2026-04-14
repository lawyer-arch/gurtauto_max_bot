import logging
from maxapi import Router, F
from maxapi.enums import parse_mode
from maxapi.types import MessageCreated, MessageCallback
from maxapi.types.attachments.upload import AttachmentUpload, AttachmentPayload
from maxapi.enums.upload_type import UploadType
from maxapi.exceptions import MaxApiError

from keyboards.catalog_keyboards import (
    button_generator_application,
    button_generator_comments,

)

router = Router(router_id="menu_router")

logger = logging.getLogger(__name__)

MAX_CAPTION = 1024
MAX_MESSAGE = 4000


# Обработчик кнопки "Оставить заявку на подбор авто"
@router.message_callback(F.callback.payload == 'leave_request')
async def leave_application(callback: MessageCallback):
    # Обратите внимание: объект теперь называется 'callback'
    
    html_text = (
        "🖊️ Ответьте на несколько вопросов\n"
        "   и по желанию приложите фото,\n"
        "   ссылку на Авито или Дром."
    )
    
    # Отправляем ответ на нажатие кнопки
    await callback.message.answer(
        text=html_text,
        format=parse_mode.ParseMode.HTML,
        attachments=[await button_generator_application()]
    )


@router.message_callback(F.callback.payload == "reviews")
async def see_reviews(callback: MessageCallback):
    # Отправляем сообщение с клавиатурой
    html_text = (
        "<b>В указанных каналах Вы можете подробно\n</b>"
        "<b>ознакомится с отзывами сотен клиентов\n</b>"
        "<b>и более подробно узнать о GURTAUTO.</b>",
    )
    await callback.message.answer(
        text=html_text,
        format=parse_mode.ParseMode.HTML,
        reply_markup=button_generator_comments()
    )
    
@router.message_callback(F.callback.payload == "contacts")
async def show_contacts(event: MessageCreated):
    await event.message.answer(
        "<b>Как нас найти:</b>\n"
        "<b>Max: +79016131647</b>\n"
        "<b> WhatsApp: +79016131647</b>\n"
        "<b> В СЛУЧАЕ ОТСУТСТВИЯ СВЯЗИ ПРОСТО ЗВОНИТЕ</b>\n"
        "⚠️ПО ☎️ +79016131647"
    )
    
@router.message_callback(F.callback.payload == "about_us")
async def show_about_us(callback: MessageCallback):
    img_path = "image/1000047083.jpg"  # исходное фото
   
    photo = FSInputFile(img_path)
    
    # Короткий текст для подписи (caption)
    short_caption = (
        "<b>Приветствуем вас в GURTAUTO!</b>\n"
        "Мы доставляем автомобили из Китая, Японии, Кореи и Киргизии."
    )
    # Отправляем фото с подписью
    await message.answer_photo(photo=photo, caption=short_caption)
    
    # Полный текст для отдельного сообщения
    full_text = (
        "<i>Если вы планируете приобрести автомобиль в ближайшее время, </i>"
        "<i>просто отправьте нам запрос с помощью бота: @GurtautoBot</i>\n\n"
        "<i>Мы оперативно рассчитаем стоимость с учетом доставки </i>"
        "<i>в ваш город и предложим лучшие условия.</i>\n"
        "<b>Для новых клиентов у нас действует скидка 15% </b>"
        "<b>на нашу комиссию в честь первого сотрудничества!</b>\n\n"
        "<i>Кроме того, участвуйте в нашей акции: </i>"
        "<b>и получите 10 000 рублей за рекомендацию нашей компании</b>\n\n"
        "<b>НАША КОНТАКТЫ И ОТЗЫВЫ ТУТ:👇</b>\n"
        "VK: vk.com/gurt_auto\n"
        "TG: t.me/gurt_auto\n"
        "https://2gis.ru/krasnodar/geo/70000001104157255\n"
        "МАХ: https://max.ru/id7000020472_biz\n\n"
        "<b>ЗАПРОСЫ ДЛЯ РАСЧЁТА СТОИМОСТИ НУЖНОГО ВАМ АВТО НАПРАВЛЯЙТЕ СЮДА:👇</b>\n"
        "➡️ Телеграм бот: @GurtautoBot\n"
        "➡️ СЮДА В https://vk.ru/gurt_auto СООБЩЕСТВО-КНОПКА НАПИСАТЬ СООБЩЕСТВУ\n"
        "➡️ TG: t.me/gurt_auto, ВНИЗУ ИКОНКА СООБЩЕНИЙ\n"
        "➡️ МАХ: https://max.ru/id7000020472_biz\n"
        "➡️ WhatsApp: wa.me/+79016131647\n"
        "➡️ В СЛУЧАЕ ОТСУТСТВИЯ СВЯЗИ ПРОСТО ЗВОНИТЕ\n"
        "⚠️ПО ☎️ 89016131647\n\n"
        "<b>Ждем ваших запросов и готовы помочь с выбором автомобиля вашей мечты!</b>"
    )
    
    # Разбиваем длинный текст на части и отправляем
    messages = textwrap.wrap(full_text, width=MAX_MESSAGE, replace_whitespace=False)
    for part in messages:
        await message.answer(part, parse_mode="HTML")