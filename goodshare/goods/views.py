from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth import login, logout, authenticate

from goodshare.goods.models import Good, Type
from goodshare.accounts.models import Account

@login_required(login_url="/accounts/login")
def good_list_search(request):

    from goodshare.goods.forms import GoodSearchForm

    c = {}
    if request.method == 'POST':
        form = GoodSearchForm(request.POST)
        c['form'] = form
        if form.is_valid():
            name = None
            if 'name' in form.data:
                name = form.cleaned_data['name']
            good_type = None
            if 'type' in form.data:
                good_type = form.cleaned_data['type']

            if name is not None and good_type is not None:
                results = Good.objects.filter(
                    name__icontains=name, type=good_type).order_by('name')
            elif name is not None:
                results = Good.objects.filter(
                    name__icontains=name).order_by('name')
            elif good_type is not None:
                results = Good.objects.filter(type=good_type).order_by('name')
            else:
                results = Good.objects.all().order_by('name')

            if results.count() == 0:
                c['search_failed'] = "Nie znaleziono żadnej pozycji"
            else:
                c['results'] = results
        else:
            c['search_failed'] = "Wprowadzono błędne dane."

    c['form'] = GoodSearchForm()
    c.update(csrf(request))
    return render_to_response("goods/good_search.html", c,
                              context_instance=RequestContext(request))


@login_required(login_url="/accounts/login")
def good(request, good_id):
    good = get_object_or_404(Good, id=good_id)
    profiles = good.account_set.get_query_set()
    c = {'good': good, 'profiles': profiles}
    return render_to_response("goods/good.html", c,
                              context_instance=RequestContext(request))

@login_required(login_url="/accounts/login")
def add_good(request):

    from goodshare.goods.forms import GoodCreateForm

    c = {}
    if request.method == 'POST':
        form = GoodCreateForm(request.POST)
        if form.is_valid():
            new_good = form.save()
            return HttpResponseRedirect("/goods/g" + str(new_good.id))
        else:
            c['create_failed'] = "Podano niewłaściwe lub niepełne dane"

    c['form'] = GoodCreateForm()

    return render_to_response("goods/add_good.html", c,
                              context_instance=RequestContext(request))

@login_required(login_url="/accounts/login")
def add_good_to_user(request, good_id, user_id):
    profile = get_object_or_404(Account, id=user_id)
    good = get_object_or_404(Good, id=good_id)
    if request.user == profile:
        if profile.goods.filter(id=good.id).count() == 0:
            profile.goods.add(good)
            profile.save()
        return HttpResponseRedirect("accounts/p" + user_id)
    return HttpResponseRedirect("goods/g" + good_id)
