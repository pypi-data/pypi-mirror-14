import logging
logger=logging.getLogger(__name__)

from django.conf import settings
from django.utils.safestring import mark_safe as S,mark_for_escaping as E
from django.template.loader import get_template
from django.template import Context

from . import FormPresentationItem

# preload paths to templates
BUTTON_TEMPLATE_PATH=settings.PRESENTATION['form']['buttonTemplatePath']


class Button(FormPresentationItem):
    def __init__(self,label,hidden=False):
        super(Button,self).__init__()
        self.label=label
        self.hidden=hidden


    def asHtml(self,presentation,form,viewMode=False):
        # override hidden if in view mode
        hidden=viewMode or self.isHidden(form)
        if hidden: return ''

        t=get_template(BUTTON_TEMPLATE_PATH)
        return t.render(Context(dict(widget=self.widgetHtml(presentation,form,hidden))))


    def widgetHtml(self,presentation,form,hidden=False):
        if hidden: return ''

        label=self.getLabel(form)
        return S('<input type="submit" class="formPresentation_button" name="{}" value="{}"/>'.format(E(self.name),label))
