from rest_framework.response import Response


class ErrorResponse(Response):
    def __init__(self, data=None, **kwargs):
        data_dict = {
            "error": data
        }
        super().__init__(data=data_dict, **kwargs)
