from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_reminder(user, batch):

    msg_plain = f""" Thanks for signing up for {batch.course.name} {batch.number}
        It starts on {batch.start_date}
        Please remember to register on Slack!"""

    # msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    msg_html = render_to_string(
        "users/slack-reminder.html",
        {"batch": batch, "user": user},
    )

    send_mail(
        f"Rocket Academy {batch.course.name} {batch.number} Slack Registration Reminder",
        msg_plain,
        "Rocket Academy <hello@rocketacademy.co>",
        [user.email],
        html_message=msg_html,
    )
