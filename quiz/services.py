from quiz.models import Question, Quiz, UserQuizResult, Choice


def get_all_quizzes():
    return Quiz.objects.all()


def quiz_results_exists(user, quiz_pk):
    return UserQuizResult.objects.filter(user=user, quiz=quiz_pk).exists()


def get_user_quiz_result(user, quiz_pk):
    return UserQuizResult.objects.get(user=user, pk=quiz_pk)


def quiz_exists(pk):
    return Quiz.objects.filter(pk=pk).exists()


def get_next_question(step):
    return Question.objects.all()[step - 1 : step]


def get_choices_for_questions(question):
    return Choice.objects.filter(question=question)


def correct_answers_count(choices):
    correct_answers = Choice.objects.filter(pk__in=choices, is_correct=True)
    return len(correct_answers)


def create_user_quiz_result(score, quiz_id, user):
    quiz = Quiz.objects.get(pk=quiz_id)
    UserQuizResult.objects.create(user=user, quiz=quiz, score=score)


def get_user_quizzes_results(user):
    return UserQuizResult.objects.filter(user=user)
