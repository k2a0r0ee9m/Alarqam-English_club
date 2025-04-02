from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(USER)
admin.site.register(ACTIVITY)
admin.site.register(SubscribeModel)
admin.site.register(PODCAST)
admin.site.register(NEWS)
admin.site.register(ARTICLE)

class AnswerInline(admin.TabularInline):
    model = ANSWER
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(QUIZ)
admin.site.register(QUESTION, QuestionAdmin)
admin.site.register(ANSWER)