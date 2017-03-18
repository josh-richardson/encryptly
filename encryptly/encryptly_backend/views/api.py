import memcache
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

client = memcache.Client([('127.0.0.1', 11211)])


@csrf_exempt
def user_exists(request):
    return_dict = {'allowed': False, 'exists': False}
    if request.method == 'POST' and 'username' in request.POST:
        username = request.POST['username']
        if username.isalnum():
            client_address_key = "user-check-" + (request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR'])
            existing_entry = client.get(client_address_key)
            if not existing_entry or int(existing_entry) <= 5:
                return_dict['allowed'] = True
                client.set(client_address_key, int(existing_entry) + 1 if existing_entry else 1, 60)
                if User.objects.filter(username=username).count() != 0: return_dict['exists'] = True
    return JsonResponse(return_dict)

