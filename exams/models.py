from django.db import models
from django.db import models
from django.conf import settings

class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # This links the test to the custom user who created it
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
