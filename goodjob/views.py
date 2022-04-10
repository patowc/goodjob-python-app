import os
import datetime
import smtplib

import requests

from django.http import HttpResponse


def goodjob_view(request):
    r = None
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
        html += "<p style='color: blue;'>&nbsp;&nbsp;&nbsp;/&f=FICHERO&r=RESULTADO</p>"
    else:
        html += '<hr>'
        html += '<p>Has pasado:</p>'
        html += '<p>FICHERO: [%s]</p>' % str(fichero)
        html += '<p>RESULTADO: [%s]</p>' % str(resultado)
        html += '<hr>'

        try:
            r = requests.head(fichero)
        except Exception as e:
            html += "<p style='color: red;'>ERROR: %s</p>" % str(e)
            html += "</body></html>"
            return HttpResponse(html)

    length = r.headers.get('content-length', None)
    if not length:
        html += "<p style='color: red;'>ERROR: no puede leer el tamaño del fichero.</p>"
    else:
        try:
            length = int(length)
        except Exception as e:
            html += "<p style='color: red;'>ERROR: el tamaño del fichero [%s] no es correcto.</p>" % str(length)
            html += "</body></html>"
            return HttpResponse(html)

    try:
        resultado = int(resultado)
    except Exception as e:
        html += "<p style='color: red;'>ERROR: el valor de resultado [%s] no es correcto.</p>" % str(resultado)
        html += "</body></html>"
        return HttpResponse(html)

    validado = int(length/1024)

    if resultado == validado:
        email_address = os.getenv('ENV_EMAIL', None)
        password = os.getenv('ENV_PASSWORD', None)
        alumno = os.getenv('ENV_ALUMNO', None)
        if not email_address or not password or not alumno:
            html += "<p style='color: red;'><b>ERROR: no has definido ENV_EMAIL, ENV_PASSWORD o ENV_ALUMNO (o ninguna).</b></p>"
            html += "<p style='color: red;'><b>Para poder confirmar el ejercicio, debes poner estos variables en el entorno de Heroku.</b></p>"
            html += "</body></html>"
            return HttpResponse(html)

        body = 'Subject: [GOODJOB] Ejercicio resuelto.\nUn alumno [%s] ha resuelto el ejercicio.\n\n' % str(alumnos)
        try:
            smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
        except Exception as e:
            print(e)
            smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(email_address, password)
        smtpObj.sendmail(email_address, 'rramirez.ext@goodjob.es', body)

        smtpObj.quit()

    html += "<p style='color: green;'><b>PERFECTO, ¡LO HAS LOGRADO!</b></p>"
    html += "</body></html>"
    return HttpResponse(html)
