from django.contrib import messages
from social_django.middleware import SocialAuthExceptionMiddleware
from social_core import exceptions as social_exceptions
from django.http import HttpResponseRedirect


class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            msg = str(exception)
            messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(redirect_to='/core/vk_api_error/')
        else:
            return super(MySocialAuthExceptionMiddleware, self).process_exception(request, exception)
