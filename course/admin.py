from django.contrib import admin

from course.models import Course, Hole


class HoleInline(admin.TabularInline):
    extra = 1
    min_num = 2
    model = Hole


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [HoleInline]
    search_fields = ('name',)
    list_filter = ('is_public',)
    list_display = ('name', 'added_by', 'is_public', 'added_on')
