from celery import shared_task


@shared_task
def send_otp_task(phone, code):

    print(
        f"Sending OTP {code} to {phone}"
    )


 

    return True