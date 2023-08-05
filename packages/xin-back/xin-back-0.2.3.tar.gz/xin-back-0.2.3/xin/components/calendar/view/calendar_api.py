import mongoengine as me

from marshmallow_mongoengine import ModelSchema

from ..model import Calendar


event_calendar_creation = "calendar.created"


class CalendarSchema(ModelSchema):

    class Meta:
        model = Calendar
        model_build_obj = False


calendar_schema = CalendarSchema()


def create_calendar(name, users=None):
    if not users:
        # todo call auth module to get the current user
        users = ['test@test.com']
    res, err = calendar_schema.load({'name': name, 'users': users})
    if err:
        return {'_errors': err}
    calendar = Calendar(**res)
    calendar.save()
    return calendar_schema.dump(calendar).data, 200


def list_calendar(page=1, per_page=20):
    # users__contains=current_user.id
    from xin.bb.tools import paginate
    return paginate(calendar_schema, Calendar.objects, page, per_page), 200


def get_calendar(calendar_id):
    try:
        calendar = Calendar.objects.get(id=calendar_id)
    except me.DoesNotExist:
        return {'_errors': '404'}, 404
    return calendar_schema.dump(calendar).data, 200


def modify_calendar(calendar_id, name=None, users=None, append=False):
    errors = {}
    if not isinstance(append, bool):
        errors['append'] = 'Must be boolean'
    if name is not None and (not isinstance(name, str) or len(name) > 255):
        errors['name'] = 'Must be string or empty'
    if users is not None and not isinstance(users, list):
        errors['users'] = 'Must be list or empty'

    if users:
        if [u for u in users if not isinstance(u, str) or len(u) > 255]:
            errors['users'] = 'List element must be strings'

    if errors:
        return {'_errors': errors}, 400

    try:
        calendar = Calendar.objects.get(id=calendar_id)
    except me.DoesNotExist:
        return {'_errors': '404'}, 404
    if name:
        calendar.name = name
    if users:
        if append:
            calendar.users.extend(users)
        else:
            calendar.users = users
    calendar.save()
    return calendar_schema.dump(calendar).data, 200
