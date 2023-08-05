"""Base for the extension."""

from model_utils import Choices


STATUS = Choices('active', 'inactive', 'deleted')
FORMAT = Choices('GeoJSON', 'KML')
