from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from bank_account.requests import post_credit_requests, post_unlink_redirect_request


@login_required
def post_credit_request(request):
    if request.method == 'POST':
        if 'amount' in request.POST and 'order_url' in request.POST:
            data = {
                "user_id": request.user.id,
                "amount": request.POST['amount'],
                "order_url": request.POST['order_url'],
                'session_id': request.COOKIES[settings.PASSPORT_SESSION_ID_NAME],
                'secret': settings.PASSPORT_SECRET_KEY,
            }
            status_code, data = post_credit_requests(data)
            if status_code == 201 and data:
                return JsonResponse({'error': False,
                                     'data': {
                                         'redirect_url': data['redirect_url']
                                     }}, safe=False)
            elif status_code == 400 and data['cause'] == 'WORKFLOW_FAULT':
                return JsonResponse({'error': True, 'data': data['message']}, safe=False)
            else:
                return JsonResponse({'error': True, 'data': 'Что пошло не так...'}, safe=False)
        else:
            return JsonResponse({'error': True, 'data': ''}, safe=False)
    else:
        return HttpResponse(status=405)


@login_required
def post_unlink_redirect(request):
    data = {
        'user_id': request.user.id,
        'session_id': request.COOKIES[settings.PASSPORT_SESSION_ID_NAME],
        'secret': settings.PASSPORT_SECRET_KEY,
    }
    post_unlink_redirect_request(data)
    return redirect('/')


@login_required
def link_redirect(request):
    url = "{passport_url}/oidc/authenticate/".format(passport_url=settings.PASSPORT_URL)
    return redirect(url)
