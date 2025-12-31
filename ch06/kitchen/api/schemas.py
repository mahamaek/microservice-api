from marshmallow import Schema, fields, validate, EXCLUDE


class OrderItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    product = fields.String(required=True)

    size = fields.String(
        required=True,
        validate=validate.OneOf(['small', 'medium', 'big']))

    quantity = fields.Integer(
        required=True,
        validate=validate.Range(1, min_inclusive=True))
