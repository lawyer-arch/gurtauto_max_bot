import logging
from maxapi import Router
from maxapi.types import MessageCreated, Command
from maxapi.types.attachments.upload import AttachmentUpload, AttachmentPayload
from maxapi.enums.upload_type import UploadType
from maxapi.exceptions import MaxApiError

router = Router(router_id="menu_router")

logger = logging.getLogger(__name__)

@router.message_created(Command('start'))
async def help_handler(event: MessageCreated):
    await event.message.answer("Начнем!")


@router.message_created(Command('send_photo'))
async def send_photo_by_token(event: MessageCreated):
    # Проверяем, есть ли текстовое содержимое в сообщении
    if not hasattr(event.message, 'content') or not event.message.content:
        await event.message.answer("Сообщение не содержит текста. Используйте: /send_photo <токен>")
        return

    # Получаем аргументы команды из текста сообщения
    command_args = event.message.content.split()[1:] if event.message.content else []

    if not command_args:
        await event.message.answer("Укажите токен фото после команды /send_photo")
        return

    token = command_args[0].strip()

    # Логирование для отладки
    logger.info(f"Попытка отправить фото. Токен: {token}, тип: {type(token)}")

    # Проверка: токен — строка
    if not isinstance(token, str):
        await event.message.answer("Токен должен быть строкой")
        return

    try:
        # Создаём вложение с динамическим токеном
        attachment = AttachmentUpload(
            type=UploadType.IMAGE,
            payload=AttachmentPayload(token=token)
        )

        # Отправляем сообщение с вложением
        await event.message.answer(
            text="Вот ваше фото по токену",
            attachments=[attachment]
        )
        logger.info("Фото успешно отправлено")

    except MaxApiError as e:
        logger.error(f"Ошибка API при отправке фото: {e.raw}")
        await event.message.answer(
            "Не удалось отправить фото: неверный токен или ошибка API"
        )
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        await event.message.answer("Произошла непредвиденная ошибка")