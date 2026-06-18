from rest_framework import serializers
from .models import Test, Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        # We only send these specific fields to the frontend
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    # This pulls in the choices linked to this question.
    # 'many=True' is crucial because one question has multiple choices!
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'marks', 'choices']

class TestSerializer(serializers.ModelSerializer):
    # This pulls in all the questions linked to this test.
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        # Notice how 'questions' is explicitly added to the fields list here
        fields = ['id', 'title', 'description', 'tutor', 'created_at', 'questions']