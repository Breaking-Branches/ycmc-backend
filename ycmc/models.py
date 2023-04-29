from django.db import models
from datetime import datetime
import uuid

# Create your models here.
class DetectInformation(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date =   models.DateTimeField(auto_now_add=True)
    repo1 = models.URLField()
    repo2 = models.URLField()
    data  = models.JSONField()

