from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Question, Quiz, Choice
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class Home(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            quizzes = Quiz.objects.all()
            context["quizzes"] = quizzes
        return render(request, "quiz/index.html", context)


@method_decorator(login_required, name="dispatch")
class QuizPage(View):
    def get(self, request: HttpRequest, pk=None):
        if pk is not None:
            quiz = Quiz.objects.filter(pk=pk).exists()
            if quiz is None:
                raise Http404()
            context = {}
            request.session["quiz_id"] = pk
            step = request.session.get("step", None)
            if step is None:
                step = request.session["step"] = 1
            # if step > 12:
            #     request.session["step"] = 1
            #     return render(request, "quiz/quiz.html", context)
            question = Question.objects.all()[step - 1 : step]
            choices = Choice.objects.filter(question=question)
            context["question"] = question
            context["choices"] = choices
            return render(request, "quiz/quiz.html", context)
        else:
            raise Http404()

    def post(self, request: HttpRequest, pk=None):
        context = {}
        step = request.session["step"]
        print(step)
        if step >= 12:
            request.session["step"] = None
            context["finish"] = True
            print(request.session["choices"])
            del request.session["choices"]
            del request.session["step"]
            return render(request, "quiz/quiz.html", context)
        answer_id = request.POST.get("choice")
        choices = request.session.get("choices", None)
        if choices is None:
            request.session["choices"] = [answer_id]
        else:
            request.session["choices"].append(answer_id)
        step = request.session["step"] = step + 1
        question = Question.objects.all()[step - 1 : step]
        choices = Choice.objects.filter(question=question)
        context["question"] = question
        context["choices"] = choices
        return render(request, "quiz/quiz.html", context)
