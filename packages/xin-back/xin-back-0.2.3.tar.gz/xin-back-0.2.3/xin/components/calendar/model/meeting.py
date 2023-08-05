import mongoengine as me


class Meeting(me.Document):
    calendar = me.ReferenceField("Calendar", required=True)
    name = me.StringField(max_length=120, required=True)
    users = me.ListField(me.EmailField(max_length=255), required=True)
    begin = me.DateTimeField(required=True)
    duration = me.IntField(required=True)
    place = me.StringField(max_length=255)
    tags = me.ListField(me.StringField(max_length=20))
    comment = me.StringField(max_length=255)
