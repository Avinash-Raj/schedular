from collections import defaultdict
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response:
        final_response = {
            "error": {
                "field_errors": {},
                "non_field_errors": []
            }
        }
        final_response['error']['field_errors'] = response.data

        response.data = final_response

    return response
