import os
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PasswordForm
from .zendesk_utils import *


def get_password(request):

    if request.method == 'POST':

        form = PasswordForm(request.POST)

        # Why isn't this picking up a 200 character string as invalid?
        if form.is_valid():
            password = form.cleaned_data['password']

            if password == os.environ.get('ZA_PASSWORD'):

                now = datetime.datetime.now()
                csv_filename = '%s-%s-%s-%s_%s-%s' % ('aggregation', now.year, now.month, now.day,
                                                        now.hour, now.minute)
                content_disp = 'attachment; filename=' + csv_filename + '.csv'

                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = content_disp
                data = read_zendesk_data()
                response = create_csv(response, data)

            else:
                #response = HttpResponse('<html><head><title>test_view</title></head><body>Password Incorrect</body></html>')
                response = render(request, 'aggregator/wrong_password.html')

        else:
            response = HttpResponse('<html><head><title>test_view</title></head><body>Form Invalid</body></html>')

    else:

        form = PasswordForm()
        response = render(request, 'aggregator/get_password.html', {'form': form})

    return response


