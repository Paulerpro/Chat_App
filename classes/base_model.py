from django.db import models
import uuid

STATUS_CHOICES = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
    ("DELETED", "DELETED"),
)

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)  
    unique_id = models.UUIDField(max_length=36, default=uuid.uuid4, editable=False, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES, blank=False, null=False, default='ACTIVE', max_length=100
        )
    meta = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        abstract = True