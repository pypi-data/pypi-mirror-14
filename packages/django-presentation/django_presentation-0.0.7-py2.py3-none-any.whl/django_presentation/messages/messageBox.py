from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe as S


def messageBox(messages):
    return S(get_template('messages/messageBox.html').render(Context({'messages':messages})))
