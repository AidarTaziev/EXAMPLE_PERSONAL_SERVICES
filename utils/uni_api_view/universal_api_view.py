import os
import logging
import mimetypes
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.conf import settings
from account.user_category import get_subcategory
from utils.uni_api_view.request_wrapper import ERPWrapper, make_request_personal
from account.passport_methods import get_user_from_passport
from account.methods import get_excel_file

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'erp.log')

User = get_user_model()

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        session = request.META.get("HTTP_SESSION")
        if session:
            user_data = get_user_from_passport(session_id=session)
            if not user_data:
                return False
            company = user_data.get("company")
            user = user_data.get("user")
            if company:
                if user['is_superuser']:
                    request.session['inn'] = request.data.get('INN', "1655202105")
                else:
                    request.session['inn'] = company.get("inn")

            return True

        else:
            return False


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated, ])
# @authentication_classes([TokenAuthentication, ])
def redirect_view(request, urn):

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.data

    data["INN"] = request.session.get("inn")

    sub_cat = get_subcategory(request.data.get("link"))

    data['lang'] = sub_cat.lang if sub_cat else None
    data['Report_GUID'] = sub_cat.erp_report_guid if sub_cat else None
    uri = "{URL}/{URN}".format(URL=sub_cat.url if sub_cat else "", URN=urn)

    erp_wrap = ERPWrapper(uri, request.method, data=data, user_dict=sub_cat.get_auth_data())
    data, headers = erp_wrap.make_erp_request()

    if 'Content-Type' in headers:
        if headers['Content-Type'] and not 'application/json' in headers['Content-Type'] and not 'text' in headers['Content-Type']:
            file_response = HttpResponse(data)

            file_response['Content-Type'] = headers.get('Content-Type')
            file_response['Content-Length'] = headers.get('Content-Length')
            file_response['Content-Disposition'] = 'inline'

            logging.debug('Frontend response data - {data}'.format(data=str(file_response)))

            return file_response

    logging.debug('Frontend response data - {data}'.format(data=data))

    return JsonResponse(data, safe=True)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated, ])
# @authentication_classes([TokenAuthentication, ])
def tracking_controller(request, urn):
    #
    # if request.method == 'GET':
    #     data = request.GET
    # else:
    #     data = request.data


    error, response = make_request_personal(path="/" + urn, data=request.data)

    return JsonResponse(response, safe=True)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated, ])
# @authentication_classes([TokenAuthentication, ])
def excel_controller(request, urn):

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.data

    logging.debug("Пришедшие от фронта данные - {data}".format(data=data))
    logging.debug(data)

    sub_cat = get_subcategory(request.data.get("link"))
    data['Report_GUID'] = sub_cat.erp_report_guid if sub_cat else None
    data['lang'] = sub_cat.lang if sub_cat else None
    uri = "{URL}/{URN}".format(URL=sub_cat.url if sub_cat else "", URN=urn)
    logging.debug("------------------------+")
    logging.debug("Запрос - {uri}".format(uri=uri))

    erp_wrap = ERPWrapper(uri, request.method, data=data, user_dict=sub_cat.get_auth_data())
    data, headers = erp_wrap.make_erp_request()
    excel_file = get_excel_file(request.data.get("link"), data.get('data'))
    if excel_file:
        file = excel_file.read()
    else:
        full_path_way = "template.xlsx"
        file = open(full_path_way, "rb").read()

    file_response = HttpResponse(file)
    file_response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    file_response['Content-Length'] = len(file)
    file_response['Content-Disposition'] = "attachment; filename=file.xlsx"
    return file_response



@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated, ])
# @authentication_classes([TokenAuthentication, ])
def tracking_excel_controller(request, urn):
    logging.debug("Запрос - {urn}".format(urn=urn))

    if request.method == 'GET':
        data = request.GET
    else:
        data = request.data

    logging.debug("Пришедшие от фронта данные - {data}".format(data=data))
    logging.debug(data)

    error, response = make_request_personal(path="/" + urn, data=data)

    logging.debug(response['data'])

    excel_file = get_excel_file(link, response['data'])

    if excel_file:
        file = excel_file.read()
    else:
        full_path_way = "template.xlsx"
        file = open(full_path_way, "rb").read()

    file_response = HttpResponse(file)
    file_response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    file_response['Content-Length'] = len(file)
    file_response['Content-Disposition'] = "attachment; filename=file.xlsx"
    return file_response
