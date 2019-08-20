from app import ma


class TagSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("uid", "name", "path")


tag_schema = TagSchema()

