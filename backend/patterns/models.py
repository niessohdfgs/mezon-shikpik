from django.db import models
from django.conf import settings

class Pattern(models.Model):

    title = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    thumbnail = models.ImageField(
        upload_to="patterns/",
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to="patterns/files/"
    )

    price = models.PositiveIntegerField()

    is_published = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title
    
class PatternPurchase(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    pattern = models.ForeignKey(
        Pattern,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        unique_together = (
            "user",
            "pattern"
        )