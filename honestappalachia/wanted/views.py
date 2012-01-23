from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from models import Story
from forms import StoryForm

def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            # manually set lat/lng
            story.lat = form.cleaned_data['lat']
            story.lng = form.cleaned_data['lng']
            story.save()
            return redirect(add_story)
    else:
        form = StoryForm()

    stories = Story.objects.all()

    return render_to_response('add_story.html', RequestContext(request,
        {
            'form': form,
            'stories': stories,
        }
    ))
