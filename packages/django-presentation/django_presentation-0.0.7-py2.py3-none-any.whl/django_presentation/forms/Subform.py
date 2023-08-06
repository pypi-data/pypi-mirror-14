import logging
logger=logging.getLogger(__name__)

from . import FormPresentationItem


class Subform(FormPresentationItem):
    def __init__(self):
        super(Subform,self).__init__()


    def asHtml(self,presentation,form,viewMode=False):
        return getattr(form,self.name).presentation.asHtml()
