from django.forms.utils import flatatt
from django.utils.html import format_html
from wagtail.admin.edit_handlers import EditHandler


class ReadOnlyPanel(EditHandler):
    """
    ReadOnlyPanel EditHandler Class - built from ideas on
    https://github.com/wagtail/wagtail/issues/2893
    Most credit to @BertrandBordage for this.
    """

    def __init__(
        self,
        attr,
        *args,
        add_hidden_input=False,
        value=None,
        **kwargs
    ):
        self.attr = attr
        self.add_hidden_input = add_hidden_input
        super().__init__(*args, **kwargs)

    def get_value(self):
        value = getattr(self.instance, self.attr)
        if callable(value):
            value = value()
        return value

    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
            add_hidden_input=self.add_hidden_input,
            value=None,
        )

    def render(self):
        self.value = self.get_value()
        return format_html(
            '<div style="padding-top: 1.2em;">{}</div>',
            self.value,
        )

    def render_as_object(self):
        return format_html(
            (
                '<fieldset>'
                '<ul class="fields"><li><div class="field">{}</div></li></ul>'
                '</fieldset>'
            ),
            self.render()
        )

    def hidden_input(self):
        attrs = {
            'type': 'hidden',
            'name': self.attr,
            'value': self.value,
            'id': 'id_' + self.attr,
        }
        return f'<input{flatatt(attrs)}>'

    def heading_tag(self, tag):
        # add the label/legen tags only if heading supplied
        if self.heading:
            if tag == 'legend':
                return format_html('<legend>{}</legend>', self.heading)
            return format_html('<label>{}{}</label>', self.heading, ':')
        return ''

    def render_as_field(self):
        # render the final output
        return format_html(
            (
                '<div class="field">'
                '{}'
                '<div class="field-content">{}</div>'
                '{}'
                '</div>'
            ),
            self.heading_tag('label'),
            self.render(),
            self.hidden_input() if self.add_hidden_input else '',
        )
