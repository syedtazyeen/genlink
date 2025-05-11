from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from fastapi import HTTPException, status
from jinja2 import Environment, PackageLoader, select_autoescape

from app.core.config import get_config


class EmailService:
    env = Environment(
        loader=PackageLoader("app", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    settings = get_config()
    
    @classmethod
    async def _send_email(
        cls,
        to_email: str,
        subject: str,
        html_content: str,
    ) -> None:
        """Send email using configured SMTP server."""
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = cls.settings.SMTP_SENDER_EMAIL
        message["To"] = to_email

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        try:
            await aiosmtplib.send(
                message,
                hostname=cls.settings.SMTP_HOST,
                port=cls.settings.SMTP_PORT,
                username=cls.settings.SMTP_USERNAME,
                password=cls.settings.SMTP_PASSWORD,
                start_tls=cls.settings.SMTP_USE_TLS,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to send email: {str(e)}",
            )

    @classmethod
    async def send_password_reset_code(cls, to_email: str, reset_code: str) -> None:
        """Send password reset code email."""
        template = cls.env.get_template("password_reset.html")
        html_content = template.render(
            reset_code=reset_code, app_name=cls.settings.APP_NAME
        )

        await cls._send_email(
            to_email=to_email,
            subject=f"{cls.settings.APP_NAME} - Password Reset Code",
            html_content=html_content,
        )

    @classmethod
    async def send_welcome_email(cls, to_email: str, full_name: str) -> None:
        """Send welcome email to new users."""
        template = cls.env.get_template("welcome.html")
        html_content = template.render(
            full_name=full_name, app_name=cls.settings.APP_NAME
        )

        await cls._send_email(
            to_email=to_email,
            subject=f"Welcome to {cls.settings.APP_NAME}!",
            html_content=html_content,
        )
