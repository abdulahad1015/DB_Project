from smtplib import SMTP
import os
from pyotp import TOTP
from dotenv import load_dotenv
load_dotenv()

def send_otp():
    # my_email = "abdulahad1015@gmail.com"
    # password = os.getenv("EMAIL_APP_PASSWORD")
    # print(password)
    # connection = SMTP("smtp.gmail.com", port=587)
    # connection.starttls()
    # connection.login(user=my_email, password=password)
    otp=TOTP('WasssUpNigga')
    otp = otp.now()
    # connection.sendmail(
    #     from_addr=my_email,
    #     to_addrs="k224353@nu.edu.pk",
    #     msg=f"Subject: Your OTP\n\nYour OTP is {otp}"
    # )
    # connection.quit()
    print(otp)
    return otp
