import random
import logging

from django.core.cache import cache


logger = logging.getLogger(__name__)


OTP_EXPIRE_TIME = 120  # 2 minutes

OTP_LIMIT_TIME = 60  # 1 minute

OTP_PREFIX = "otp"



class OTPService:



    @staticmethod
    def generate_code():

        return str(
            random.randint(
                100000,
                999999
            )
        )



    @staticmethod
    def get_key(phone):

        return f"{OTP_PREFIX}:{phone}"



    @classmethod
    def send_otp(cls, phone):

        key = cls.get_key(phone)


        # جلوگیری از درخواست زیاد

        if cache.get(
            f"{key}:limit"
        ):

            return {
                "success": False,
                "message":
                "Please wait before requesting another code"
            }



        code = cls.generate_code()



        # ذخیره OTP در Redis

        cache.set(
            key,
            code,
            timeout=OTP_EXPIRE_TIME
        )



        # محدودیت ارسال مجدد

        cache.set(
            f"{key}:limit",
            True,
            timeout=OTP_LIMIT_TIME
        )



        # فعلا جایگزین SMS
        # بعدا اینجا کاوه نگار + Celery می‌آید

        logger.warning(
            f"OTP for {phone}: {code}"
        )



        return {

            "success": True,

            "message":
            "OTP sent successfully"

        }





    @classmethod
    def verify_otp(cls, phone, code):

        key = cls.get_key(phone)


        saved_code = cache.get(
            key
        )



        if not saved_code:

            return False



        if str(saved_code) != str(code):

            return False



        # حذف بعد از استفاده

        cache.delete(
            key
        )



        return True
    









