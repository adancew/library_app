from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from datetime import date, timedelta
from shared.models import *
from shared.decorators import employee_required
from .forms import *

from .utils import *

@login_required
@employee_required 
def index(request, *args, **kwargs):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        return render(request, 'resources/res_index.html', 
                      {'resources':filter_resources_with_details(search_query)})
    else:
        return render(request, 'resources/res_index.html',
                      {'resources': filter_resources_with_details("")})



@login_required
def resource_detail(request, resource_id, *args, **kwargs):
    res_as_dict = get_resource_with_details(resource_id)
    return render(request, "resources/res_detail.html", {'resource': res_as_dict}) 


@login_required
@employee_required 
def resource_enter_pick(request, *args, **kwargs):
    return render(request, 'resources/res_pick.html', {})


@login_required
@employee_required 
def resource_enter(request, res_type, *args, **kwargs):
    
    if request.method == 'POST':
        
        if res_type == 'audiobook':
            form = EnterAudiobookForm(request.POST)
        elif res_type == 'book':
            form = EnterBookForm(request.POST)
        elif res_type == 'comic':
            form = EnterComicForm(request.POST)
        elif res_type == 'journal':
            form = EnterJournalForm(request.POST)
        elif res_type == 'movie':
            form = EnterMovieForm(request.POST)

        if form.is_valid():
            new_res = get_resource_from_form(form)
            new_res.save()
            # functions below create instance of book/comic ect and save it
            if (res_type=='audobook'):
                save_audiobook(form,new_res)
            elif (res_type=='book'):
                save_book(form, new_res)
            elif (res_type=='comic'):
                save_comic(form,new_res)
            elif (res_type=='journal'):
                save_journal(form,new_res)
            elif (res_type=='movie'):
                save_movie(form,new_res)
            
            messages.info(request, "dodano nowy zasób")
            return redirect('resources:resources-index')      
    else:
        
        if res_type == 'audiobook':
            form = EnterAudiobookForm()
        elif res_type == 'book':
            form = EnterBookForm()
        elif res_type == 'comic':
            form = EnterComicForm()
        elif res_type == 'journal':
            form = EnterJournalForm()
        elif res_type == 'movie':
            form = EnterMovieForm()
        
    return render(request, 'resources/res_enter.html', {'form': form})


# TODO doesn't quite fit the scenario yet
@login_required
@employee_required 
def resource_delete(request, resource_id, *args, **kwargs):
    
    try:
        resource = Resource.objects.get(id=resource_id)
        
        # check if the book is currently borrowed
        if Borrowing.objects.filter(resource_id=resource_id, status="UNDERWAY").count() > 0:
            raise Exception

        c = get_resource_category(resource_id)
        if c=='audiobook': Audiobook.objects.get(resource_id=resource_id).delete()
        elif c=='book': Book.objects.get(resource_id=resource_id).delete()
        elif c=='comic': Comic.objects.get(resource_id=resource_id).delete()
        elif c=='journal': Journal.objects.get(resource_id=resource_id).delete()
        elif c=='movie': Movie.objects.get(resource_id=resource_id).delete()

        resource.delete()
        messages.success(request, "Usuwanie zakończyło się sukcesem.")

    except:
        messages.error(request, "Usuwanie nie powiodło się.")

    return redirect('resources:resources-index')


@login_required
@employee_required 
def resource_edit(request, resource_id, *args, **kwargs):
    resource = Resource.objects.get(id=resource_id)
    res_type = get_resource_category(resource_id)

    if request.method == 'POST':
        
        if res_type == 'audiobook':
            form = EnterAudiobookForm(request.POST, initial = get_resource_with_details(resource_id))
        elif res_type == 'book':
            form = EnterBookForm(request.POST, initial = get_resource_with_details(resource_id))
        elif res_type == 'comic':
            form = EnterComicForm(request.POST, initial = get_resource_with_details(resource_id))
        elif res_type == 'journal':
            form = EnterJournalForm(request.POST, initial = get_resource_with_details(resource_id))
        elif res_type == 'movie':
            form = EnterMovieForm(request.POST, initial = get_resource_with_details(resource_id))
        
        if form.is_valid():
            
            old_resource = Resource.objects.get(id=resource_id)
            new_resource = get_resource_from_form(form)
            update_resource(old_resource, new_resource)

            if (res_type=='audobook'):
                update_audiobook(form,resource_id)
            elif (res_type=='book'):
                update_book(form, resource_id)
            elif (res_type=='comic'):
                update_comic(form,resource_id)
            elif (res_type=='journal'):
                update_journal(form,resource_id)
            elif (res_type=='movie'):
                update_movie(form,resource_id)

            messages.success(request, "Edycja danych zakończyła się sukcesem.")
            return redirect('resources:resources-index')
    else:
        if res_type == 'audiobook':
            form = EnterAudiobookForm(initial = get_resource_with_details(resource_id))
        elif res_type == 'book':
            form = EnterBookForm(initial = get_resource_with_details(resource_id))
        elif res_type == 'comic':
            form = EnterComicForm(initial = get_resource_with_details(resource_id))
        elif res_type == 'journal':
            form = EnterJournalForm(initial = get_resource_with_details(resource_id))
        elif res_type == 'movie':
            form = EnterMovieForm(initial = get_resource_with_details(resource_id))
        
    return render(request, 'resources/res_edit.html', 
                  {'form': form, 'resource':resource})

