from time import mktime
from datetime import datetime
from django.shortcuts import render
from django.db.models import Count
from website.apps.statistics.models import StatisticalValue, statistic

from website.apps.core.models import Family

GRAPH_START = datetime.strptime(
    "01 Apr 2013 00:00:00", "%d %b %Y %H:%M:%S"
)


def format_time_struct(date):
    return int(mktime(date)) * 1000

def get_xy(label, get_latest=False):
    x = [format_time_struct(GRAPH_START.timetuple()), ]
    y = [0, ]
    
    for i, row in enumerate(
        StatisticalValue.objects.get_all_with_dates(label)
    ):
        if i % 7 == 0:
            x.append(format_time_struct(row[1].timetuple()))
            y.append(row[0])
    
    # get_latest
    if get_latest:
        x.append(format_time_struct(datetime.now().timetuple()))
        y.append(float(statistic.get_statistic(label)))
    return {'x': x, 'y': y, 'name': label}


def make_family_chart(top=15):
    """Families by number of languages, largest first; the tail folded into 'Other'"""
    families = list(
        Family.objects.annotate(count=Count('language')).filter(count__gt=0).order_by('-count', 'family')
    )
    rows = [{'label': f.family, 'url': f.get_absolute_url(), 'count': f.count} for f in families[:top]]
    rest = families[top:]
    if rest:
        rows.append({'label': f'Other ({len(rest)} families)', 'url': None, 'count': sum(f.count for f in rest)})
    largest = max((r['count'] for r in rows), default=1)
    for r in rows:
        r['fraction'] = r['count'] / largest
    return {'label': 'Languages per Family', 'rows': rows}

    

def statistics(request):
    """Shows statistics"""
    out = {'charts': []}
    
    # add line graphs
    for i, label in enumerate(statistic.get_graphing(), 1):
        out['charts'].append({
            'label': label,
            'type': "lineChart",
            'id': 'chart_id_%d' % i,
            'data': get_xy(label, get_latest=True),
            'extra': {
                 'x_is_date': True,
                 'x_axis_format': "%d %b %Y",
            }
        })
    
    # add pie of languages / family
    out['family'] = make_family_chart()
    return render(request, 'statistics/details.html', out)
