from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('37494C384F6357775A4E61513075726B304841414175316D774A3567564E386956467669344274645A46733D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'Your confirmation code is: {code}'
        }
        response = api.sms_send(params)
        print(response)

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)



