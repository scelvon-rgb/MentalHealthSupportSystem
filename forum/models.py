from django.db import models
from django.contrib.auth.models import User


class ForumPost(models.Model):

    post_id = models.AutoField(primary_key=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    content = models.TextField()

    anonymous = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "forum_posts"

    def __str__(self):
        return self.title


class ForumComment(models.Model):

    comment_id = models.AutoField(primary_key=True)

    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "forum_comments"

    def __str__(self):
        return f"Comment by {self.author.username}"