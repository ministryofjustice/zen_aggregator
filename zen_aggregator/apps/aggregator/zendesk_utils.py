import csv
from django.conf import settings
import zdesk


def read_zendesk_data():
    zd = zdesk.Zendesk(settings.ZENDESK_SHORT_URL, settings.ZENDESK_USERNAME, settings.ZENDESK_TOKEN, True)
    full_data = zd.search(query='type:ticket subject:Feedback (gamma)', get_all_pages=True)
    data = full_data['results']
    return data


def add_csv_to_response(response, data):

    csv_writer = csv.writer(response, delimiter=',')

    csv_writer.writerow(['Score', 'Date'])

    sum_scores = 0
    for item in data:
        csv_writer.writerow([item['description'][0], item['created_at'][:10]])
        sum_scores += int(item['description'][0])

    mean_score = 'Mean score = %s' % (str(sum_scores/len(data)))

    csv_writer.writerow('')
    csv_writer.writerow([mean_score])

