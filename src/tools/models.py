from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Tools(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    small_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='tools/images')
    categories = models.ManyToManyField(Category)
    date_added = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name
        
    def is_favorited_by(self, user):
        """Check if this tool is favorited by the given user"""
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(user=user, tool=self).exists()

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Ensure a user can only favorite a tool once
        unique_together = ('user', 'tool')
        
    def __str__(self):
        return f"{self.user.username} - {self.tool.name}"
    
class Comment(models.Model):
    tools = models.ForeignKey(Tools, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.tool.name}"

class ContentImage(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    image = models.ImageField(_('Image'), upload_to='content_images/')
    uploaded_at = models.DateTimeField(_('Uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Content Image')
        verbose_name_plural = _('Content Images')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
    
class Suggestion(models.Model):
    tool_name = models.CharField(max_length=100)
    tool_link = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    back_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion by {self.back_email} on {self.tool_name}"