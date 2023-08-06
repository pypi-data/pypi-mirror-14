

class FormPresentationBoundItem(object):
    """Binds an item to presentation and form instances so that function calls to eg. asHtml or labelHtml (on a Field) can provide the required parameters."""
    def __init__(self,presentation,form,item):
        self.presentation=presentation
        self.form=form
        self.item=item

    def __getattr__(self,name):
        i=getattr(self.item,name)
        if callable(i):
            def partial(*args,**kwargs):
                return i(self.presentation,self.form,*args,**kwargs)
            return partial
        return i
