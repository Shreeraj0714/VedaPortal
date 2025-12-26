from django.core.management.base import BaseCommand
from main.models import Subject, Unit, Topic
import os
import markdown

class Command(BaseCommand):
    help = "TEST: Import markdown with formatting"

    def handle(self, *args, **kwargs):
        file_path = "content/test/hello.md"

        with open(file_path, "r", encoding="utf-8") as f:
            html_content = markdown.markdown(f.read())

        subject, _ = Subject.objects.get_or_create(name="TEST SUBJECT")
        unit, _ = Unit.objects.get_or_create(
            subject=subject,
            title="TEST UNIT",
            defaults={"order": 99}
        )

        Topic.objects.update_or_create(
            unit=unit,
            title="Hello Topic",
            defaults={
                "content": html_content,  # ✅ HTML, not markdown
                "order": 1
            }
        )

        self.stdout.write("✅ Formatting FIXED")
