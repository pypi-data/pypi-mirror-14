from django.utils.safestring import SafeText as S
from django.utils.six import with_metaclass

from . import FormPresentationItem,FormPresentationBoundItem


class FormPresentationMetaclass(type):
    """Metaclass to create items and form objects on the FormPresentation instance."""
    def __new__(meta,name,bases,attrs):
        # extract (and remove) any FormPresentationItem attributes on the class
        items=[(fn,attrs.pop(fn)) for fn,obj in list(attrs.items()) if isinstance(obj,FormPresentationItem)]
        # now sort by creationCounter to get the definition order
        items.sort(key=lambda x: x[1].creationCounter)
        # set the name on each item, unless it's already set
        for n,i in items:
            if i.name is None: i.setName(n)
        # and set the items attribute to a list of the FormPresentationItems in the defined order
        attrs['items']=[i for _,i in items]
        # continue with the class creation
        return super(FormPresentationMetaclass,meta).__new__(meta,name,bases,attrs)


class FormPresentation(with_metaclass(FormPresentationMetaclass,object)):
    def __init__(self,form,presentationAttributeOnForm=True,viewMode=False):
        self.form=form
        if presentationAttributeOnForm: self.form.presentation=self
        self.viewMode=viewMode
        # if there's a getItems method, get items from it instead
        if hasattr(self,'getItems'):
            self.items=self.getItems()


    def asHtml(self):
        # self.fieldLayoutTemplate
        s=[]
        for item in self.items:
            s.append(item.asHtml(self,self.form,viewMode=self.viewMode))
        return S(''.join(s))


    def __getattr__(self,name):
        """If a physical attribute doesn't exist, check in self.items and return a bound item that provides presentation and form instances to function calls.
        This is used in templates when presenting individual items, like so: {{presentation.description.labelHtml}}
        """
        for item in self.items:
            if item.name==name:
                return FormPresentationBoundItem(self,self.form,item)
        raise AttributeError()


    # ----------------------------------------
    # Helper functions
    # ----------------------------------------
    @staticmethod
    def isNewInstance(form):
        return form.instance.pk is None

    @staticmethod
    def isExistingInstance(form):
        return not FormPresentation.isNewInstance(form)
