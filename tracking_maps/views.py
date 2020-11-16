from rest_framework.decorators import api_view, permission_classes
from utils.uni_api_view.universal_api_view import IsAuthenticated
from account.views import create_response_object
from tracking_maps import maps_methods as maps


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated, ])
def get_nomenclature(request):
    return create_response_object(error=False, data=maps.nomenclature_indexes_file)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated, ])
def get_tracking_map_data(request):
    nomenclatures = request.data.get('nomenclatures')
    filtered_data = maps.filter_data(nomenclatures, 'product')
    return create_response_object(error=False, data=filtered_data)
