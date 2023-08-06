import logging

from django.db import models
from django.dispatch import receiver

from howl.models import Alert, Observer
from howl.signals import alert_clear, alert_notify, alert_wait


logger = logging.getLogger(__name__)


def prepare_message(obj):
    return '{0}>> {1} - {2} >>{3}<<'.format(
        obj.get_state_display().upper(),
        obj.observer,
        obj.timestamp,
        obj.value,
    )


@receiver(alert_wait, sender=Alert)
def send_warning(sender, instance, **kwargs):
    logger.debug(prepare_message(instance))


@receiver(alert_notify, sender=Alert)
def send_alert(sender, instance, **kwargs):
    logger.debug(prepare_message(instance))


@receiver(alert_clear, sender=Alert)
def send_clear(sender, instance, **kwargs):
    message = '<<<<OK>>>> {0} - {1}'.format(
        instance.observer,
        instance.timestamp,
    )
    logger.debug(message)


class DataPooling(models.Model):
    observer = models.ForeignKey(Observer)

    @property
    def last_measurement(self):
        if not self.measurement_set.first():
            return None

        return self.measurement_set.first().value

    @property
    def last_time(self):
        if not self.measurement_set.first():
            return None

        return self.measurement_set.first().timestamp


class Measurement(models.Model):
    datapooling = models.ForeignKey(DataPooling)
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
