from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from posts.models import Post

fake = Faker()


class Command(BaseCommand):
    help = "Generate posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, help="Indicates the number of posts to be created"
        )

    def handle(self, *args, **options):
        count = options["count"] or 100
        for i in range(count):
            Post.objects.create(
                title=fake.text(max_nb_chars=50),
                content=fake.text(max_nb_chars=255),
                updated_at=timezone.now()
            )
        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {count} posts")
        )
