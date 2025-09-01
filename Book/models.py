from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Story', 'Story'),
        ('Study', 'Study'),
    ]
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='book_images/')
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Borrow(models.Model):
    DURATION_CHOICES = [
        ('1 Week', '1 Week'),
        ('15 Days', '15 Days'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    borrowed_at = models.DateTimeField(auto_now_add=True)
