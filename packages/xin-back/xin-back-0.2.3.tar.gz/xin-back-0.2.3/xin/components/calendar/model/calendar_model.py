import mongoengine as me


class Calendar(me.Document):
    name = me.StringField(max_length=255, required=True)
    users = me.ListField(me.EmailField(max_length=255), required=True)
    meetings = me.ListField(me.ReferenceField("Meeting"))
