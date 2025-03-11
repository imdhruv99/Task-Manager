from marshmallow import Schema, fields, validate, validates, ValidationError

class TaskSchema(Schema):
    """Task schema for validation and serialization."""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(['todo', 'in_progress', 'done']), default='todo')
    priority = fields.Str(validate=validate.OneOf(['low', 'medium', 'high']), default='medium')
    due_date = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('title')
    def validate_title(self, value):
        """Validate title."""
        if not value.strip():
            raise ValidationError('Title cannot be empty.')

# Create schema instances
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
