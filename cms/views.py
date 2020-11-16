import logging
from django.http import JsonResponse
from rest_framework.views import APIView
from account.passport_methods import get_user_from_passport
from account.user_category import get_user_info


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'erp.log')


def create_response_object(error, report=None, data=None, titles=None):
    response_data = {
        "error": error
    }
    if report is not None:
        response_data["report"] = report
    if data is not None:
        response_data["data"] = data
    if titles is not None:
        response_data["titles"] = titles

    return JsonResponse(response_data)


class UserData(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        session = request.data.get("session")
        if not session:
            return create_response_object(True, report="Пожалуйста, войдите в аккаунт на паспорте")

        user = get_user_from_passport(session_id=session)
        if not user:
            return create_response_object(True, report="Пожалуйста, перезайдите")

        return create_response_object(False, data=get_user_info(user))
