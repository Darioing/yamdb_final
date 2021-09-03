import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def year_validator(value):
    """Валидатор для года"""

    if value < -3000 or value > datetime.datetime.now().year + 20:
        raise ValidationError(
            gettext_lazy('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
