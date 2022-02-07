from pathlib import Path

from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from starlette.background import BackgroundTasks

from ecommerce.orders import schema, models
from ecommerce.settings import config

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER= Path(__file__).resolve().parent.parent / 'templates'
)


async def send_email_async(subject: str, email_to: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


def send_email_background(background_tasks: BackgroundTasks, email_to: str, order: schema.ShowOrder):
    message = MessageSchema(
        subject='Ecommerce mail module',
        recipients=[email_to],
        template_body={'body': order.dict()}
    )
    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')
