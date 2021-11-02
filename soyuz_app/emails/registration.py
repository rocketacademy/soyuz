from django.core.mail import send_mail


def send_reg_notification(user, batch, section):

    email_text_body = f""" Thanks for signing up for {batch.course.name}
        It starts on {batch.start_date}
        You are in section {section.number}"""

    # TODO: add relevant batch deailts to email
    # send them a confirmation email
    send_mail(
        f"Rocket Academy {batch.course.name} Signup",
        email_text_body,
        "Rocket Academy <hello@rocketacademy.co>",
        [user.email],
    )
