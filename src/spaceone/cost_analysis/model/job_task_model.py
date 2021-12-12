from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class JobTask(MongoModel):
    job_task_id = StringField(max_length=40, generate_id='job-task', unique=True)
    status = StringField(max_length=20, default='PENDING',
                         choices=('PENDING', 'CANCELED', 'IN_PROGRESS', 'SUCCESS', 'FAILURE'))
    options = DictField()
    created_count = IntField(default=0)
    error_code = StringField(max_length=254, default=None, null=True)
    error_message = StringField(default=None, null=True)
    job_id = StringField(max_length=40, required=True)
    data_source_id = StringField(max_length=40, required=True)
    domain_id = StringField(max_length=40, required=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    started_at = DateTimeField(default=None, null=True)
    finished_at = DateTimeField(default=None, null=True)

    meta = {
        'updatable_fields': [
            'status',
            'created_count',
            'error_code',
            'error_message',
            'updated_at',
            'started_at',
            'finished_at'
        ],
        'ordering': [
            '-created_at'
        ],
        'indexes': [
            'job_task_id',
            'status',
            'job_id',
            'data_source_id',
            'domain_id',
            'created_at'
        ]
    }
