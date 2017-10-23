from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django.contrib.sites.models import Site

from config_models.models import ConfigurationModel


EXPERIENCE_TYPES = (
    (0, 'Recurring Nudge and Upgrade Reminder'),
    (1, 'Course Updates'),
)
DEFAULT_EXPERIENCE_TYPE = EXPERIENCE_TYPES[0][0]


class Schedule(TimeStampedModel):
    enrollment = models.OneToOneField('student.CourseEnrollment', null=False)
    active = models.BooleanField(
        default=True,
        help_text=_('Indicates if this schedule is actively used')
    )
    start = models.DateTimeField(
        db_index=True,
        help_text=_('Date this schedule went into effect')
    )
    upgrade_deadline = models.DateTimeField(
        blank=True,
        db_index=True,
        null=True,
        help_text=_('Deadline by which the learner must upgrade to a verified seat')
    )

    def get_experience_type(self):
        if (hasattr(self, 'experience')):
            return self.experience.experience_type
        else:
            return DEFAULT_EXPERIENCE_TYPE

    class Meta(object):
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')


class ScheduleConfig(ConfigurationModel):
    KEY_FIELDS = ('site',)

    site = models.ForeignKey(Site)
    create_schedules = models.BooleanField(default=False)
    enqueue_recurring_nudge = models.BooleanField(default=False)
    deliver_recurring_nudge = models.BooleanField(default=False)
    enqueue_upgrade_reminder = models.BooleanField(default=False)
    deliver_upgrade_reminder = models.BooleanField(default=False)
    enqueue_course_update = models.BooleanField(default=False)
    deliver_course_update = models.BooleanField(default=False)


class ScheduleExperience(models.Model):
    schedule = models.OneToOneField(Schedule, related_name='experience')
    experience_type = models.IntegerField(choices=EXPERIENCE_TYPES, default=DEFAULT_EXPERIENCE_TYPE)
