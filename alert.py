import smtplib
from email.message import EmailMessage


def send_alert(subject, body, to):
    # Must have 2-factor authentication setup through gmail
    # with an app password

    # Sender
    user = "duhwhiteshroot@gmail.com"
    password = "mzhfyfvzzplbazpc"

    # Create message
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user

    # Gmail server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # Required
    server.starttls()
    # Login
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    print("Sent alert!")


# if __name__ == '__main__':

    # send_alert("", "", bradegbert26@gmail.com)

    # In order to send a text message, [insert 10-digit number]@txt.att.net
    # https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/
