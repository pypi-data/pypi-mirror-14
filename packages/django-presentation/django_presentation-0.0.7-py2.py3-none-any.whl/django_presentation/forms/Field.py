import logging
logger=logging.getLogger(__name__)

from django.conf import settings
from django.utils.html import format_html
from django.template.loader import get_template

from django_presentation.utils import specialInterpretValue

from . import FormPresentationItem

# preload paths to templates
FIELD_TEMPLATE_PATH=settings.PRESENTATION['form']['fieldTemplatePath']
ERRORS_TEMPLATE_PATH=settings.PRESENTATION['form']['errorsTemplatePath']


class Field(FormPresentationItem):
    """Presents a form field by calculating label, input and errors html and putting them all together with a template.
    The provided template wraps elements in container divs to allow considerable styling flexibility using only CSS.

    +---------------------------------------+
    | formPresentation_fieldContainer       |
    |  - label                              |
    | +------------------------------------+|
    | | formPresentation_inputContainer    ||
    | |  - errors                          ||
    | |  - widget (the input element)      ||
    | +------------------------------------+|
    +---------------------------------------+
    """
    def __init__(self,label='',hidden=False,
                 readonly=False,readonlyFormatter=None,
                 widget=None,widgetAttrs=None,
                 fieldContainerClasses='',templatePath=None):
        super(Field,self).__init__()
        self.label=label
        self.hidden=hidden

        self.readonly=readonly
        self.readonlyFormatter=readonlyFormatter

        self.widget=widget
        self.widgetAttrs=widgetAttrs

        self.fieldContainerClasses=fieldContainerClasses
        self.templatePath=templatePath if templatePath else FIELD_TEMPLATE_PATH


    def asHtml(self,presentation,form,viewMode=False):
        t=get_template(self.templatePath)
        # override readonly if in view mode
        readonly=viewMode or self.isReadonly(form)
        hidden=self.isHidden(form)

        return t.render({
            'fieldContainerClasses':' '+self.fieldContainerClasses if self.fieldContainerClasses else '',
            'label':self.labelHtml(presentation,form,readonly,hidden),
            'widget':self.widgetHtml(presentation,form,readonly,hidden),
            'errors':self.errorsHtml(presentation,form,readonly,hidden),
            'hidden':hidden,
            })


    def labelHtml(self,presentation,form,readonly=False,hidden=False):
        if readonly and hidden:
            # if readonly AND hidden - it's not really anything, is it...
            return ''

        label=self.getLabel(form)
        if readonly:
            return format_html('<label>{}</label>',label)

        else:
            return form[self.name].label_tag(label)


    def widgetHtml(self,presentation,form,readonly=False,hidden=False):
        if readonly and hidden:
            # if readonly AND hidden - it's not really anything, is it...
            return ''

        elif readonly:
            # readonly fields may not even be in the form and therefore may need to be read from the instance
            # handle nested attributes
            value=form.instance
            for a in self.name.split('.'):
                value=getattr(value,a)
            # if we have a function to format the readonly value, use it
            if self.readonlyFormatter is not None: value=self.readonlyFormatter(value)
            return format_html('{}',value)

        else:
            # format the input field
            # get attrs for the widget
            if self.widgetAttrs:
                attrs=specialInterpretValue(self.widgetAttrs,None,form).copy()
            elif self.widget and hasattr(self.widget,'attrs'):
                attrs=self.widget.attrs.copy()
            else:
                attrs={}

            # and add our own class
            attrs['class']=(attrs.get('class','')+' formPresentation_widget').strip()
            # and add another class if it has errors
            if form[self.name].errors:
                attrs['class']+=' errors'

            if hidden:
                return form[self.name].as_hidden(attrs=attrs)

            else:
                return form[self.name].as_widget(widget=self.widget,attrs=attrs)


    def errorsHtml(self,presentation,form,readonly=False,hidden=False):
        if readonly:
            return ''

        else:
            # format the errors
            errors=''
            if form[self.name].errors:
                errors=get_template(ERRORS_TEMPLATE_PATH).render({'errors':form[self.name].errors})
            return errors
