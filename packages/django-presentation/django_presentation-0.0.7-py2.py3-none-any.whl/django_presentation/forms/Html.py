import logging
logger=logging.getLogger(__name__)

from . import FormPresentationItem


class Html(FormPresentationItem):
    def __init__(self,html,hidden=False):
        super(Html,self).__init__()
        self.html=html
        self.hidden=hidden


    def asHtml(self,presentation,form,viewMode=False):
        if self.isHidden(form): return ''
        return self.html
