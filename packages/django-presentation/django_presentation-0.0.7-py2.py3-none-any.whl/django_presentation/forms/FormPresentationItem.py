from django.utils.safestring import SafeText as S

from django_presentation.utils import specialInterpretValue


class FormPresentationItem(object):
    creationCounter=0

    def __init__(self):
        self.creationCounter=FormPresentationItem.creationCounter
        FormPresentationItem.creationCounter+=1

        self.name=None


    def setName(self,name):
        """Called when a FormPresentation instance is being created to set the name from the attribute name.
        Returns self so that name can be set in the same line as creating the FormPresentationItem instance:
            fieldName=Field().setName(getDynamicName())
        """
        self.name=name
        return self


    def getLabel(self,form):
        """A label can be a string, dict (lookup by name) or a callable (passed the form)."""
        return specialInterpretValue(self.label,self.name,form=form)

    def isHidden(self,form):
        return specialInterpretValue(self.hidden,None,form)

    def isReadonly(self,form):
        return specialInterpretValue(self.readonly,None,form)


    def asHtml(self,presentation,form):
        raise NotImplemented('Must be implemented in derived classes')
