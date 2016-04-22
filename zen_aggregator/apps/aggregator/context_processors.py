def globals(request):

    return {
        'app_title': 'Zendesk Aggregator', # Application Title (Populates <title>)
        'proposition_title': 'Zendesk Aggregator', # Proposition Title (Populates proposition header)
        'phase': 'alpha', # Current Phase (Sets the current phase and the colour of phase tags). Presumed values: alpha, beta, live
        'product_type': 'service', # Product Type (Adds class to body based on service type). Presumed values: information, service
        'feedback_url': 'test.test.test', # Feedback URL (URL for feedback link in phase banner)
    }

