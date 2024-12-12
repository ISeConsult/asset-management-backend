from apps.people.models import User
import pyotp
import time
from rest_framework.response import Response
import jwt
import arrow
from decouple import config
from django.core.cache import cache
from apps.people.utils import send_notification
import random
import pyotp
import qrcode
from django.db.models import Q
from io import BytesIO
import logging
logger = logging.getLogger(__name__)


class Authenticator:
    def generate_token(self, email):
        user = User.objects.get(email=email)
        payload = {
            "user_uid": str(user.uid),
            "user_id": user.id,
            "exp": arrow.utcnow().shift(days=30).datetime,
            "iat": arrow.utcnow().datetime,
        }
        token = jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        return token

    def generate_otp(self):
        rand = random.randint(10000, 99999)
        return rand

    def send_otp(self,email):
        try:
            otp = self.generate_otp()
            logger.info(otp)
            cache.set(email, otp,timeout=300)
            context = {
                'template':'otp',
                'context':{
                    'otp':otp
                }
            }
            mail = send_notification(recipient=email,context=context)
            logger.warning(mail)
            return otp
        except Exception as e:
            logger.warning(f"SMTPException: {str(e)}")
            return Response({"success": False, "info": "Error sending OTP via email"})



    # to be used for the forgot password verification
    def forgot_verify_otp(self, email, user_entered_otp):
        stored_otp = cache.get(email)
        logger.warning(stored_otp)
        if stored_otp is None:
            return Response({"success": False, "info": "Kindly click the resend button to continue"})
    
        user_otp = int(user_entered_otp)
        if stored_otp != user_otp:
            retries = cache.get(f"retries:{email}")
            if retries is None:
                retries = 0
            retries += 1
            cache.set(f"retries:{email}", retries)
    
            if retries > 4:
                logger.warning("Max retries reached")
                cache.delete(email)
                return Response({"success": False, "info": "Max retries reached, Kindly click the resend button to continue"})
            else:
                return Response({"success": False, "info": "Invalid OTP"})
    
        cache.delete(f"{email}")
        cache.delete(f"retries:{email}")  # Reset retries
        return Response({"success": True, "info": "email verified successfully"})
    
    

    def generate_authenticator_key(self):
        key = pyotp.random_base32()
        return key
    
    def get_totp_uri(self,user_id):
        issuer = config("TWO_FACTOR_ISSUER")
        user = User.objects.get(id=user_id)
        totp = pyotp.TOTP(user.authenticator_key)
        return totp.provisioning_uri(user.email, issuer_name=issuer)

    def generate_qr_code(self,user):
        uri = self.get_totp_uri(user)
        qr = qrcode.make(uri)
        stream = BytesIO()
        qr.save(stream, "PNG")
        return stream.getvalue()
    
    def verify_authenticator_key(self, field, code):
        user = User.objects.get(Q(email=field) | Q(phone_number=field))
        totp = pyotp.TOTP(user.authenticator_key)  
        return totp.verify(code)
    
    
    def generate_backup_codes(self):
        codes = []
        for i in range(10):
            code = pyotp.random_base32()
            codes.append(code)
        return codes
    








