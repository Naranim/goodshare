from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth import login, logout, authenticate

from goodshare.accounts.models import Account, Comment
from goodshare.goods.models import Good
from goodshare.places.models import Place


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/p" + str(request.user.id))

    from goodshare.accounts.forms import AccountCreationForm

    form = AccountCreationForm(request.POST)
    c = {'form': form}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data["alias"]
            password = form.cleaned_data["password1"]
            account = authenticate(username=username, password=password)
            login(request, account)
            return HttpResponseRedirect("/index.html")
        else:
            c['reg_failed'] = "Wprowadzono błędne dane"

    c.update(csrf(request))
    return render_to_response('accounts/register.html', c,
                              context_instance=RequestContext(request))


def login_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/p" + str(request.user.id))

    from django.contrib.auth.forms import AuthenticationForm

    form = AuthenticationForm(data=request.POST)
    c = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/index")
            else:
                c['log_failed'] = "Błędna nazwa użytkownika lub hasło"
        else:
            c['log_failed'] = "Wprowadzono błędne dane"

    c.update(csrf(request))
    return render_to_response("accounts/login.html", c,
                              context_instance=RequestContext(request))


@login_required(login_url="/accounts/login")
def logout_account(request):
    logout(request)
    return HttpResponseRedirect("/index")


@login_required(login_url="/accounts/login")
def profile(request, account_id):
    from goodshare.accounts.forms import CommentForm

    profile = get_object_or_404(Account, id=account_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["comment"]
            if len(text):
                from datetime import datetime
                comment = Comment(user=profile,
                                  creator=request.user,
                                  date=datetime.now(),
                                  comment=text)
                comment.save()

    goods = profile.goods.all()
    places = profile.places.all()
    comments = profile.get_comments()
    form = CommentForm()
    c = {'profile': profile,
        'goods': goods,
        'places': places,
        'rate': profile.get_rate(),
        'form': form,
        'comments': comments }
    return render_to_response("accounts/profile.html", c, context_instance=RequestContext(request))
