from django import template
from quiz.models import Quiz
from django.conf import settings

register = template.Library()


@register.inclusion_tag("quiz/include/quizzes_list.html")
def show_quizzes():
    quizzes = Quiz.objects.all()
    return {
        "quizzes": quizzes,
        "MEDIA_URL": settings.MEDIA_URL,
    }
