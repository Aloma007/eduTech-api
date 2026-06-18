from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsTutor
from .models import Test, Question, Choice, Submission, StudentAnswer
from .serializers import TestSerializer

class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only Tutors can modify tests
            permission_classes = [IsAuthenticated, IsTutor]
        else:
            # Both Students and Tutors can view tests
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        test = self.get_object()
        student = request.user

        # Security Check 1: Tutors cannot take tests!
        if not student.is_student:
            return Response({"error": "Only registered students can submit exams."}, status=status.HTTP_403_FORBIDDEN)

        # Security Check 2: Prevent taking the test twice
        if Submission.objects.filter(test=test, student=student).exists():
            return Response({"error": "You have already completed this test."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Create the blank submission paper
        submission = Submission.objects.create(test=test, student=student)

        total_score = 0

        # Step 2: Grab the JSON data the student sent us
        # We expect a list like: [{'question_id': 1, 'choice_id': 2}, ...]
        answers_data = request.data.get('answers', [])

        # Step 3: The Auto-Grader Loop
        for data in answers_data:
            try:
                question = Question.objects.get(id=data['question_id'], test=test)
                selected_choice = Choice.objects.get(id=data['choice_id'], question=question)

                # Record their exact answer in the database
                StudentAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_choice=selected_choice
                )

                # Check if it matches the master marking guide!
                if selected_choice.is_correct:
                    total_score += question.marks

            except (Question.DoesNotExist, Choice.DoesNotExist):
                # If they send fake IDs, we just ignore it
                continue

                # Step 4: Write the final score at the top of the paper and save
        submission.score = total_score
        submission.save()

        # Step 5: Hand the graded paper back to the student
        return Response({
            "message": "Examination submitted and graded successfully!",
            "final_score": total_score
        }, status=status.HTTP_201_CREATED)