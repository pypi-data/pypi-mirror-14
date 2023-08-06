from django.db import models


class PublishedQueryset(models.query.QuerySet):

    def published(self):
        return self.exclude(live_url='').filter(publish=True)


class StacksPageModelManager(models.Manager):

    def get_queryset(self):
        return PublishedQueryset(self.model)


class StacksPageModelManagerPublishedModelManager(StacksPageModelManager):
    """

    """
    def get_queryset(self):
        return super(
            StacksPageModelManagerPublishedModelManager, self
        ).get_queryset().published()
