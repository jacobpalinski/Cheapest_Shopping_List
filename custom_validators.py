import regex as re
from wtforms.validators import ValidationError
from property_notifier import *
import smtplib

# Validate email is a gmail or microsoft account
def email_from_options(form,field):
    valid_email_endings=['@gmail.com','@outlook.com', '@hotmail.com','@msn.com', '@live.com']
    if re.search(r'@.+',field.data).group(0) not in valid_email_endings:
        raise ValidationError('Please use a Gmail or Microsoft account when using this service')

# Validate email password is correct
class Email_Password:
    def __init__(self,fieldname):
        self.fieldname=fieldname
    
    def __call__(self,form,field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)

        customer_email=Customer_Email()

        if re.search(r'@.+',other.data).group(0)=='@gmail.com':
            smtp_server=customer_email.smtp_servers['Gmail']
            with smtplib.SMTP(smtp_server,customer_email.port) as server:
                server.starttls()
                try:
                    server.login(other.data,field.data)
                except (ValidationError,smtplib.SMTPAuthenticationError):
                    raise ValidationError('Incorrect password or not app-specific password. If no app specific password created go to https://support.google.com/mail/answer/185833?hl=en and follow instructions provided')
        
        elif re.search(r'@.+',other.data).group(0) in ['@outlook.com','@hotmail.com','@live.com','@msn.com']:
            smtp_server=customer_email.smtp_servers['Microsoft']
            with smtplib.SMTP(smtp_server,customer_email.port) as server:
                server.starttls()
                try:
                    server.login(other.data,field.data)
                except smtplib.SMTPAuthenticationError:
                    raise ValidationError('Incorrect password. Please enter correct password for email address')

# Validate suburb is a valid Australian suburb as per census data in property_notifier.py
def suburb_validation(form,field):
    suburbs=field.data.lower().title().replace(' And ',',').replace(' Or ',',').split(',')
    for suburb in suburbs:
        if suburb_state_dict.get(suburb)==None:
            raise ValidationError(f"{suburb} doesn't exist. Please enter a valid suburb. If multiple suburbs, seperate with comma leaving no whitespaces after commas eg. Madeley,Darch,East Perth")

# Validate minimum price is less than maximum price
class LessThan:
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data >= other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Field must be equal to %(other_name)s.')

            raise ValidationError(message % d)

# Validate None is selected for variable_loan_type if fixed rate loan is selected and Principal and Interest or Interest Only for variable rate loan
class CheckValidVariableLoanType: 
    def __init__(self,fieldname):
        self.fieldname=fieldname #loan_type field
    
    def __call__(self,form,field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if other.data=='Fixed' and field.data!='None':
            raise ValidationError('Please select None for fixed rate loan')
        elif other.data=='Variable' and field.data=='None':
            raise ValidationError('Please select Interest Only or Principal and Interest for variable rate loan')

# Validates loan term depending on loan type
class ValidLoanTerm:
    def __init__(self,fieldname):
        self.fieldname=fieldname #variable_loan_type field
    
    def __call__(self,form,field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if other.data=='None' and (field.data<1 or field.data>5):
            raise ValidationError('Enter loan term between 1-5 years')
        elif other.data=='Interest Only' and (field.data<5 or field.data>10):
            raise ValidationError('Enter loan term between 5-10 years')
        elif other.data=='Principal and Interest' and field.data not in [10,15,20,25,30]:
            raise ValidationError('Enter 10,15,20,25 or years as loan term')