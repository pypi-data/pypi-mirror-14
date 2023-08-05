from xin.components.calendar.model.calendar_model import Calendar
from xin.components.calendar.view import (
    create_calendar, list_calendar, get_calendar, modify_calendar, event_calendar_creation)

from .common import BaseTest


class TestCalendarAPI(BaseTest):

    def test_create_calendar(self):
        r = create_calendar("test", ["test@test.com"])
        assert r[1] == 200
        objects = Calendar.objects()
        assert len(objects) == 1
        assert str(objects[0]['id']) == r[0]['id']

    def test_list_calendars(self):
        self.clean_db()
        r = create_calendar("test", ["test@test.com"])
        r = create_calendar("test2", ["test@test.com"])
        r = create_calendar("test3", ["test@test.com"])
        r = create_calendar("test4", ["test@test.com"])
        r = list_calendar()
        assert r[1] == 200
        assert len(r[0]['_items']) == 4

    def test_get_calendars(self):
        r = list_calendar()
        assert r[1] == 200
        assert len(r[0]['_items']) == 4
        r = get_calendar(r[0]['_items'][0]['id'])
        assert r[1] == 200
        assert r[0]['name'] == 'test'

    def test_modify_calendars(self):
        r = create_calendar("test", ["test@test.com"])
        assert r[1] == 200
        r = modify_calendar(calendar_id=r[0]['id'], name="new_name")
        assert r[1] == 200
        assert r[0]['name'] == 'new_name'
        r = modify_calendar(calendar_id=r[0]['id'], users=["pika@chu.com"])
        assert r[1] == 200
        assert len(r[0]['users']) == 1
        assert r[0]['users'][0] == "pika@chu.com"
        r = modify_calendar(calendar_id=r[0]['id'], users=["tor@tank.com"], append=True)
        assert r[1] == 200
        assert len(r[0]['users']) == 2
        assert r[0]['users'][0] == "pika@chu.com"
        assert r[0]['users'][1] == "tor@tank.com"
