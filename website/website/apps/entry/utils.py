
def task_log(request, task, message):
    from website.apps.entry.models import TaskLog # has to be here for circular import
    return TaskLog.objects.create(
                person=request.user, 
                task=task,
                page=request.resolver_match.view_name, 
                message=message
    )
