import datetime
from dateutil.relativedelta import relativedelta
import csv
from django.conf import settings
import zenpy


def get_adp_tickets():

    ZENPY_CREDS = {
          'email': settings.ZENDESK_EMAIL,
          'token': settings.ZENDESK_TOKEN,
          'subdomain': settings.ZENDESK_SUBDOMAIN
        }

    zen = zenpy.Zenpy(**ZENPY_CREDS)

    start_date = datetime.datetime(2015, 11, 1, 0, 0, 0)
    end_date = datetime.datetime(2016, 1, 1, 0, 0, 0)

    all_results = []

    while start_date <= datetime.datetime.now():

        if end_date > datetime.datetime.now():
            end_date = datetime.datetime.now() + relativedelta(days=+1)

        results = zen.search(type='ticket', subject='Feedback (gamma)', created_between=[start_date, end_date])

        for result in results:
            all_results.append(result)

        start_date = start_date + relativedelta(months=+2)
        end_date = end_date + relativedelta(months=+2)

    return all_results


def add_csv_to_response(response, data):

    csv_writer = csv.writer(response, delimiter=',')

    csv_writer.writerow(['Score', 'ID', 'Date', 'Subject', 'Tags'])

    sum_scores = 0
    for item in data:

        csv_writer.writerow([item.description[0], item.id, item.created_at[:10], item.subject, ', '.join(item.tags)])
        sum_scores += int(item.description[0])

    mean_score = 'Mean score = %s' % (str(sum_scores/len(data)))

    csv_writer.writerow('')
    csv_writer.writerow([mean_score])




