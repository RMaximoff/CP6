from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_img/', blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'

    def __str__(self):
        return self.title
