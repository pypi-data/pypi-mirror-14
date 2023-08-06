import logging
logger=logging.getLogger(__name__)

from django.conf import settings
from django.template.loader import get_template
from django.template import Context

from . import FormPresentationItem


# preload paths to templates
ERRORS_TEMPLATE_PATH=settings.PRESENTATION['form']['errorsTemplatePath']

class ErrorMessages(FormPresentationItem):
    def asHtml(self,presentation,form,viewMode=False):
        if viewMode:
            return ''

        else:
            # format the errors
            errors=''
            es=form.non_field_errors() if self.name=='__all__' else form[self.name].errors
            if es:
                errors=get_template(ERRORS_TEMPLATE_PATH).render(Context({'errors':es}))
            return errors
