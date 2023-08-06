from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES


class TypedChoiceField(forms.ChoiceField):
    """Better than Django's default TypedChoiceField which has some bugs or design inconsistencies."""

    def __init__(self,*args,**kwargs):
        self.coerce=kwargs.pop('coerce',lambda val:val)
        self.emptyValue=kwargs.pop('emptyValue','')
        super(TypedChoiceField,self).__init__(*args,**kwargs)


    def to_python(self,value):
        """
        Validates that the value is in self.choices and can be coerced to the right type.
        """
        if value==self.emptyValue or value in EMPTY_VALUES:
            return self.emptyValue

        try:
            value=self.coerce(value)
        except(ValueError,TypeError,ValidationError):
            raise ValidationError(self.error_messages['invalid_choice']%{'value':value})

        return value


    def validate(self,value):
        if self.required and value==self.emptyValue:
            raise ValidationError(self.error_messages['required'])

        # validate that value is in choices
        for k,v in self.choices:
            if isinstance(v,(list,tuple)):
                # This is an optgroup, so look inside the group for options
                for k2,v2 in v:
                    if value==k2:
                        return
            elif value==k:
                return

        raise ValidationError(self.error_messages['invalid_choice']%{'value':value})


    def prepare_value(self,value):
        try:
            return self.to_python(value)
        except ValidationError:
            return self.emptyValue
