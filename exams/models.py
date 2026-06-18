from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # This links the test to the custom user who created it
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    # This links every question to a specific Test.
    # 'related_name' lets us easily grab all questions for a test later!
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    marks = models.IntegerField(default=1) # Points awarded for getting this right

    def __str__(self):
        return f"{self.test.title} - Question: {self.text[:50]}"

class Choice(models.Model):
    # This links every choice to a specific Question
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    # The auto-grader will look for this exact flag to score the student
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"



class Submission(models.Model):
    # Links to the Test and the Student taking it
    test = models.ForeignKey(Test, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_student': True})

    # We leave this blank initially; the auto-grader will calculate and fill this in!
    score = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s attempt on {self.test.title}"


class StudentAnswer(models.Model):
    # Links their specific choice to their overall submission
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer for: {self.question.text[:30]}"