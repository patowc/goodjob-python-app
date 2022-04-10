from django.http import HttpResponse
import datetime


def goodjob_view(request):
    error = False
    now = datetime.datetime.now()
    html = "<html><body>"

    html += "<p>La hora: %s.</p>" % now

    fichero = request.GET.get('f', None)
    resultado = request.GET.get('r', None)

    if not fichero:
        html += "<p style='color: red;'>No has indicado el fichero.</p>"
        error = True

    if not resultado:
        html += "<p style='color: red;'>No has indicado el resultado.</p>"
        error = True

    if error:
        html += '<hr>'
        html += "<p style='color: blue;'>Vuelve a llamar esta misma URL pasando:</p>"
        html += "<p style='color: red;'>&nbsp;&nbsp;&nbsp;/&f=<FICHERO>&r=<RESULTADO></p>"
    else:
        html += '<hr>'
        html += '<p>Has pasado:</p>'
        html += '<p>FICHERO: [%s]</p>' % str(fichero)
        html += '<p>RESULTADO: [%s]</p>' % str(resultado)

    html += "</body></html>"
    return HttpResponse(html)
