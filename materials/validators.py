import re

from rest_framework.exceptions import ValidationError


class URLValidate:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field_value = value.get(self.field)

        if not field_value:
            return

        youtube_pattern = re.compile("^https://www.youtube.com/")
        if not youtube_pattern.match(field_value):
            raise ValidationError("Разрешены только ссылки на YouTube")
