from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class ExpireActivationCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Activation code is expired!")


class IncorrectActivationCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Activation code is incorrect!')


class PermissionDeniedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You have not access to this action!')
