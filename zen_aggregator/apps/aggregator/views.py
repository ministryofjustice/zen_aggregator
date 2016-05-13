import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PasswordForm
from .zendesk_utils import *


def generate_response():

    now = datetime.datetime.now()
    csv_filename = '%s-%s-%s-%s_%s-%s' % ('aggregation', now.year, now.month, now.day, now.hour, now.minute)
    content_disp = 'attachment; filename=' + csv_filename + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disp
    return response


def get_password(request):

    if request.method == 'POST':

        form = PasswordForm(request.POST)

        # Why isn't this picking up a 200 character string as invalid?
        if form.is_valid():
            password = form.cleaned_data['password']

            if password == os.environ.get('ZA_PASSWORD'):
                response = generate_response()
                data = get_adp_tickets()
                add_csv_to_response(response, data)

            else:
                response = render(request, 'aggregator/wrong_password.html')

        else:
            response = HttpResponse('<html><head><title>test_view</title></head><body>Form Invalid</body></html>')

    else:

        form = PasswordForm()
        response = render(request, 'aggregator/get_password.html', {'form': form})

    return response


