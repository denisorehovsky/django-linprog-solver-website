from django import forms


class SimplexInitForm(forms.Form):
    coefficients_number = forms.TypedChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)], coerce=int
    )
    constraints_number = forms.TypedChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)], coerce=int
    )
    is_non_negative = forms.BooleanField(initial=True, required=False)


class SimplexCoefficientsForm(forms.Form):
    tendency = forms.ChoiceField(initial='max',
                                 choices=[('max', 'max'), ('min', 'min')])

    def __init__(self, coefficients_number, *args, **kwargs):
        super().__init__(*args, **kwargs)

        coefficients_number = int(coefficients_number)
        for number in range(1, coefficients_number+1):
            field_name = 'coefficient_{}'.format(number)
            self.fields[field_name] = forms.FloatField()
