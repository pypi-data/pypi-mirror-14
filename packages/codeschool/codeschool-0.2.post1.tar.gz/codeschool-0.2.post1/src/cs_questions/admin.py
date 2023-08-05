import copy
from django.contrib import admin
from cs_questions import models


class QuestionBase(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('title', 'short_description', 'author_name', '_has_comment')
    list_filter = ('author_name', 'timestamp')
    fieldsets = (
        (None, {
            'fields': (('title', 'author_name'),
                       'discipline',
                       'short_description', 'long_description',),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('comment',),
        }),

    )
    save_as = True
    save_on_top = True
    search_fields = (
        'title',
        'author_name',
        'short_description',
        'comment',
    )

    @staticmethod
    def _has_comment(obj):
        return bool(obj.comment)


@admin.register(models.CodeIoQuestion)
class CodeIoQuestionAdmin(QuestionBase):
    # Inline models
    class AnswerKeyInline(admin.StackedInline):
        model = models.CodeIoAnswerKey
        extra = 0
        fieldsets = (
            (None, {
                'fields': ('language', 'source_code'),
            }),
            ('Advanced', {
                'classes': ('collapse',),
                'fields': ('placeholder', 'response_template_extra'),
            }),

        )

    inlines = [AnswerKeyInline]

    # Overrides and other configurations
    list_display = QuestionBase.list_display + ('timeout',)
    fieldsets = copy.deepcopy(QuestionBase.fieldsets)
    fieldsets[0][1]['fields'] += ('response_template',)
    fieldsets[1][1]['fields'] += ('timeout',)


admin.site.register(models.QuestionActivity)
admin.site.register(models.CodeIoActivity)
admin.site.register(models.CodeIoFeedback)