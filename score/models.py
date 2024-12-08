from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Session(models.Model):

    # Used to keep a consistent name for the player count annotation
    PLAYER_COUNT_ANNOTATION = 'player_count'

    timestamp = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='sessions')
    added_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='created_sessions')
    users = models.ManyToManyField(
        'user.User',
        related_name='sessions',
        through='score.SessionUser',
        through_fields=('session', 'user'),
    )

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


class SessionUser(models.Model):

    joined_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.PLAYER)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_users')
    accepted_by = models.ForeignKey(
        'user.User',
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='accepted_users',
    )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.get_role_display()}'

    class Meta:
        unique_together = ('session', 'user', 'role')


class SessionJoinAction(models.Model):

    class ActionType(models.IntegerChoices):
        INVITE = 1, _('Invite')
        REQUEST = 2, _('Request')

    # Meta info
    timestamp = models.DateTimeField(auto_now_add=True)
    inactive = models.BooleanField(default=False, db_index=True)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.PLAYER)
    type_of = models.PositiveSmallIntegerField(choices=ActionType.choices, default=ActionType.INVITE)

    # Session
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='invites')

    # Users
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sent_invites')
    created_for = models.ForeignKey(
        'user.User', on_delete=models.SET_NULL, default=None, null=True, related_name='received_invites'
    )

    def deactivate(self):
        self.inactive = True
        self.save()

    def accept(self, by: User) -> bool:
        ActionType = self.__class__.ActionType

        match self.type_of:
            case ActionType.INVITE:
                # created_for and by must be the same user
                assert self.created_for == by, 'Cannot accept an invite that was not sent to you'
                self.session.users.add(
                    self.created_for, through_defaults={'role': self.role, 'accepted_by': self.created_by}
                )
            case ActionType.REQUEST:
                self.session.users.add(self.created_by, through_defaults={'role': self.role, 'accepted_by': by})
            case _:
                return False

        self.deactivate()
        return True

    class Meta:
        ordering = ('-timestamp',)
        unique_together = [('session', 'created_by')]


class Score(models.Model):

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='scores')
    hole = models.ForeignKey('course.Hole', on_delete=models.CASCADE, related_name='scores')

    strokes = models.PositiveSmallIntegerField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='scores')

    class Meta:
        unique_together = ('session', 'hole', 'user')
