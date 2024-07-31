from django import forms

class donate(forms.Form):
    choice = (
        ("Khushi Foundation", "Khushi Foundation"),
        ("Desire Society", "Desire Society"),
        ("Safe Nation Foundation", "Safe Nation Foundation"),
        ("Tare Zameen Foundation", "Tare Zameen Foundation"),
        ("Us", "Directly to us")
    )

    name = forms.CharField(
        max_length=225,
        widget=forms.TextInput(attrs={'id': 'name'})
    )
    NGO = forms.ChoiceField(
        choices=choice,
        widget=forms.Select(attrs={'id': 'donateto'})
    )
    donation = forms.IntegerField(
        widget=forms.NumberInput(attrs={'id': 'donation'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'comment'})
    )
    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if not cleaned_data.get(field) and field not in self._errors:
                self._errors[field] = self.error_class([f"{self.fields[field].label} is required."])
        return cleaned_data