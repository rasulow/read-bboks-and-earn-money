import requests
from django.conf import settings


def send_otp(phone_number, otp):
    # url = f'https://2factor.in/API/V1/{settings.SMS_API_KEY}/SMS/{phone_number}/{otp}/Your OTP is'
    # payload = ''
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }

    # response = requests.get(url, data=payload, headers=headers)
    print('Your otp is:', otp)
    
    # return bool(response.ok)