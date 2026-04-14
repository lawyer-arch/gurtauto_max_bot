from maxapi.types import MessageCreated, Command
from maxapi.enums import parse_mode 
from keyboards.main_menu import generate_main_menu_markup
from maxapi import Router

router = Router(router_id="start")


@router.message_created(Command('start'))
async def start_handler(event: MessageCreated):
    html_text = (
        "<i>🚗 Добро пожаловать!</i>\n"
        "<b>          GURTAUTO</b>\n"
        "<i>поможет воплотить мечту в реальность.</i>"
    )
    
    await event.message.answer(
        text=html_text,
        format=parse_mode.ParseMode.HTML,
        attachments=[await generate_main_menu_markup()]
    )
