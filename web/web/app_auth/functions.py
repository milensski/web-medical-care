from django.contrib import messages


def show_errors(request, form):
    list_errors = ''
    for error in form.errors:
        list_errors += form.errors[error]

    messages.error(request, list_errors)
