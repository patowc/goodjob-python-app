from django.http import HttpResponse
import datetime

def goodjob_view(request):
    now = datetime.datetime.now()
    html = "<html><body>La hora: %s.</body></html>" % now
    return HttpResponse(html)
