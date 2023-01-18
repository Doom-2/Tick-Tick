from django.contrib import admin
from .models import GoalCategory, Goal, GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'description', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'goal', 'user', 'created', 'updated')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
