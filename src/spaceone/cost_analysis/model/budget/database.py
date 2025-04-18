from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class PlannedLimit(EmbeddedDocument):
    date = StringField(required=True, max_length=7)
    limit = FloatField(default=0)


class Plan(EmbeddedDocument):
    threshold = FloatField(required=True)
    unit = StringField(max_length=20, required=True, choices=["PERCENT", "ACTUAL_COST"])

    def to_dict(self):
        return dict(self.to_mongo())


class Recipients(EmbeddedDocument):
    users = ListField(StringField(), default=[])

    def to_dict(self):
        return dict(self.to_mongo())


class Notification(EmbeddedDocument):
    state = StringField(max_length=20, required=True, choices=["ENABLED", "DISABLED"])
    plans = ListField(EmbeddedDocumentField(Plan), default=[])
    recipients = EmbeddedDocumentField(Recipients)

    def to_dict(self):
        return dict(self.to_mongo())


class Budget(MongoModel):
    budget_id = StringField(max_length=40, generate_id="budget", unique=True)
    name = StringField(max_length=255, default="")
    limit = FloatField(required=True)
    planned_limits = ListField(EmbeddedDocumentField(PlannedLimit), default=[])
    currency = StringField()
    time_unit = StringField(max_length=20, choices=["TOTAL", "MONTHLY"])
    start = StringField(required=True, max_length=7)
    end = StringField(required=True, max_length=7)
    notification = EmbeddedDocumentField(Notification)
    notified_months = ListField(StringField(max_length=10))
    utilization_rate = FloatField(null=True, default=0)
    tags = DictField(default={})
    resource_group = StringField(
        max_length=40, choices=["WORKSPACE", "PROJECT"]
    )  # leave WORKSPACE for previous version
    budget_manager_id = StringField(max_length=60, default=None, null=True)
    service_account_id = StringField(max_length=40)
    project_id = StringField(max_length=40, default=None, null=True)
    workspace_id = StringField(max_length=40, default=None, null=True)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by = StringField(max_length=255, null=True)

    meta = {
        "updatable_fields": [
            "name",
            "limit",
            "planned_limits",
            "start",
            "end",
            "notification",
            "notified_months",
            "utilization_rate",
            "tags",
            "budget_manager_id",
        ],
        "minimal_fields": [
            "budget_id",
            "name",
            "limit",
            "project_id",
            "service_account_id",
            "budget_manager_id",
        ],
        "change_query_keys": {"user_projects": "project_id"},
        "ordering": ["name"],
        "indexes": [
            "name",
            "resource_group",
            "service_account_id",
            "project_id",
            "workspace_id",
            "domain_id",
        ],
    }
