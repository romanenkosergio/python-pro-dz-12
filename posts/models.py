from django.db.models import Model, CharField, DateTimeField, TextField


class Post(Model):
    """Post model."""
    title = CharField(max_length=50)
    content = TextField(max_length=255)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
