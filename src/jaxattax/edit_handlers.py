from django.utils.html import format_html
from wagtail.admin.edit_handlers import EditHandler


class ReadOnlyPanel(EditHandler):
    """ ReadOnlyPanel EditHandler Class - built from ideas on https://github.com/wagtail/wagtail/issues/2893
        Most credit to @BertrandBordage for this.
        Usage:
        attr:               name of field to display
        style:              optional, any valid style string
        add_hidden_input:   optional, add a hidden input field to allow retrieving data in form_clean (self.data['field'])
        If the field name is invalid, or an error is received getting the value, empty string is returned.
        """
    def __init__(self, attr, style=None, add_hidden_input=False, *args, value=None, **kwargs):
        # error if attr is not string
        if type(attr)=='str':
            self.attr = attr
        else:
            try:
                self.attr = str(attr)
            except:
                pass
        self.style = style
        self.add_hidden_input = add_hidden_input
        super().__init__(*args, **kwargs)

    def get_value(self):
        # try to get the value of field, return empty string if failed
        try:
            value = getattr(self.instance, self.attr)
            if callable(value):
                value = value()
        except AttributeError:
            value = ''
        return value
        
    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
            style=self.style,
            add_hidden_input=self.add_hidden_input,
            value=None,
        )

    def render(self):
        # return formatted field value
        self.value = self.get_value()
        return format_html('<div style="padding-top: 1.2em;">{}</div>', self.value)

    def render_as_object(self):
        return format_html(
            '<fieldset>'
            '<ul class="fields"><li><div class="field">{}</div></li></ul>'
            '</fieldset>',
            self.render())

    def hidden_input(self):
        # add a hidden input field if selected, field value can be retrieved in form_clean with self.data['field']
        if self.add_hidden_input:
            input = f'<input type="hidden" name="{self.attr}" value="{self.value}" id="id_{self.attr}">'
            return format_html(input)
        return ''

    def heading_tag(self, tag):
        # add the label/legen tags only if heading supplied
        if self.heading:
            if tag == 'legend':
                return format_html('<legend>{}</legend>', self.heading)
            return format_html('<label>{}{}</label>', self.heading, ':')
        return ''

    def get_style(self):
        # add style if supplied
        if self.style:
            return format_html('style="{}"', self.style)
        return ''

    def render_as_field(self):
        # render the final output
        return format_html(
            '<div class="field" {}>'
            '{}'
            '<div class="field-content">{}</div>'
            '{}'
            '</div>',
            format_html(self.get_style()), self.heading_tag('label'), self.render(), self.hidden_input())  
