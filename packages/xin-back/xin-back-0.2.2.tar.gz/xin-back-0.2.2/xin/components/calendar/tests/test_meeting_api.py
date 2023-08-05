from datetime import datetime

from xin.components.calendar.model.meeting import Meeting
from xin.components.calendar.view import create_calendar
from xin.components.calendar.view.meeting_api import (
    create_meeting, list_meetings, get_meeting, modify_meeting, event_meeting_creation)

from .common import BaseTest



def calendar_factory(name="test", users=["test@test.com"]):
    r = create_calendar("test", ["test@test.com"])
    return r[0]


class TestMeetingAPI(BaseTest):

    def test_create_meeting(self):
        calendar = calendar_factory()
        r = create_meeting(calendar_id=calendar['id'], name="first meeting", users=["pika@chu.com"],
                           duration="90", place="ici et la bas", comment="pourquoi pas", tags=['pokemon'])
        assert r[1] == 200
        objects = Meeting.objects()
        assert str(objects[0]['id']) == r[0]['id']

    def test_list_meeting(self):
        calendar = calendar_factory()
        r = create_meeting(calendar_id=calendar['id'], name="meeting1")
        r = create_meeting(calendar_id=calendar['id'], name="meeting2")
        r = create_meeting(calendar_id=calendar['id'], name="meeting3")
        r = create_meeting(calendar_id=calendar['id'], name="meeting4")
        r = create_meeting(calendar_id=calendar['id'], name="meeting5")
        r = list_meetings(calendar['id'])
        assert r[1] == 200
        assert len(r[0]['_items']) == 5

    def test_get_meeting(self):
        calendar = calendar_factory()
        r = create_meeting(calendar_id=calendar['id'], name="meeting1")
        r = get_meeting(r[0]['id'])
        assert r[1] == 200
        assert r[0]['name'] == "meeting1"

    def test_modify_meeting(self):
        calendar = calendar_factory()
        r = create_meeting(calendar_id=calendar['id'], name="meeting1")
        r = get_meeting(r[0]['id'])
        assert r[1] == 200
        assert r[0]['name'] == "meeting1"
        r = modify_meeting(r[0]['id'], name="new_name")
        assert r[1] == 200
        assert r[0]['name'] == "new_name"
        r = modify_meeting(r[0]['id'], users=["pika@chu.com"])
        assert r[1] == 200
        assert len(r[0]['users']) == 1
        assert r[0]['users'][0] == "pika@chu.com"
        r = modify_meeting(r[0]['id'], users=["tor@chu.com"], append=True)
        assert r[1] == 200
        assert len(r[0]['users']) == 2
        assert r[0]['users'][1] == "tor@chu.com"
        r = modify_meeting(r[0]['id'], date_begin=datetime(2007, 12, 5, 12, 00))
        assert r[1] == 200
        #assert r[0]['begin'] == str(datetime(2007, 12, 5, 12, 00))
        r = modify_meeting(r[0]['id'], duration=100)
        assert r[1] == 200
        assert r[0]['duration'] == 100
        r = modify_meeting(r[0]['id'], place="defined")
        assert r[1] == 200
        assert r[0]['place'] == "defined"
