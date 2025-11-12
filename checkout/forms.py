from django import forms
from django_countries import countries
from django_countries.widgets import CountrySelectWidget

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'postcode', 'town_or_city', 'county', 'country',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔧 Completely override the country field with a normal ChoiceField
        # so we don't get a BlankChoiceIterator at all.
        self.fields['country'] = forms.ChoiceField(
            choices=[('', 'Country *')] + list(countries),
            required=True,
            widget=CountrySelectWidget(attrs={'class': 'stripe-style-input'}),
        )

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for name, field in self.fields.items():
            if name != 'country':
                placeholder = placeholders.get(name, '')
                if field.required and placeholder:
                    placeholder = f'{placeholder} *'
                field.widget.attrs.update({
                    'placeholder': placeholder,
                    'class': 'stripe-style-input',
                })
                field.label = False
            else:
                # Country: no placeholder text (the widget handles it), hide the label
                field.label = False
