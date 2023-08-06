Mandrill Logger is a simple app to log the communication with mandrill.
Sometimes we want to log the emails on our end instead of giving users access to the mandrill-account. This also allows us to follow up on user emails that are being rejected or marked as spam.

# Installation


    pip install mandrill-logger

# Getting Started

## Add to INSTALLED_APPS*

    'mandrill_logger',

## Migrate

    python manage.py migrate mandrill_logger

## Implement Mandrill Logger
After you have sent your email, simply send the email object to log_email:

    from mandrill_logger.utils import MandrillLogger
    mandrill_logger = MandrillLogger()
    mandrill_logger.log_email(email)

## Log into Admin to view the logs
Simply log in to Django Admin to view the logs created.
