from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from lazysignup.decorators import allow_lazy_user

#################################################################
# ASCII
#################################################################
@allow_lazy_user
def ascii(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('gofish/ascii.html', context_dict, context)

