from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name='Сообщение')
    image = models.ImageField(upload_to='blog/', verbose_name='Превью', blank=False)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=True)
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            num = 1
            for blog in Blog.objects.all():
                if blog.slug == slug:
                    slug = f'{slug}_{num}'
                    num += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_published = False
        self.save()

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'
        ordering = ['create_date']