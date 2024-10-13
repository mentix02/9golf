from django.contrib import admin

from score.models import Score, Session, SessionInvite


class ScoreInline(admin.TabularInline):
    extra = 0
    model = Score


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = (ScoreInline,)
    list_display_links = ('course',)
    list_display = ('id', 'course', 'timestamp', 'added_by')


@admin.register(SessionInvite)
class SessionInviteAdmin(admin.ModelAdmin):
    list_filter = ('role',)
    list_display = ('id', 'session', 'sent_by', 'sent_to', 'role', 'timestamp')
