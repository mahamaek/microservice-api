import uuid
from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint
import copy
from flask import abort

from marshmallow import ValidationError

from api.schemas import (
    GetScheduledOrderSchema,
    ScheduleStatusSchema,
    ScheduleOrderSchema,
    GetScheduledOrdersSchema,
    KitchenScheduleParameters
)

blueprint = Blueprint('Kitchen', __name__, description='Kitchen_API')

schedules = [
    {
        'id': str(uuid.uuid4()),
        'scheduled': datetime.now(),
        'status': 'pending',
        'order': [
            {
                'product': 'capuccino',
                'quantity': 1,
                'size': 'big'
            }
        ]
    }
]

schedules = []


def validate_schedule(schedule):
    schedule = copy.deepcopy(schedule)
    schedule['scheduled'] = schedule['scheduled'].isoformat()
    errors = GetScheduledOrderSchema().validate(schedule)
    if errors:
        raise ValidationError(errors)


@blueprint.route('/kitchen/schedules')
class KitchenSchedules(MethodView):
    @blueprint.arguments(KitchenScheduleParameters, location='query')
    @blueprint.response(status_code=200, schema=GetScheduledOrdersSchema)
    def get(self, parameters):
        # response validation with marshmallow
        for schedule in schedules:
            validate_schedule(schedule)

        if not parameters:
            return {'schedules': schedules}

        query_set = [schedule for schedule in schedules]
        in_progress = parameters.get('progress')
        if in_progress is not None:
            query_set = [
                schedule
                for schedule in schedules
                if schedule['status'] == 'progress'
            ]
        else:
            query_set = [
                schedule
                for schedule in schedules
                if schedule['status'] != 'progress'
            ]

        since = parameters.get('since')
        if since is not None:
            query_set = [
                schedule for schedule in schedules
                if schedule['scheduled'] >= since
            ]
        limit = parameters.get('limit')
        if limit is not None and len(query_set) > limit:
            query_set = query_set[:limit]

        return {'schedules': query_set}

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=201, schema=GetScheduledOrderSchema)
    def post(self, payload):
        payload['id'] = str(uuid.uuid4())
        payload['scheduled'] = datetime.utcnow()
        payload['status'] = 'pending'
        schedules.append(payload)
        validate_schedule(payload)
        return payload


@blueprint.route('/kitchen/schedules/<schedule_id>')
class KitchenSchedule(MethodView):

    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def get(self, schedule_id):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                validate_schedule(schedule)
                return schedule
        abort(404, description=f'Resoure with ID {schedule_id} not found')

    @blueprint.arguments(ScheduleOrderSchema)
    @blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
    def put(self, payload, schedule_id):
        for schedule in schedules:
            if schedule['id'] == schedule_id:
                schedule.update(payload)
                validate_schedule(schedule)
                return schedule
        abort(404, description=f'Resoure with ID {schedule_id} not found')

    @blueprint.response(status_code=204)
    def delete(self, schedule_id):
        for index, schedule in enumerate(schedules):
            if schedule['id'] == schedule_id:
                schedules.pop(index)
                return schedule
        abort(404, description=f'Resoure with ID {schedule_id} not found')
        return


@blueprint.route('/kitchen/schedules/<schedule_id>/cancel', methods=['POST'])
@blueprint.response(status_code=200, schema=GetScheduledOrderSchema)
def cancel_schedule(schedule_id):
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            schedules['status'] = 'cancelled'
            validate_schedule(schedule)
            return schedule
    abort(404, description=f'Resoure with ID {schedule_id} not found')


@blueprint.response(status_code=200, schema=ScheduleStatusSchema)
@blueprint.route('/kitchen/schedules/<schedule_id>/status', methods=['GET'])
def get_schedule_status(schedule_id):
    for schedule in schedules:
        if schedule['id'] == schedule_id:
            validate_schedule(schedule)
            return {'status': schedule['status']}
    abort(404, description=f'Resoure with ID {schedule_id} not found')
