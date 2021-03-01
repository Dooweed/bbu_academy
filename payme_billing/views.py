from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from payme_billing.tools import MerchantApiRequest

@csrf_exempt
def payme_billing(request):
    payme_request = MerchantApiRequest(request)

    return JsonResponse(data=payme_request.response())
