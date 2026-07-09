from django.db import models


class ResourceCategory(models.Model):

    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Resource(models.Model):

    title = models.CharField(
        max_length=200
    )

    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.CASCADE
    )

    description = models.TextField()

    content = models.TextField()

    # Optional file attachment (PDF, DOCX, etc.)
    resource_file = models.FileField(
        upload_to="resources/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title