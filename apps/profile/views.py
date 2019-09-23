from django.http.response import HttpResponse


def index(request):  # todo profielpagin's maken -->  onder /leiding/naamslug zetten (dus ook een //leidng pagina
    return HttpResponse("Profile index")
