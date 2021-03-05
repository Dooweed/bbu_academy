from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from . import merchant_api_methods
from .utils import check_post, check_authorization, check_json_content, check_request_id, check_method, check_params, PaymeCheckFailedException

@csrf_exempt
def payme_billing(request):
    request_id, method, params, result = None, None, None, None

    try:
        check_post(request)
        check_authorization(request)
        content = check_json_content(request)
        request_id = check_request_id(content)
        method = check_method(content)
        params = check_params(content)
        result = merchant_api_methods.perform(method, params)
    except PaymeCheckFailedException as e:
        result = e.error()

    response = {
        "id": request_id,
        "error" if result.is_error() else "result": result.dict()
    }

    return JsonResponse(data=response)
