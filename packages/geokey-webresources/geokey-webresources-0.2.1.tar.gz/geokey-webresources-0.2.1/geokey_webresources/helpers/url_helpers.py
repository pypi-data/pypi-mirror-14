"""All helpers for the URL."""

import urllib2

from mimetypes import MimeTypes

from ..base import FORMAT
from ..exceptions import URLError


def check_url(url):
    """
    Check if URL is accessible and what data format it is.

    Parameters
    ----------
    url : str
        URL to check.

    Returns
    -------
    str
        Data format of the URL.
    """
    dataformat = None
    response = None
    errors = []

    try:
        response = urllib2.urlopen(url)

        if response.headers.get('Access-Control-Allow-Origin') != '*':
            errors.append(
                'The server does not allow to use this URL externally. Make '
                'sure that CORS is enabled on the server.'
            )
        else:
            # Try to guess content type first
            content_type = MimeTypes().guess_type(url)[0]

            # If unsuccessful, get it from the headers
            if content_type is None:
                content_type = response.headers.get('Content-Type')

            if 'application/json' in content_type:
                dataformat = FORMAT.GeoJSON
            elif 'application/vnd.google-earth.kml+xml' in content_type:
                dataformat = FORMAT.KML
            else:
                errors.append('This data format is currently not supported.')
    except urllib2.URLError as error:
        if hasattr(error, 'code'):
            errors.append('The server returned %s error.' % error.code)
        if hasattr(error, 'reason'):
            errors.append('Failed to reach the server: %s.' % error.reason)

    if errors:
        raise URLError('The URL cannot be used due to:', errors)

    return dataformat
