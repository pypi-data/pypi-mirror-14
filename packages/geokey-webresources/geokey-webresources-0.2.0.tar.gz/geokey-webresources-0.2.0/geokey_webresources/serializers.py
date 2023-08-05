"""All serializers for the extension."""

from rest_framework.serializers import SerializerMethodField

from geokey.core.serializers import FieldSelectorSerializer

from .models import WebResource


class WebResourceSerializer(FieldSelectorSerializer):
    """Serializer for a web resource."""

    symbol = SerializerMethodField()

    def get_symbol(self, webresource):
        """
        Get URL of a symbol.

        Parameters
        ----------
        webresource : geokey_webresources.models.WebResource
            Web resource that is being serialised.
        """
        if webresource.symbol:
            return webresource.symbol.url

        return None

    class Meta:
        """Serializer meta."""

        model = WebResource
        fields = ('id', 'status', 'name', 'description', 'created', 'modified',
                  'dataformat', 'url', 'colour', 'symbol')
