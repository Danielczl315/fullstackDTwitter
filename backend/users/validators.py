# python imports
import re 
# django imports
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(username):
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        raise ValidationError( _(
            'Enter a valid username. This value may contain only English letters, '
            'numbers and underscores.'
        )) 