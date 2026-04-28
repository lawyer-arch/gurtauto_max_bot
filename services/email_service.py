import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings


class EmailService:
    
    async def send_lead_notification(self, user_name: str, phone: str, data: dict):
        """Отправка уведомления о новой заявке на email"""
        
        # Формируем тело письма
        text = f"""
        🔥 НОВАЯ ЗАЯВКА!
        
        👤 {user_name}
        📞 {phone}
        
        🚗 {data.get('marka')} {data.get('model')} ({data.get('color')})
        Двигатель: {data.get('engine')}
        Привод: {data.get('drive')}
        Топливо: {data.get('fuel')}
        Пробег: {data.get('mileage')}
        Возраст: {data.get('year')}
        Состояние: {data.get('repairs')}
        Бюджет: {data.get('budget')}
        """
        
        if data.get("url"):
            text += f"\n\n🔗 Ссылка:\n{data.get('url')}"
        
        # Создаём письмо
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_LOGIN
        msg["To"] = settings.NOTIFICATION_EMAIL
        msg["Subject"] = f"🔥 Новая заявка от {user_name}"
        msg.attach(MIMEText(text, "plain", "utf-8"))
        
        # Отправляем
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_LOGIN,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
            start_tls=False
        )