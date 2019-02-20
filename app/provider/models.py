from django.db import models
from datetime import datetime
from django.utils.module_loading import import_string
from django.contrib.postgres.fields import JSONField


class Provider(models.Model):
    STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS, default='active')
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_provider_object(self, file_name, class_name):
        path_ = f'app.provider.{file_name}.{self.name}.{class_name}'
        import_ = import_string(path_)
        return import_

    @property
    def get_client(self):
        return self.get_provider_object('clients', 'Client')

    @property
    def get_adapter(self):
        return self.get_provider_object('adapters', 'Adapter')

    class Meta:
        db_table = 'provider'

    def __str__(self):
        return self.name
