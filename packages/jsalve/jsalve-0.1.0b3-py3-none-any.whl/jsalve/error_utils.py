"""
Utilities for handling arbitrary errors and exceptions and transforming
their data into JSON API.
"""
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from . import utils as jsalve_utils


def make_error_object(status_code='400', pointer='/data', detail='Bad request'):
    """
    Returns:
         dict: The default basic error ``dict`` has ``status`` **'400'**, a source pointer to
    **'/data'** and error detail of **'Bad request'**.
    """
    if isinstance(status_code, int):
        #JSON API requires status code must be a string
        status_code = str(status_code)
    error_object = {
        'status': status_code,
        'source': {
            'pointer': pointer
        },
        'detail': detail
    }
    return error_object


def get_field_type(field, model):
    """
    Arguments:
        field (str): A string name for a resource field.
        model (object): A Django model class.
    Returns:
        str: A 'relationships' string if field represents a model relationship.
        Otherwise, returns 'attributes' string.
    """
    field_type = 'attributes'
    if model and hasattr(model, '_meta'):
        model_meta = model._meta
        model_field_type = model_meta.get_field(field)
        if isinstance(model_field_type, (ForeignKey, ManyToManyField, OneToOneField)):
            field_type = 'relationships'
    return field_type


def convert_to_error_objects(exception_detail, status_code,
                             model=None, non_field_errors_key='non_field_errors'):
    """
    Converts a Django REST Framework (DRF) validation error dict - typically an
    exception detail - into JSON API error objects.

    Arguments:
        exception_detail (dict): In DRF, this is expected to be a dict
            keyed to field names and/or a ``non-field error`` key. The values
            are lists of string; each string is an error explanation.
            ::

                {
                    'field1': ['errorA', 'errorB'],
                    'field2': ['errorA', 'errorB'],
                    'non_field_error': ['errorX', 'errorZ']
                }

        status_code (str): An HTTP status code (e.g. 400, 422, 500)
        model: A Django model
        non_field_errors_key (str): The key name for errors unrelated to a model
            field.

    Returns:
        list: A list of error object dictionaries. If no error objects are created, the list
        will be empty.
    """
    error_objects = list()
    # extract non-field errors
    if non_field_errors_key in exception_detail:
        detail_messages = exception_detail[non_field_errors_key]
        for message in detail_messages:
            error_object = make_error_object(status_code=status_code, detail=message)
            error_objects.append(error_object)
    # extract errors for each key; for model serializer errors, each key is a field's errors
    for field, detail_messages in exception_detail.items():
        for message in detail_messages:
            dasherized_field = jsalve_utils.format_value(field)
            field_type = get_field_type(field, model)
            pointer = '/data/{0}/{1}'.format(field_type, dasherized_field)
            error_object = make_error_object(status_code, pointer, message)
            error_objects.append(error_object)
    return error_objects
