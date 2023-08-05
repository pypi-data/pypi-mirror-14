from copy import copy

from rest_framework.serializers import HyperlinkedModelSerializer

from .utils import remove_empty, str_match_type, list_or_single_value, check_parse, remove_character


def get_key_value_filter(key_value, ns):
    # Receives {'field1': 'value1|value2', 'field2': 'value3,value4', 'field3': 'value5', 'field4': 'number'}
    # Returns this string:  "field1__range": ["value1", "value2"],
    #                       "field2__in": ["value3", "value4"],
    #                       "field3__icontains": "value5",
    #                       "field4": "number",
    #                       "field5": value_X  # A variable created in "ns" with the value
    to_filter = to_exclude = ''
    final_i = len(key_value)
    for i, (key, value) in enumerate(key_value.items()):

        if '.' in key:
            key = key.replace('.', '__')

        range_query = False  # Also filters boolean indirectly

        is_str = isinstance(value, str)
        is_bool = False if is_str else isinstance(value, bool)

        if is_str:
            # Range query case: "|", or Pipe
            # Multi value case: ",", or Comma
            # "value1|value2" or "value1,value2" turn into ["value1","value2"];
            # "value1," or "value1|" into ["1"]
            value = list_or_single_value(value, '|' if '|' in value else ',')
            if isinstance(value, list):
                is_str = is_bool = False
            range_query = False if is_bool or is_str or len(value) != 2 else True

        value = check_parse(value)

        # Or use the types of match queries ("contains", "startswith" etc.) or "range query"
        match_type, value = str_match_type(value) if not range_query else [False, value]
        # Set the name of the variable for exec's namespace
        ns_value = 'value_%s' % i
        # Handle single and multiple values mounting single query or "__in"/"__range" with a list
        key_value_string = (('"' + key +
                             ('__' + match_type if match_type else
                              ('__range' if range_query else
                               ('__in' if 'list' in value.__class__.__name__.lower() else ''))) +
                             '": ' + ns_value +
                             (', ' if i + 1 != final_i else '')))

        if not is_bool and is_str and value.startswith('-'):
            value = remove_character(value, 'first')
            to_exclude += key_value_string
        else:
            to_filter += key_value_string
        # Assign the value to the variable in namespace
        ns.update({ns_value: value})
    return to_filter, to_exclude


def set_serializer(instance=None, request=None, serializer=None, fields=[]):
    if (serializer or
            # Valid "serializer_class"
            (hasattr(instance, 'serializer_class') and instance.serializer_class) or
            # Valid "serializer_base" with a serializer class as value for attribute "base"
            (hasattr(instance, 'serializer_base') and 'base' in instance.serializer_base)):
        to_fields, to_exclude, raw_fields = [], [], []
        if request and 'fields' in request.query_params:
            raw_fields += remove_empty(request.query_params['fields'].split(','))
        elif fields:
            raw_fields += fields
        for raw_field in raw_fields:
            if raw_field.startswith('-'):
                to_exclude.append(remove_character(raw_field, 'first'))
            else:
                to_fields.append(raw_field)
        if not instance:
            instance = type('EmptyClass', (), {'serializer_class': None})()
        instance.serializer_class = serializer_factory(model=(instance.serializer_base['model']
                                                              if (hasattr(instance, 'serializer_base') and
                                                                  'model' in instance.serializer_base)
                                                              else None),
                                                       # "base" is priority here, but under "serializer"
                                                       base=(serializer if serializer
                                                             else (instance.serializer_class
                                                                   if 'base' not in instance.serializer_base
                                                                   else instance.serializer_base['base'])),
                                                       fields=tuple(to_fields), exclude=tuple(to_exclude))
    # assign it to "self.serializer_class"
    return instance.serializer_class


def serializer_factory(model=None, base=HyperlinkedModelSerializer, fields=None, exclude=None, order_by=None):
    # Source for this solution: http://stackoverflow.com/a/27468982/4694834
    attrs = {}
    if model:
        attrs.update({'model': model})
    # "fields" take priority over "exclude"
    if fields:
        if hasattr(base.Meta, 'exclude'):
            del base.Meta.exclude
        attrs.update({'fields': fields})
    if exclude and not fields:
        if hasattr(base.Meta, 'fields'):
            fields = list(base.Meta.fields)
            for field in exclude:
                fields.remove(field)
            attrs.update({'fields': tuple(fields)})
        else:
            attrs.update({'exclude': exclude})

    parent = (object,)
    if hasattr(base, 'Meta'):
        parent = (base.Meta, object)
    class_name = model.__name__ + 'Serializer' if model else (base.__name__ if base else 'CustomSerializer')
    return type(base)(class_name, (base,), {'Meta': type('Meta', parent, attrs)})


def select_fields(query_params, selected_fields):
    if selected_fields:
        dont_filter, do_filter = [], []
        for selected_field in selected_fields:  # Mount both selected and not selected fields
            if selected_field.startswith('-'):
                dont_filter.append(selected_field.replace('-', ''))
            else:
                do_filter.append(selected_field)
        new_query_params = copy(query_params)
        if do_filter or dont_filter:
            condition = 'key not in do_filter' if do_filter else 'key in dont_filter'  # Mount the string to eval
            for key, value in new_query_params.items():
                if eval(condition):
                    del query_params[key]

    return query_params


def filter_fields(objects: list, query_params):
    raw_fields = remove_empty(query_params['fields'].split(',')) if 'fields' in query_params else []

    result, exclude, fields = [], [], []

    for field in raw_fields:
        if field.startswith('-'):
            exclude.append(field.replace('-', ''))
        else:
            fields.append(field)

    for obj in objects:
        filtered_fields = {} if fields else obj.copy()
        for key, value in obj.items():
            if key in fields:
                filtered_fields[key] = obj[key]
            elif key in exclude and not fields:
                del filtered_fields[key]
        result.append(filtered_fields)

    return result
