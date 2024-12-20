from django.contrib import admin
from .models import Quiz, Choice, Question, UserQuizResult


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    inlines = [QuestionInline, ChoiceInline]


admin.site.register(UserQuizResult)
