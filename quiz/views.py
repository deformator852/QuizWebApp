from django.shortcuts import render
from django.views import View
from .models import Quiz


class Home(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            quizzes = Quiz.objects.all()
            context["quizzes"] = quizzes
        return render(request, "quiz/index.html", context)


class QuizPage(View):
    def get(self, request, pk=None):
        return render(request, "quiz/quiz.html")
