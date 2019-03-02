from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from unidecode import unidecode

User = get_user_model()


class Tour(models.Model):
    title = models.CharField(max_length=250, unique=True)
    destination = models.TextField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    duration = models.DurationField(blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('html name', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def change_status(self):
        self.active = not self.active
        super().save()


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, name='user', related_name='+', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, name='tour', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    created_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField()

    def __str__(self):
        return self.text


class Order(models.Model):
    tour = models.ForeignKey(Tour, name='tour', related_name='orders', on_delete=models.PROTECT)
    user = models.ForeignKey(User, name='user', related_name='orders', on_delete=models.PROTECT)
    ordered_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=120)

    def save(self, *args, **kwargs):
        self.status = 'Pending'
        super().save(*args, **kwargs)

    def accept(self):
        self.status = 'Accepted'
        super().save()

    def reject(self):
        self.status = 'Rejected'
        super().save()

    def cancel(self):
        self.status = 'Canceled'
        super().save()

    class Meta:
        permissions = (('can_cancel', 'user can cancel'), ('can_accept', 'admin can approve or reject'))


class Images(models.Model):
    tour = models.ForeignKey(Tour, default=None, related_name='images', on_delete=False)
    image = models.ImageField(upload_to='pictures', verbose_name='Image')
    is_main = models.BooleanField(default=False)

    def make_main(self):
        self.is_main = not self.is_main
        self.save()
