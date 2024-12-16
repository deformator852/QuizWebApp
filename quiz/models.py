from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="photos/%Y/%m/%d")
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)


class UserQuizResult(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
