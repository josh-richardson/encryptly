import random
import string


def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def get_ss_cookie(request, key, default_val=None):
    val = request.session.get(key)
    if not val:
        val = default_val
    return val
