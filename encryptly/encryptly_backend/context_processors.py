from django.conf import settings

# Lets templates know if we're in debug mode
def debug(context):
    return {'DEBUG': settings.DEBUG}
