from django.contrib import admin

from .models import DataPooling, Measurement


class MeasurementInline(admin.TabularInline):
    model = Measurement


@admin.register(DataPooling)
class DataPoolingAdmin(admin.ModelAdmin):
    list_display = ('observer', 'last_value', 'last_time')
    inlines = [MeasurementInline]

    def last_value(self, instance):
        if not instance.last_measurement:
            return None

        return instance.last_measurement
    last_value.short_description = 'Last measurement'

    def last_time(self, instance):
        if not instance.last_time:
            return None

        return instance.last_time
    last_time.short_description = 'Time of measurement'
