"""All exceptions for the extension."""

from django.utils.safestring import mark_safe


class URLError(Exception):
    """Throw URL error."""

    def __init__(self, message, errors):
        """Initialise error messages."""
        self.message = message
        self.errors = errors

    def to_html(self):
        """Convert error messages to HTML."""
        html = '<p>%s</p>' % self.message

        html += '<ul>'
        for error in self.errors:
            html += '<li>%s</li>' % error
        html += '</ul>'

        return mark_safe(html)
