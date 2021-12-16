from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_reg_notification(user, batch):

    msg_plain = f""" Thanks for signing up for {batch.course.name}
        It starts on {batch.start_date}"""

    # msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    msg_html = render_to_string(
        "users/batch-registration.html",
        {"batch": batch, "user": user},
    )

    send_mail(
        f"Rocket Academy {batch.course.name} {batch.start_date} Signup",
        msg_plain,
        "Rocket Academy <hello@rocketacademy.co>",
        [user.email],
        html_message=msg_html,
    )
