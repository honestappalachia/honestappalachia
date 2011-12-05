from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from forms import PageForm, MediaFileForm
from models import Page, MediaFile

def main_page(request):
    return render_to_response('wiki/main_page.html',
            RequestContext(request, {}))

def index(request):
    """Lists all pages stored in the wiki."""
    context = {
        'pages': Page.objects.all(),
    }

    return render_to_response('wiki/index.html',
            RequestContext(request, context))

def media_index(request):
    """Lists all stored mediafiles"""
    mediafiles = MediaFile.objects.all()
    return render_to_response('wiki/media_index.html',
            { 'mediafiles': mediafiles },
            RequestContext(request, {})
        )

def view(request, name):
    """Shows a single wiki page."""
    try:
        page = Page.objects.get(name=name)
    except Page.DoesNotExist:
        page = Page(name=name)

    context = {
        'page': page,
    }

    return render_to_response('wiki/view.html',
            RequestContext(request, context))

@login_required
def edit(request, name):
    """Allows users to edit wiki pages."""
    try:
        page = Page.objects.get(name=name)
    except Page.DoesNotExist:
        page = None
        
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if not page:
                page = Page()
            page.name = form.cleaned_data['name']
            page.content = form.cleaned_data['content']

            page.save()
            return redirect(view, name=page.name)
    else:
        if page:
            form = PageForm(initial=page.__dict__)
        else:
            form = PageForm(initial={'name': name})

    context = {
        'form': form,
    }

    return render_to_response('wiki/edit.html',
            RequestContext(request, context))

@login_required
def delete(request, name):
    """Deletes a wiki page"""
    p = Page.objects.get(name=name)
    context = {
        'page': p,
    }
    p.delete()
    # rather than a hard delete, mark inactive?
    return render_to_response('wiki/delete.html',
            RequestContext(request, context))

@login_required
def media_upload(request):
    """Uploads a file to the media library"""
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wiki/media/') # TODO: something meaningful
    else:
        form = MediaFileForm()

    context = {
        'form': form,
    }

    return render_to_response('wiki/media_upload.html',
            RequestContext(request, context))

@login_required
def user_profile(request):
    """Shows a user's profile page"""
    return render_to_response('registration/profile.html',
            RequestContext(request, {})
        )
