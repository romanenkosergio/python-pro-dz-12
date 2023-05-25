from django.forms import ModelForm
from django.utils import timezone

from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

    def save(self, *args, **kwargs):
        if not self.instance.id:
            self.instance.updated_at = timezone.now()
        return super().save(*args, **kwargs)
