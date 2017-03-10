from django.forms import CheckboxInput, Widget
from django.forms.widgets import boolean_check


class RightCheckbox(Widget):
    render = CheckboxInput().render

    def __init__(self, attrs=None, check_test=None):
        super(RightCheckbox, self).__init__(attrs)
        self.check_test = boolean_check if check_test is None else check_test
