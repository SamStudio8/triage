from event import models as EventModels
from django.contrib.contenttypes.models import ContentType

def _get_history(obj):
    return EventModels.EventRecord.objects.filter(
            object_id=obj.pk,
            content_type=ContentType.objects.get_for_model(obj)
    )

def _eventful(request, old, new):
    # Naughty as this assumes the save was successful for now as I can't
    # think of a way to do it without messy signals or having to save a
    # deep copy of the object
    if new.pk is not None:
        event = None

        for field, new_data in new.__dict__.iteritems():
            if field[0] == "_":
                continue

            old_data = old.__dict__.get(field)
            print field, new_data, old_data
            if old_data != new_data:
                if event is None:
                    # New historical event record
                    event = EventModels.EventRecord(
                            content_type=ContentType.objects.get_for_model(new),
                            object_id=new.pk,
                            user_id=request.user.id
                    )
                    event.save()

                # Create field change event
                change = EventModels.EventFieldChange(
                        field=field,
                        original=old_data,
                        new=new_data
                )
                change.save()

                # Attach field change to event record
                entry = EventModels.EventRecordEntry(
                        event_id=event.pk,
                        content_type=ContentType.objects.get_for_model(change),
                        object_id=change.pk
                )
                entry.save()

