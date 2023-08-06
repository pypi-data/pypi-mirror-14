"""
# editing questions
s=ss.addStyle('option.unknownValue')
s.fontWeight='bold'
s.color=ColourConstant('Black')
s=ss.addStyle('option.yesValue')
s.fontWeight='bold'
s.color=ColourConstant('Green')
s=ss.addStyle('option.noValue')
s.fontWeight='bold'
s.color=ColourConstant('Red')
"""
class StyledUnknownYesNoSelect(widgets.NullBooleanSelect):
    def render_option(self,selectedChoices,optionValue,optionLabel):
        optionValue=force_text(optionValue)

        selectedAttribute=''
        if optionValue in selectedChoices:
            selectedAttribute=S(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selectedChoices.remove(optionValue)
        classMap={'1':'unknownValue','2':'yesValue','3':'noValue'}
        classAttribute=classMap.get(optionValue,'')
        if classAttribute!='': classAttribute=S(' class="{}"'.format(classAttribute))
        return format_html('<option value="{}"{}{}>{}</option>',optionValue,classAttribute,selectedAttribute,force_text(optionLabel))
