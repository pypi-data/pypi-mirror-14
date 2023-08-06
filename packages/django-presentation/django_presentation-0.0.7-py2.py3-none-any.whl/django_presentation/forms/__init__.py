import django.apps

class AppConfig(django.apps.AppConfig):
    name='django_presentation.forms'
    label='django_presentation_forms'


from .FormPresentationItem import FormPresentationItem
from .FormPresentationBoundItem import FormPresentationBoundItem
from .Field import Field
from .ErrorMessages import ErrorMessages
from .Button import Button
from .Html import Html
from .Subform import Subform

from .FormPresentation import FormPresentation
