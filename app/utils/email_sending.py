import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from app.core.config import settings


def send_email_message(to_addr: str, subject: str, html_template: str):

    try:
        message = MIMEMultipart()
        message["From"] = formataddr(("Услуги в кармане", settings.SMTP_LOGIN))
        message["To"] = to_addr
        message["Subject"] = subject
        message.attach(MIMEText(html_template, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
        server.send_message(message)
        server.quit()

        return True
    except Exception:
        return False


def get_code_html_template(code: str):
    html_template = """
                <html>
                    <body>
                        <p>
                            Здравствуйте!
                            <br>
                            <br>
                            Вы отправили запрос на подтверждение почтового адреса.
                            <br>
                            <br>
                            Ваш код:
                            <br>
                            <br>
                            <strong>{code}</strong>
                            <br>
                            <br>
                            С уважением Услуги в кармане.
                        </p>
                    </body>
                </html>
                """.format(code=code)
    return html_template


def get_code_refresh_password_html_template(code: str):
    html_template = """
                <html>
                    <body>
                        <p>
                            Здравствуйте!
                            <br>
                            <br>
                            Вы отправили запрос на восстановление пароля.
                            <br>
                            <br>
                            Ваш код:
                            <br>
                            <br>
                            <strong>{code}</strong>
                            <br>
                            <br>
                            С уважением Услуги в кармане.
                        </p>
                    </body>
                </html>
                """.format(code=code)
    return html_template