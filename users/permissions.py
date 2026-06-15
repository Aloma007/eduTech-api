from rest_framework import permissions

class IsTutor(permissions.BasePermission):
    """Allows access only to authenticated users flagged as tutors."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_tutor)

class IsStudent(permissions.BasePermission):
    """Allows access only to authenticated users flagged as students."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)