from django.http import JsonResponse
from typing import List


def render_api_response(data: List, **kwargs) -> JsonResponse:
    """
    {"status": success/failure, data: [], error_message: "", code:""}
    :param data:
    :param kwargs: code, msg, http_code and data_support
    :return: JsonResponse
    """
    res_obj = dict(
        status="FAILURE", code=kwargs.pop("code", "na"), message=kwargs.pop("msg", "")
    )

    status = kwargs.pop("success", True)
    if status:
        res_obj["status"] = "SUCCESS"

    res_obj["response"] = dict(
        data=[data] if not type(data) == list else data,
        support=kwargs.pop("data_support", dict()),
    )

    _http = dict(status=kwargs.pop("http_code", 200))
    res_obj.update(kwargs)

    return JsonResponse(res_obj, **_http)
