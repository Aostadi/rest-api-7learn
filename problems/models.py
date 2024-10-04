from django.db import models

from accounts.models import User


class Problem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=100)


class Submission(models.Model):
    participant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submissions"
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="submissions"
    )

    submitted_time = models.DateTimeField()
    code = models.URLField()
    score = models.PositiveIntegerField(default=0)

