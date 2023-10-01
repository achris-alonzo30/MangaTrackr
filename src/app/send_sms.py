from twilio.rest import Client
import os


my_phone_number = os.environ.get("MY_PHONE_NUMBER")
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
os_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
os_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")


def send_sms(message_body, to_phone_number, from_phone_number):

    # Your Account SID and Auth Token from twilio.com/console
    account_sid = os_account_sid
    auth_token = os_auth_token

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_phone_number,
        from_=from_phone_number,
        body=message_body
    )

    print(f"SMS sent with SID: {message.sid}")


if __name__ == "__main__":
    # You can test the send_sms function here
    my_phone_number = my_phone_number
    twilio_phone_number = twilio_phone_number
    message_content = "This is a test message from your Python script."

    send_sms(message_content, my_phone_number, twilio_phone_number)
