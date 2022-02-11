from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_waiting_list_confirmation(user, batch, first_name, waiting_list_count, waiting_list_position):

    msg_plain = f""" Thanks for signing up for {batch.course.name.capitalize()} {batch.number}'s waiting list!\nWe will notify you by email if a spot opens up"""

    # msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
    msg_html = render_to_string(
        "users/emails/email-waiting-list-confirmation.html", {
            "user": user,
            "batch": batch,
            "first_name": first_name,
            "waiting_list_count": waiting_list_count,
            "waiting_list_position": waiting_list_position
        },
    )

    send_mail(
        f"Rocket Academy {batch.course.name.capitalize()} {batch.number} Waiting List",
        msg_plain,
        "Rocket Academy <basics@rocketacademy.co>",
        [user.email],
        html_message=msg_html,
    )
