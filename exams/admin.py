from django.contrib import admin
from .models import Test, Question, Choice, Submission, StudentAnswer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(StudentAnswer)