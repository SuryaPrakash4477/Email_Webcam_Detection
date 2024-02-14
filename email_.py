import smtplib
from email.message import EmailMessage # This email class will create an email object instance
import imghdr # To take the type of the images or gives the metadata about the images

PASSWORD = "bavh uxve zpsa coel"
email_sender = "suryaprakashsharma453@gmail.com"
receiver_emails = "suryaprakashsharma453@gmail.com"

def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()

    # This object is behave like dictionary and we should provide values of diff. keys
    email_message["Subject"] = "New customer showed up!"
    
    #Email Body
    email_message.set_content("Hey, We just saw a new employee!")


    #Attachment of the Email
    with open(image_path, "rb") as file:
        content = file.read()
    
    email_message.add_attachment(content, maintype="image", subtype = imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo() # Giving some routines to start the email server parameters
    gmail.starttls()# It will encrypt our password
    gmail.login(email_sender, PASSWORD)

    # Method is used to send the email as string
    gmail.sendmail(email_sender, receiver_emails, email_message.as_string())
    gmail.quit()
    print("send_email  function ended")
    print("Mail Sent Successfully.")


if __name__ == "__main__":
    send_email(image_path = "images/25.png")