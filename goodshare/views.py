from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/p' + str(request.user.id))
    else:
        context = Context({})
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context))
