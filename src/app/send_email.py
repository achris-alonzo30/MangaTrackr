import smtplib
import os

# Get email credentials from environment variables
EMAIL = "mangapickr@gmail.com"
PASSWORD = "ykom mqzf uhhn lkiu"


def send_manga_update(message_update, recipient_email):
    try:
        # Create an SMTP connection
        connection = smtplib.SMTP('smtp.gmail.com', port = 587)
        connection.starttls()  # Secure the connection
        connection.login(user = EMAIL, password = PASSWORD)

        # Compose the email
        subject = 'New Chapter Available'
        body = message_update
        message = f'Subject: {subject}\n\n{body}'

        # Send the email
        connection.sendmail(from_addr = EMAIL, to_addrs = recipient_email, msg = message)

        print("Email sent successfully")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
    finally:
        # Close the connection
        connection.quit()


# Example usage:
if __name__ == "__main__":
    recipient_email = "recipient@example.com"  # Replace with the recipient's email address
    message_update = "New manga chapter available!"

    send_manga_update(message_update, recipient_email)
