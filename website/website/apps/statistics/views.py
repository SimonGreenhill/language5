from time import mktime
from django.shortcuts import render
from website.apps.statistics.models import StatisticalValue

WANTED_STATISTICS = [
    "Number of Languages", 
    "Number of Sources", 
    "Number of Words", 
    "Number of Lexical Items",
]

def get_xy(label):
    x, y = [], []
    for row in StatisticalValue.objects.get_all_with_dates(label):
        x.append(int(mktime(row[1].timetuple())))
        y.append(row[0])
    return {'x': x, 'y': y, 'name': label}

def statistics(request):
    """Shows statistics"""
    out = {}
    out['charttype'] = "lineChart"
    out['charts'] = []
    
    for i, label in enumerate(WANTED_STATISTICS, 1):
        out['charts'].append({
            'label': label,
            'id': 'chart_id_%d' % i,
            'data': get_xy(label)
        })
        
    return render(request, 'statistics/details.html', out)
