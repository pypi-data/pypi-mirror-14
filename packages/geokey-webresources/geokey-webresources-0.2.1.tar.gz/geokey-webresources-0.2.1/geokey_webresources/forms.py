"""All forms for the extension."""

from django.forms import ModelForm

from .models import WebResource


class WebResourceForm(ModelForm):
    """Form for a single web resource."""

    class Meta:
        """Form meta."""

        model = WebResource
        fields = ('name', 'description', 'url', 'colour', 'symbol')
