from django.core.mail import send_mail
from django.template import loader

def SendMail():
    # inject the respective values in HTML template
    html_message = loader.render_to_string(
        'email/email.html',
        {
            # TODO: Enter the recipient name
            'name': 'Dharmendra Patidar',
            # TODO:  Update with your own body
            'body': 'This email is to verify whether we can send email in Django from Gmail account.',
            # TODO: Update the signature
            'sign': 'Sphurit',
        })
    send_mail(
        'Congratulations!',
        'You are lucky to receive this mail.',
        'patidardharmendra830@gmail.com',  # TODO: Update this with your mail id
        ['patidardharam24@gmail.com'],  # TODO: Update this with the recipients mail id
        html_message=html_message,
        fail_silently=False,
    )

def SendRegistrationMail(email):
    send_mail(
        'Congratulations!',
        'Welcome Email',
        'patidardharmendra830@gmail.com',  # TODO: Update this with your mail id
        [email,],  # TODO: Update this with the recipients mail id
        html_message=loader.render_to_string('email/registration-success-mail.html',{}),
        fail_silently=False,
    )

    

def SendInvoicMail(data):
    send_mail(
        'Congratulations!',
        'Purchase Email',
        'patidardharmendra830@gmail.com',  # TODO: Update this with your mail id
        [data['email'],],  # TODO: Update this with the recipients mail id
        html_message=loader.render_to_string('email/invoice-mail.html',{
            'name': data['name'],
            'invoice_number': data['invoice_number'],
            'order_date': data['order_date'],
            'items':data['items'],
            'subtotal':data['subtotal'],
            'gst_rate':data['gst_rate'],
            'gst_price':data['gst_price'],
            'total':data['total'],
        }),
        fail_silently=False,
    )