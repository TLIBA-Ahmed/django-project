from django.shortcuts import render
from django.views.generic import ListView , DetailView , CreateView, UpdateView, DeleteView
from .models import Conference
from django.http import HttpResponse
from django.urls import reverse_lazy
# Create your views here.

class ConferenceCreateView(CreateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    fields = "__all__"
    #fields = ['name', 'theme', 'description', 'start_date', 'end_date', 'location']
    success_url = reverse_lazy('list_conferences')

class ConferenceUpdateView(UpdateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    fields = "__all__"
    success_url = reverse_lazy('list_conferences')

class ConferenceDeletesView(DeleteView):
    model = Conference
    template_name = 'conference/conference_confirm_delete.html'
    success_url = reverse_lazy('list_conferences')

def home(request, name):
    return render(request, 'conference/home.html', context={'name': name})
# render pour charger un fichier

def welcome(request):
    return HttpResponse("<h2> Welcome to the Conference App ! </h2>")


#methode pour lister les conferences bil fonction
def listConferences(request):
    conferences = Conference.objects.all()
    return render(request, 'conference/list_conferences.html', {'confs': conferences}) 

#methode pour lister les conferences class 
class ConferenceListView(ListView):
    model = Conference
    template_name = 'conference/list_conferences.html'
    context_object_name = 'confs' #mnin bch tjib el list mteik (base de donnees) w t3ayetlha confs fel template


class ConferenceDetailsView(DetailView):
    model = Conference
    template_name = 'conference/conference_details.html'
    