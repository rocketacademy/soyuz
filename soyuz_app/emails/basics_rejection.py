from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_rejection_email(user, batch):

    msg_plain = f""" Thank you {user.first_name} for your interest in {batch.course.name.capitalize()} {batch.number}.
    We're sorry we're not able to offer you a place in this course."""

    # msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    msg_html = render_to_string(
        "users/basics-rejection.html",
        {"batch": batch, "user": user},
    )

    send_mail(
        f"Thank you {user.first_name.capitalize()} for your interest in {batch.course.name.capitalize()} {batch.number}",
        msg_plain,
        "Rocket Academy <hello@rocketacademy.co>",
        [user.email],
        html_message=msg_html,
    )
