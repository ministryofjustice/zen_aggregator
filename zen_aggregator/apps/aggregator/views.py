import csv
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .forms import PasswordForm
from django.conf import settings
import zdesk


def read_zendesk_data():
    zd = zdesk.Zendesk(settings.ZENDESK_SHORT_URL, settings.ZENDESK_USERNAME, settings.ZENDESK_TOKEN, True)
    full_data = zd.search(query='type:ticket subject:Feedback (gamma)', get_all_pages=True)
    data = full_data['results']
    return data


def create_csv(response, data):

    csv_writer = csv.writer(response, delimiter=',')

    csv_writer.writerow(['Score', 'Date'])

    sum_scores = 0
    for item in data:
        csv_writer.writerow([item['description'][0], item['created_at'][:10]])
        sum_scores += int(item['description'][0])

    mean_score = 'Mean score = %s' % (str(sum_scores/len(data)))

    csv_writer.writerow('')
    csv_writer.writerow([mean_score])

    return response


def get_password(request):

    if request.method == 'POST':

        form = PasswordForm(request.POST)

        # Why isn't this picking up a 200 character string as invalid?
        if form.is_valid():
            password = form.cleaned_data['password']

            if password == 'cabbage':

                now = datetime.datetime.now()
                csv_filename = '%s-%s-%s-%s_%s-%s-%s' % ('aggregation', now.year, now.month, now.day, now.hour,
                                                           now.minute, now.second)
                content_disp = 'attachment; filename=' + csv_filename + '.csv'
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = content_disp
                data = read_zendesk_data()
                response = create_csv(response, data)

            else:
                response = HttpResponse('<html><head><title>test_view</title></head><body>Password Incorrect</body></html>')

        else:
            response = HttpResponse('<html><head><title>test_view</title></head><body>Form Invalid</body></html>')

    else:

        form = PasswordForm()
        response = render(request, 'aggregator/get_password.html', {'form': form})

    return response


