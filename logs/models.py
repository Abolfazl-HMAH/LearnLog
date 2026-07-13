from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Entry(models.Model):
    log = models.ForeignKey(
        Log,
        on_delete=models.CASCADE,
        related_name="entries"
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:40]