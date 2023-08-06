from django.forms import widgets
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe as S



class ChoicesRadioSelect(widgets.Widget):
    def __init__(self,choices,*args,**kwargs):
        super(self.__class__,self).__init__(*args,**kwargs)
        self.choices=choices


    def render(self,name,value,attrs=None):
        s=[]
        for c in self.choices:
            extraAttrs=attrs.copy()
            extraAttrs.update(dict(type='radio',name=name,value=c[0]))
            if value==c[0]: extraAttrs['checked']='checked'
            extraAttrs=self.build_attrs(extraAttrs)
            s.append(format_html('<label><input {}/>{}</label>',flatatt(extraAttrs),c[1]))
        return S(''.join(s))


    def getChoiceText(self,value):
        # return the first match
        for c in self.choices:
            if c[0]==value:
                return c[1]
        return value
