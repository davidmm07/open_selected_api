from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError
import re
from email_validator import validate_email, EmailNotValidError
from app.models.users import Users

ma = Marshmallow()

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Users

    email = fields.Email(required=True)
    password = fields.String(required=True)

    @validates('email')
    def validate_email(self, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValidationError('Invalid email address.')

    @validates('password')
    def validate_password(self, value):
        if len(value) < 10:
            raise ValidationError('Password must be at least 10 characters long.')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[!@#?]', value):
            raise ValidationError('Password must contain at least one special character: !, @, #, or ?')
