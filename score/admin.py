from django.contrib import admin

from score.models import Score, Session, SessionJoinAction


class ScoreInline(admin.TabularInline):
    extra = 0
    model = Score


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = (ScoreInline,)
    list_display_links = ('course',)
    list_display = ('id', 'course', 'timestamp', 'added_by')


@admin.register(SessionJoinAction)
class SessionInviteAdmin(admin.ModelAdmin):
    list_filter = ('role',)
    list_display = ('id', 'session', 'created_by', 'created_for', 'role', 'timestamp')
