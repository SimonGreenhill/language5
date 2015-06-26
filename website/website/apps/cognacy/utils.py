from website.apps.lexicon.models import CognateSet

def get_missing_cogids(limit=10):
    cogids = CognateSet.objects.all().values_list('id', flat=True)
    # handle no cognate case.
    if len(cogids) == 0:
        return range(1, limit + 1)
    
    # find the maximum cognate id and adding limit to it -- this 
    # means that we can iterate over things happily and always return
    # $limit records
    max_cog_id = max(cogids) + limit
    return [i for i in range(1, max_cog_id + 1) if i not in cogids][0:limit]

