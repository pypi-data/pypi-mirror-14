"""All managers for the extension."""

from django.db import models

from .base import STATUS


class WebResourceManager(models.Manager):
    """Manage a single web resource."""

    def get_queryset(self):
        """
        Return all web resources.

        Returns
        -------
        django.db.models.Queryset
            All web resources, excluding deleted.
        """
        return super(
            WebResourceManager,
            self
        ).get_queryset().exclude(status=STATUS.deleted)
