from event import models as EventModels
from django.contrib.contenttypes.models import ContentType

def FieldChange(request, old, new):
    # Naughty as this assumes the save was successful for now as I can't
    # think of a way to do it without messy signals or having to save a
    # deep copy of the object
    if old and old.pk is not None:
        event = None

        for field, new_data in new.__dict__.iteritems():
            if field[0] == "_":
                continue

            old_data = old.__dict__.get(field)
            if old_data != new_data:
                if event is None:
                    # New historical event record
                    event = EventModels.EventRecord(
                            content_type=ContentType.objects.get_for_model(old),
                            object_id=old.pk,
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

def LinkChange(request, link):
    # New historical event records
    from_event = EventModels.EventRecord(
            content_type=ContentType.objects.get_for_model(link.from_task),
            object_id=link.from_task.pk,
            user_id=request.user.id
    )
    from_event.save()

    to_event = EventModels.EventRecord(
            content_type=ContentType.objects.get_for_model(link.to_task),
            object_id=link.to_task.pk,
            user_id=request.user.id
    )
    to_event.save()

    # Create link change events
    from_desc = "%s %d: %s" % (link.link_type.from_desc,
                               link.from_task.pk,
                               link.from_task.name)
    to_desc = "%s %d: %s" % (link.link_type.to_desc,
                             link.to_task.pk,
                             link.to_task.name)

    from_change = EventModels.EventLinkChange(
            description=to_desc
    )
    from_change.save()

    to_change = EventModels.EventLinkChange(
            description=from_desc
    )
    to_change.save()

    # Attach field change to event record
    from_entry = EventModels.EventRecordEntry(
            event_id=from_event.pk,
            content_type=ContentType.objects.get_for_model(from_change),
            object_id=from_change.pk
    )
    from_entry.save()

    to_entry = EventModels.EventRecordEntry(
            event_id=to_event.pk,
            content_type=ContentType.objects.get_for_model(to_change),
            object_id=to_change.pk
    )
    to_entry.save()

