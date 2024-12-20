from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .services import (
    correct_answers_count,
    create_user_quiz_result,
    get_all_quizzes,
    get_choices_for_questions,
    get_next_question,
    get_user_quiz_result,
    quiz_exists,
    quiz_results_exists,
)


class Home(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            quizzes = get_all_quizzes()
            context["quizzes"] = quizzes
        return render(request, "quiz/index.html", context)


@method_decorator(login_required, name="dispatch")
class QuizPage(View):
    def get(self, request: HttpRequest, pk=None):
        if pk is not None:
            user = request.user
            context = {}
            if quiz_results_exists(user, pk):
                user_quiz_result = get_user_quiz_result(user, pk)
                context["quiz_result_exist"] = True
                context["score"] = user_quiz_result.score
                return render(request, "quiz/quiz.html", context)
            quiz = quiz_exists(pk)
            if quiz is None:
                raise Http404()
            request.session["quiz_id"] = pk
            step = request.session.get("step", None)
            if step is None:
                step = request.session["step"] = 1
            question = get_next_question(step)
            choices = get_choices_for_questions(question)
            context["question"] = question
            context["choices"] = choices
            return render(request, "quiz/quiz.html", context)
        else:
            raise Http404()

    def post(self, request: HttpRequest, pk=None):
        context = {}
        step = request.session["step"]
        if step >= 12:
            choices = request.session["choices"]
            quiz_id = request.session["quiz_id"]
            user = request.user
            score = correct_answers_count(choices)
            create_user_quiz_result(score, quiz_id, user)
            context["finish"] = True
            context["score"] = score
            del request.session["choices"]
            del request.session["step"]
            del request.session["quiz_id"]
            return render(request, "quiz/quiz.html", context)
        answer_id = request.POST.get("choice")
        choices = request.session.get("choices", None)
        if choices is None:
            request.session["choices"] = [answer_id]
        else:
            request.session["choices"].append(answer_id)
        step = request.session["step"] = step + 1
        return redirect(reverse("quiz", kwargs={"pk": pk}))
