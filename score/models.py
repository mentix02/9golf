from django.db import models
from django.utils.translation import gettext_lazy as _


class Session(models.Model):

    # Used to keep a consistent name for the player count annotation
    PLAYER_COUNT_ANNOTATION = 'player_count'

    timestamp = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField('user.User', through='SessionUser', related_name='sessions')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='sessions')
    added_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='created_sessions')

    def __str__(self) -> str:
        return f'{self.course.name} #{self.id}'

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            self.users.add(self.added_by, through_defaults={'role': Role.ADMIN})
        else:
            super().save(*args, **kwargs)

    class Meta:
        ordering = ('-timestamp',)


class Role(models.IntegerChoices):
    PLAYER = 1, _('Player')
    CAN_INVITE = 2, _('Can Invite')
    ADMIN = 3, _('Admin')


class SessionInviteType(models.IntegerChoices):
    INVITE = 1, _('Invite')
    REQUEST = 2, _('Request')


class SessionUser(models.Model):

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.PLAYER)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_users')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.get_role_display()}'

    class Meta:
        unique_together = ('session', 'user')


class SessionInvite(models.Model):

    # Meta info
    timestamp = models.DateTimeField(auto_now_add=True)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.PLAYER)
    type_of = models.PositiveSmallIntegerField(choices=SessionInviteType.choices, default=SessionInviteType.INVITE)

    # Session
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='invites')

    # Users
    sent_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sent_invites')
    sent_to = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='received_invites')

    class Meta:
        ordering = ('-timestamp',)
        unique_together = ('session', 'sent_to')


class Score(models.Model):

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='scores')
    hole = models.ForeignKey('course.Hole', on_delete=models.CASCADE, related_name='scores')

    strokes = models.PositiveSmallIntegerField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='scores')

    class Meta:
        unique_together = ('session', 'hole', 'user')
