from event import models as EventModels
from django.contrib.contenttypes.models import ContentType

def _get_history(obj):
    return EventModels.EventRecord.objects.filter(
            object_id=obj.pk,
            content_type=ContentType.objects.get_for_model(obj)
    )

