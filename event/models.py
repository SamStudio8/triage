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
        ordering = ('timestamp',)

    # Timestamp
    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(EventRecord, self).save(*args, **kwargs)

    def get_entry_slugs(self):
        field_entries = []
        for entry in self.eventrecordentry_set.all():
            record_entry = entry.get_record_entry().slugify(self)
            if record_entry:
               field_entries.append(record_entry)
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

#class EventLinkChange(models.Model):
#    pass

class EventFieldChange(models.Model):
    field = models.CharField(max_length=255)

    #TODO Is allowing null for these is as bad as I think it is?
    original = models.CharField(max_length=255, null=True, blank=True)
    new = models.CharField(max_length=255, null=True, blank=True)

    def slugify(self, event):
        s = ""
        if self.field not in event.get_object().RECORD_OPTIONS["invisible"]:
            if self.field.endswith("_id"):
                event_model = event.content_type.model_class()
                model_field = event_model._meta.get_field_by_name(self.field.replace("_id",""))

                related_model = model_field[0].rel.to

                try:
                    old_value = related_model.objects.get(pk=self.original)
                except related_model.DoesNotExist:
                    old_value = None

                try:
                    new_value = related_model.objects.get(pk=self.new)
                except related_model.DoesNotExist:
                    new_value = None

                s = "%s: %s -> %s" % (self.field, old_value, new_value)
            else:
                s = "%s: %s -> %s" % (self.field, self.original, self.new)

        return s
