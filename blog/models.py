from django.db import models

from users.models import CustomUser


class Blogs(models.Model):
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='authors'
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='blogs_owner'
    )

    class Meta:
        ordering = ('updated_at',)
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return f"title: {self.title}, owner: {self.owner.username}"


class Tags(models.Model):
    title = models.CharField(max_length=130, blank=False, db_index=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class Posts(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        db_index=True
    )
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"id:{self.id}, author: {self.author.username}, \
                blog: {self.blog.title}"


class Comments(models.Model):
    author = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL
    )
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"id: {self.id}, author: {self.author.username}, \
               post: {self.post.title}"
