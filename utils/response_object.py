from django.http import JsonResponse


def create_response_object(error, message):
    return JsonResponse({'error': error, 'data': message})