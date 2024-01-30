from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse

# Create your models here.


sport = 'SP'
education = 'ED'
policy = 'PO'
economy = 'EC'
zdrav = 'ZD'

TOPICS = [
    (sport, 'Спорт'),
    (policy, 'Политика'),
    (education, 'Образование'),
    (economy, 'Экономика'),
    (zdrav, 'Здравоохранение')
]

news = 'NE'
articles = 'AR'

TYPES = [
    (news, 'Новость'),
    (articles, 'Статья')
]


class Appoiments(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self):
        articles_rate = int((Post.objects.filter(author_id=self.pk).aggregate(Sum('rate'))['rate__sum'] * 3) or 0)
        comment_rate = int(Comment.objects.filter(user_id=self.user).aggregate(Sum('rate'))['rate__sum'] or 0)
        comments_posts_rate = int(Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rate'))['rate__sum'] or 0)
        self.rate = articles_rate + comment_rate + comments_posts_rate
        self.save()

        return self.rate

    def update_sum_post(self):
        return Post.objects.filter(author=self).count()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=2, choices=TOPICS, default=zdrav, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.name}'


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_news = models.CharField(max_length=2, choices=TYPES, default=news)
    date_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.date_time.strftime("%d.%m.%Y")}: {self.title.title()} - {self.text[:20]}'

    def preview(self):
        t_ = self.text[0:124]
        return f"{t_}..."

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()
