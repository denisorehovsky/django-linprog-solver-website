from django import forms


class SimplexInitForm(forms.Form):
    variables = forms.ChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)]
    )
    conditions = forms.ChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)]
    )
    is_non_negative = forms.BooleanField(initial=True, required=False)


class SimplexCoefficientsForm(forms.Form):
    tendency = forms.ChoiceField(initial='max',
                                 choices=[('max', 'max'), ('min', 'min')])

    def __init__(self, variables, *args, **kwargs):
        super().__init__(*args, **kwargs)

        variables = int(variables)
        for number in range(1, variables + 1):
            field_name = 'variable_{}'.format(number)
            self.fields[field_name] = forms.FloatField()
