import csv
import zdesk
import datetime
from dateutil.relativedelta import relativedelta


import time
import csv
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import zdesk
import zenpy


def get_adp_tickets():

    ZENPY_CREDS = {
          'email': settings.ZENDESK_EMAIL,
          'token': settings.ZENDESK_TOKEN,
          'subdomain': settings.ZENDESK_SUBDOMAIN
        }

    zen = zenpy.Zenpy(**ZENPY_CREDS)

    start_date = datetime.datetime(2015, 11, 1, 0, 0, 1)  # 01/10/15, 00:01
    end_date = datetime.datetime(2015, 12, 31, 0, 0, 1)

    all_results = []

    while end_date <= datetime.datetime.now():

        results = zen.search(type='ticket', subject='Feedback (gamma)', created_between=[start_date, end_date])

        # all_results = all_results + results

        for result in results:
            all_results.append(result)

        start_date = start_date + relativedelta(months=+1)
        end_date = end_date + relativedelta(months=+1)

    return all_results


def add_csv_to_response(response, data):

    csv_writer = csv.writer(response, delimiter=',')

    csv_writer.writerow(['Score', 'Date'])

    sum_scores = 0
    for item in data:
        csv_writer.writerow([item.description[0], item.created_at[:10]])
        sum_scores += int(item.description[0])

    mean_score = 'Mean score = %s' % (str(sum_scores/len(data)))

    csv_writer.writerow('')
    csv_writer.writerow([mean_score])




