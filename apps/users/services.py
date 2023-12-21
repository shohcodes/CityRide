import os
from random import randint

from dotenv import load_dotenv
from infobip_api_client.api.send_sms_api import SendSmsApi
from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.exceptions import ApiException
from infobip_api_client.model.sms_advanced_textual_request import SmsAdvancedTextualRequest
from infobip_api_client.model.sms_destination import SmsDestination
from infobip_api_client.model.sms_response import SmsResponse
from infobip_api_client.model.sms_textual_message import SmsTextualMessage

from apps.users.exceptions import ExpireActivationCodeException
from apps.users.models import SMS

load_dotenv()


def send_sms(phone_number):
    base_url = os.getenv('base_url')
    api_key = os.getenv('api_key')
    sender = os.getenv('sender')
    recipient = f'998{phone_number}'
    code = randint(111111, 999999)
    message_text = f"You code is: {code}. Do not share it with anyone!"
    client_config = Configuration(
        host=base_url,
        api_key={"APIKeyHeader": api_key},
        api_key_prefix={"APIKeyHeader": "App"},
    )
    api_client = ApiClient(client_config)
    sms_request = SmsAdvancedTextualRequest(
        messages=[
            SmsTextualMessage(
                destinations=[
                    SmsDestination(
                        to=recipient,
                    ),
                ],
                _from=sender,
                text=message_text,
            )
        ])
    api_instance = SendSmsApi(api_client)
    try:
        api_response: SmsResponse = api_instance.send_sms_message(sms_advanced_textual_request=sms_request)
        SMS.objects.create(phone_number=phone_number, code=code)
    except ApiException as ex:
        pass


def check_activation_code(phone_number, code):
    activation_code = SMS.objects.filter(phone_number=phone_number, is_used=False).last()
    if activation_code:
        if activation_code.expired:
            raise ExpireActivationCodeException
        if activation_code.code == code:
            activation_code.is_used = True
            activation_code.save(update_fields=["is_used"])
            return True
        return False
