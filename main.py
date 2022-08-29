import os
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List

load_dotenv('.env')

username = os.getenv('EMAIL_HOST_USER')
password = os.getenv('EMAIL_HOST_PASSWORD')
email_from = os.getenv('EMAIL_FROM')
email_port = os.getenv('EMAIL_PORT')
email_server = os.getenv('EMAIL_HOST')


class EmailSchema(BaseModel):
    subject: str
    email: List[EmailStr]
    content: str


conf = ConnectionConfig(
    MAIL_USERNAME=username,
    MAIL_PASSWORD=password,
    MAIL_FROM=email_from,
    MAIL_PORT=email_port,
    MAIL_SERVER=email_server,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

app = FastAPI()

html = """Thanks for using our App"""


@app.get("/")
def read_root():
    return {"Hello": html}


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    print(email)
    message = MessageSchema(
        subject=email.subject,
        recipients=email.dict().get("email"),  # List of recipients
        body=email.content,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
