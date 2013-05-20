from django.shortcuts import render
from website.apps.statistics.models import StatisticalValue
from time import mktime

WANTED_STATISTICS = [
    "Number of Languages", 
    "Number of Sources", 
    "Number of Words", 
    "Number of Lexical Items",
]

def get_dates():
    out = [] 
    for t in StatisticalValue.objects.filter(label="Number of Languages").order_by('date').values_list('date', flat=True):
        out.append(int(mktime(t.timetuple())))
    return out
    
def statistics(request):
    """Shows statistics"""
    extra = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": "%d %b %Y %H:%M:%S %p"
    }
    chartdata = {
        'x': get_dates(),
    }
    for i, label in enumerate(WANTED_STATISTICS, 1):
        chartdata["y%d" % i] = StatisticalValue.objects.get_all(label)
        chartdata["name%d" % i] = label
        chartdata["extra%d" % i] = extra
        
    import datetime
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 100
    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)
    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"},
                   "date_format": tooltip_date}
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie}
    charttype = "lineChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }

    return render(request, 'statistics/details.html', data)
    
    #return render(request, 'statistics/details.html', {'chartdata': chartdata,})

