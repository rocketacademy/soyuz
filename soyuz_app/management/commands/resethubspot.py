from django.conf import settings
from django.core.management.base import BaseCommand
from hubspot.auth.oauth import ApiException
from mimesis import Person
from mimesis.locales import Locale

from soyuz_app.library.hubspot import Hubspot
from soyuz_app.models import User


class Command(BaseCommand):
    help = "Resets all the local data and on the API"

    # def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        # extra saftey - hard code, don't run on production
        if settings.ALLOWED_HOSTS == "learn.rocketacademy.co":
            return

        hubspot_client = Hubspot()
        try:
            for _ in range(60):
                person = Person(Locale.EN)
                email = person.email()
                first_name = person.first_name()
                last_name = person.last_name()
                hubspot_id = hubspot_client.create_contact(email, first_name, last_name)
                u = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    hubspot_id=hubspot_id,
                )
                u.set_password("123456789")
                u.save()
                self.stdout.write(
                    self.style.SUCCESS(f"create {email} {first_name} {last_name}")
                )

        except ApiException as e:
            print("Exception when calling method: %s\n" % e)
            raise ValueError("Hubspot Error!!1!")
        self.stdout.write(self.style.SUCCESS("done"))
        # for poll_id in options['poll_ids']:
