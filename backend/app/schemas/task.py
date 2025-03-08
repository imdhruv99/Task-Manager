from marshmallow import Schema, fields, validate, ValidationError, pre_load
from datetime import datetime

class TaskSchema(Schema):
    """Task schema with enhanced datetime handling"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(['todo', 'in_progress', 'done']),
        default='todo'
    )
    priority = fields.Str(
        validate=validate.OneOf(['low', 'medium', 'high']),
        default='medium'
    )
    due_date = fields.DateTime(
        allow_none=True,
        format='iso',  # Explicit ISO format requirement
        error_messages={
            'invalid': 'Invalid datetime format. Use ISO 8601 format (e.g. "2025-03-08T07:17:02Z")'
        }
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True

    @pre_load
    def preprocess_due_date(self, data, **kwargs):
        """Normalize due_date input before validation"""
        if 'due_date' in data and data['due_date']:
            # Handle date-only strings by adding default time
            if isinstance(data['due_date'], str):
                date_str = data['due_date'].strip()

                if len(date_str) == 10:  # YYYY-MM-DD format
                    data['due_date'] = f"{date_str}T00:00:00"
                elif len(date_str) > 10 and 'T' not in date_str:
                    # Convert space separator to T
                    data['due_date'] = date_str.replace(' ', 'T', 1)

        return data
