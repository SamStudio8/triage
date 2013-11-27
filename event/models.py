import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import utc

class EventRecord(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ('-timestamp',)

    # Timestamp
    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(EventRecord, self).save(*args, **kwargs)

    #TODO This is bad and you should feel bad
    def get_field_entries(self):
        field_entries = []
        for entry in self.eventrecordentry_set.all():
            if entry.content_type == ContentType.objects.get(app_label="event", model="eventfieldchange"):
                record_entry = entry.get_record_entry()
                if record_entry.field not in self.get_object().RECORD_OPTIONS["invisible"]:
                    if record_entry.field.endswith("id"):
                        d_field = self.content_type.model_class()._meta.get_field_by_name(record_entry.field.replace("_id",""))
                        rel_model = d_field[0].rel.to
                        old_desc = rel_model.objects.get(pk=record_entry.original)
                        new_desc = rel_model.objects.get(pk=record_entry.new)

                        s = "%s: %s -> %s" % (record_entry.field, old_desc, new_desc)
                    else:
                        s = "%s: %s -> %s" % (record_entry.field, record_entry.original, record_entry.new)
                    field_entries.append(s)
        return field_entries

    def get_object(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

class EventRecordEntry(models.Model):
    event = models.ForeignKey(EventRecord)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def get_record_entry(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

class EventMemo(models.Model):
    reply_to = models.ForeignKey("EventMemo")
    memo = models.CharField(max_length=255)

class EventFieldChange(models.Model):
    field = models.CharField(max_length=255)
    original = models.CharField(max_length=255, blank=True)
    new = models.CharField(max_length=255, blank=True)

