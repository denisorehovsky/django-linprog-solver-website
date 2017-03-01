from django import forms


class SimplexInitForm(forms.Form):
    coefficients_number = forms.TypedChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)], coerce=int
    )
    constraints_number = forms.TypedChoiceField(
        initial=3, choices=[(i, i) for i in range(1, 11)], coerce=int
    )
    is_non_negative = forms.BooleanField(initial=True, required=False)
