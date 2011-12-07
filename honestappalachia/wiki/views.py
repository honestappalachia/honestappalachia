from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse

from forms import PageForm, MediaFileForm, BulkUploadForm
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
            return HttpResponseRedirect(reverse('media_index'))
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

import zipfile
import os
from datetime import datetime

def page_update_or_create(name, content):
    """Update or create a Wiki Page"""
    try:
        p = Page.objects.get(name=name)
    except Page.DoesNotExist:
        p = Page(name=name)
    finally:
        p.content = content
        p.save()

# idea: use messages (on wiki index page, or dashboard)
# to communicate results of these type of actions
# Info: Bulk upload successfully added 5 of 6 files
# Info: Did not add AboutUs.md, overwrite was off
# etc.

def handle_bulk_upload(f, overwrite):
    """Adds pages from uploaded file to Wiki"""
    fext = f.name.split(".")[-1]
    if fext == "md": # process single .md file
        name = f.name.split(".")[0]
        if Page.objects.filter(name=name) and not overwrite:
            # filter returns empty list, get raises a Model.DoesNotExist
            pass
        else:
            page_update_or_create(name, f.read())
    else: # process .zip archive
        zf = zipfile.ZipFile(f, 'r')
        flist = zf.namelist()
        for filename in flist:
            fext = filename.split(".")[-1]
            if fext == "md": # only process .md files
                name = filename.split(".")[0]
                if Page.objects.filter(name=name) and not overwrite:
                    # filter returns empty list, get raises a Model.DoesNotExist
                    pass
                else:
                    page_update_or_create(name, zf.read(filename))

@login_required
def bulk_upload(request):
    """Given a zip file of .md files, adds them as Wiki pages"""
    if request.method == 'POST':
        # validate form, process zip file
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_bulk_upload(
                form.cleaned_data['upload'],
                form.cleaned_data['overwrite_exisiting'])
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BulkUploadForm()

    context = {
        'form': form,
    }

    return render_to_response('wiki/bulk_upload.html',
            RequestContext(request, context))

@login_required
def bulk_download(request):
    """Saves all pages as .md files, zips them, and redirects to download"""
    # absolute path to zipfile to create, from MEDIA_ROOT
    zfname = os.path.join(settings.MEDIA_ROOT,
                          datetime.now().strftime("BULK-%Y%m%d-%H%M%S"))
    zf = zipfile.ZipFile(zfname, mode='w')
    pages = Page.objects.all()
    try:
        for p in pages:
            zf.writestr(p.name + ".md", p.content)
    finally:
        zf.close()

    return HttpResponseRedirect(settings.MEDIA_URL + zfname.split("/")[-1])
