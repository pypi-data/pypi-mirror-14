import mongoengine as me
from datetime import datetime

from xin.bb.tools import paginate
from xin.bb.view_util import BaseModelSchema

from ..model import Meeting, Calendar


event_meeting_creation = "meeting.created"


class MeetingSchema(BaseModelSchema):

    class Meta:
        model = Meeting


def create_meeting(calendar_id, name, users=None, date_begin=None, duration=60,
                   place="Undefined", comment=None, tags=None):
    try:
        calendar = Calendar.objects.get(id=calendar_id)
    except me.DoesNotExist:
        return {'_errors': '404'}, 404
    if not users or not len(users):
        # todo call auth module to get the current user
        users = calendar.users

    if not date_begin:
        date_begin = datetime.utcnow()

    meeting = Meeting(calendar=calendar_id, name=name, users=users,
                      tags=tags, comment=comment, begin=date_begin, duration=duration, place=place)
    meeting.save()
    return MeetingSchema().dump(meeting).data, 200


def list_meetings(calendar_id, page=1, per_page=20):
    # users__contains=current_user.id
    return paginate(MeetingSchema(), Meeting.objects(calendar=calendar_id), page, per_page), 200


def get_meeting(meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except me.DoesNotExist:
        return {'_errors': '404'}, 404
    return MeetingSchema().dump(meeting).data, 200


def modify_meeting(meeting_id, name=None, users=None, append=False, date_begin=None,
                   duration=None, place=None, comment=None, tags=None):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except me.DoesNotExist:
        return {'_errors': '404'}, 404
    if name:
        meeting.name = name
    if users and len(users):
        if append:
            meeting.users.extend(users)
        else:
            meeting.users = users
    if date_begin:
        meeting.begin = date_begin
    if duration:
        meeting.duration = duration
    if place:
        meeting.place = place
    if comment:
        meeting.comment = comment
    if tags:
        meeting.tags = tags

    meeting.save()
    dump = MeetingSchema().dump(meeting)
    return dump.data, 200


def delete_meeting(meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except me.DoesNotExist:
        return {'_errors': '404'}, 404
    meeting.delete()
    return 200
