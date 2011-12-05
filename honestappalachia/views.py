from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

import torcheck

def upload(request):
    """Check Tor status; redirect to hidden service if OK"""
    if torcheck.is_using_tor(request):
        # redirect to hidden service
        return redirect("http://www.google.com")
    else:
        return render_to_response("upload_notor.html",
                RequestContext(request, {}))
