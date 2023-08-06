from django.template import Library


register=Library()


@register.inclusion_tag('messages/messageBox.html')
def messageBox(messages):
    return {'messages':messages}
