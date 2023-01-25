from django.contrib import admin
from .models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'description', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'goal', 'user', 'created', 'updated')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    search_fields = ('title', )


class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('board', 'user', 'role', 'created', 'updated')
    search_fields = ('board', 'user', 'role')


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(BoardParticipant, BoardParticipantAdmin)
