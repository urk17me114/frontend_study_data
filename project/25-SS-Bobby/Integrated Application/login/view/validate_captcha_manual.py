
"""
Author: Glen Paul

Functionality:
--------------
This module provides a manual CAPTCHA validation function for verifying 
user-submitted CAPTCHA responses against the stored CAPTCHA entry in 
Django's CaptchaStore.


"""




from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def validate_captcha_manual(captcha_id, captcha_response):
    try:
        captcha = CaptchaStore.objects.get(hashkey=captcha_id)
        
        if not captcha_response.isupper():
            return False

        return captcha.response == captcha_response.lower()
    except CaptchaStore.DoesNotExist:
        return False