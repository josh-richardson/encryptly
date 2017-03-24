import random
import string


# Generates a random string of length n
def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


# Gets a server side cookie
def get_ss_cookie(request, key, default_val=None):
    val = request.session.get(key)
    if not val:
        val = default_val
    return val
