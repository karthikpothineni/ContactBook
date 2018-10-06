from __future__ import unicode_literals

from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField('date joined ', auto_now_add=True)
    updated_at = models.DateTimeField('date modified', auto_now=True)
    soft_delete = models.BooleanField('soft delete', default=False)

    class Meta:
        abstract = True
        app_label = 'orders'
