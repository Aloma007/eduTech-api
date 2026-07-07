from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Test, Question, Choice

User = get_user_model()


class TestSubmissionAPI(APITestCase):
    def setUp(self):
        """This runs FIRST to set up the fake database for the robot."""
        # 1. Create a dummy student
        self.student = User.objects.create_user(username="test_student", password="password123", is_student=True)

        # 2. Create a dummy tutor (NEW!)
        self.tutor = User.objects.create_user(username="test_tutor", password="password123", is_tutor=True)

        # 3. Create a dummy exam and attach the tutor! (UPDATED)
        self.exam = Test.objects.create(title="UNIT TEST EXAM", tutor=self.tutor)

        # 4. Create a dummy question & correct choice
        self.question = Question.objects.create(test=self.exam, text="What is 2 + 2?", marks=1.0)
        self.correct_choice = Choice.objects.create(question=self.question, text="4", is_correct=True)

        # 5. The target URL for submission
        self.submit_url = f'/api/tests/{self.exam.id}/submit/'

    def test_student_gets_perfect_score(self):
        """The actual test! The robot logs in and takes the exam."""
        # Log the robot in as the student
        self.client.force_authenticate(user=self.student)

        # The fake JSON payload the robot will send
        # (Make sure this matches the exact JSON format your API expects!)
        payload = {
            "answers": [
                {
                    "question_id": self.question.id,
                    "choice_id": self.correct_choice.id
                }
            ]
        }

        # Fire the POST request at the API!
        response = self.client.post(self.submit_url, payload, format='json')

        # Check 1: Did the server accept it? (Expecting HTTP 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check 2: Did the auto-grader calculate a perfect 1.0 score?
        self.assertEqual(response.data['final_score'], 1.0)