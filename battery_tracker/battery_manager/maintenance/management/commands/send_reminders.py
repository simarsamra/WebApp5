from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from maintenance.models import BatteryReplacementRecord
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Send email reminders for due and upcoming battery replacements'

    def handle(self, *args, **options):
        # Set your recipients here
        recipients = [
            'recipient1@example.com',
            'recipient2@example.com',
        ]
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')

        today = date.today()
        upcoming_date = today + timedelta(days=45)

        due_replacements = BatteryReplacementRecord.objects.filter(
            replacement_date__lt=today
        ).order_by('replacement_date')

        upcoming_replacements = BatteryReplacementRecord.objects.filter(
            replacement_date__gte=today,
            replacement_date__lte=upcoming_date
        ).order_by('replacement_date')

        subject = "Battery Replacement Reminders"
        message = "Battery Replacement Reminders\n\n"

        if due_replacements.exists():
            message += "Overdue Replacements:\n"
            for rec in due_replacements:
                message += f"- {rec.battery.component.machine.building.name} | {rec.battery.component.machine} | {rec.battery.component} | {rec.battery} | Due: {rec.replacement_date}\n"
            message += "\n"

        if upcoming_replacements.exists():
            message += "Upcoming Replacements (next 45 days):\n"
            for rec in upcoming_replacements:
                message += f"- {rec.battery.component.machine.building.name} | {rec.battery.component.machine} | {rec.battery.component} | {rec.battery} | Due: {rec.replacement_date}\n"
            message += "\n"

        if not due_replacements.exists() and not upcoming_replacements.exists():
            message += "No replacements are due or upcoming in the next 45 days."

        send_mail(
            subject,
            message,
            from_email,
            recipients,
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS('Reminder email sent.'))