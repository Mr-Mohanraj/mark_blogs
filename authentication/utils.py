import random
from django.conf import settings
import json
from django.core.mail import send_mail
import jwt


def send_activation_code(user, url):
    encode_data = generate_token(
        hide_data={"username": user.username}, key="activation key", mode='encode')
    send_mail(
        "For your activate account in mark_blogs",
        "activation click the link :" f"{url}user/{encode_data}/activation/",
        "mohanraj@markblogs.com",
        [user.email],
        fail_silently=True,
    )


def generate_token(key, mode, hide_data: dict = "", token="",):
    """mode: 'encode' for encode the values
            'decode' for decode the values
        key: 'secure key for encoding and decode'
        hide_data: what data you want to encode
        token: the encode the data
        ``` For decoding values are token,key```
        ``` For encode values are hide_data, key ```
        """
    if mode == 'encode':
        encoded_data = jwt.encode(hide_data, key, algorithm="HS256")
        return encoded_data
    elif mode == 'decode':
        decoded_data = jwt.decode(token, key, algorithms=['HS256'])
        return decoded_data


def password_forgot_mail(request, username, email, token):
    send_mail(
        'Your password change token',
        f"Click the link to verified to change your password {username} => {request.build_absolute_uri('/')}password/{token}/forgot/change/",
        'mohanraj@markblogs.com',
        [email],
        fail_silently=True,
    )
