from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from rest_framework import serializers
from .methods import set_serializer, get_key_value_filter, select_fields
from .utils import mix_dicts_self_params, takeoff_list, remove_empty


class CountSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()


class UrlFilterModelViewSet(ModelViewSet):
    # HIGHLY IMPORTANT NOTE: DON'T PERFORM "UPDATE" TO THESE, OR ALL YOUR REQUEST WILL APPLY IT!!!!! D:
    default_filter = {}  # example: {'field1': 'value1', 'field2': 'value2'}
    aliases = {}  # example: {'key_to_show1': 'key_to_search1', 'key_to_show2': 'key_to_search2'}
    serializer_base = {}  # example: {'model': Class, 'base': ClassSerializer}

    def list(self, request, *args, **kwargs):
        quantity = request.query_params.get('quantity', 'false').lower() == 'true'
        many = not quantity
        self.serializer_class = CountSerializer if quantity else set_serializer(self, request)
        filtered_list = self.qp_filter(self.queryset, request)
        serialize = self.serializer_class(filtered_list, many=many)
        return Response(serialize.data)

    def qp_filter(self, query_obj, request,
                  default_filter=None,
                  aliases=None,
                  selected_fields=None,
                  perform='filter',
                  priority_perform='self',
                  priority_filter='params',
                  priority_aliases='params'):
        """
        :param selected_fields: specify the fields to be filtered | Example: ['filter_me', 'and_me'] & ['-not_me']
        :param priority_perform: set priority to define method to perform | Values: 'self' & 'params'
        :param priority_aliases: set priority to join the aliases | Values: 'self' & 'params'
        :param priority_filter: set priority to join the default filters | Values: 'self' & 'params'
        :param perform: type of query | Values: 'filter' & 'get'
        :param aliases: switch keys between search and display
        :param default_filter: custom filter (receives a dict)
        :param query_obj: sort of "model.objects" (comes without "all()", "filter()" etc.)
        :param request: request with filter options at query_params
        :return: filtered query, or default if there's no query params
        """

        default_filter = mix_dicts_self_params(self.default_filter, default_filter, priority_filter)

        if not len(request.query_params) and not default_filter:  # if there's nothing to filter, return all
            return query_obj.all()

        aliases = mix_dicts_self_params(self=self.aliases, params=aliases, priority=priority_aliases)

        # Mix the "default_filter" with the "query_params" treated from request, based on the "priority_filter"
        query_params = mix_dicts_self_params(default_filter, takeoff_list(dict(request.query_params)), priority_filter)

        ns = {'result_query': None, 'query_set': query_obj}  # namespace for exec

        if 'fields' in query_params:
            del query_params['fields']
        if 'exclude' in query_params:
            del query_params['exclude']

        query_params = select_fields(query_params, selected_fields)

        quantity = True if query_params.pop('quantity', 'false').lower() == 'true' else None

        # Need to take it off query_params to have no effect at "len(query_params)", so I used "raw_perform"
        raw_perform = query_params.pop('perform', None)
        if priority_perform == 'params' and raw_perform:
            perform = raw_perform

        distinct = to_filter = order_by = None

        if aliases:
            # aliases example: {'key_to_show1': 'key_to_search1', 'key_to_show2': 'key_to_search2'}
            for key, value in aliases.items():
                if key in query_params:
                    query_params[value] = query_params.pop(key)

        order_by_opts = query_params.pop('order_by', None)
        distinct_opts = query_params.pop('distinct', None)

        if isinstance(distinct_opts, str):  # Allow empty params
            # Example: ?distinct=field
            distinct = ''
            distinct_opts = remove_empty(distinct_opts.split(','))
            for i, item in enumerate(distinct_opts):
                distinct += ('"%s"' + (', ' if i + 1 != len(distinct_opts) else '')) % item
            # ")" is out for empty param case
            # The default "order_by" is breaking the request (don't know why, so I moved it to the result of the query)
            distinct = '.order_by().distinct(' + distinct + ')'
            # Final: .distinct("field1") or .distinct()

        if order_by_opts:
            # Example: ?order_by=field1,field2
            order_by = ''
            order_by_opts = remove_empty(order_by_opts.split(','))
            for i, item in enumerate(order_by_opts):
                order_by += ('"%s"' + (', ' if i + 1 != len(order_by_opts) else ')')) % item

            if order_by:
                order_by = '.order_by(' + order_by
            # Final: .order_by("field1", "field2")

        # Note: gotta pop all query options out of query_params before actually mount the filter
        if len(query_params):  # fields to filter
            if priority_perform == 'params':
                perform = query_params.pop('perform', perform)
            to_filter, to_exclude = get_key_value_filter(query_params, ns)
            # Empty params case (e.g. "?field1=&field2=")
            if to_filter:
                to_filter = (('.%s(**{%s})' % (perform, to_filter)) +
                             (('.exclude(**{%s})' % to_exclude) if to_exclude and perform == 'filter' else ''))

        # Mount query options in the string
        query_opts = '{distinct}{filter}'.format(**{
            'distinct': (distinct if distinct else ''),
            'filter': (to_filter if to_filter else '')
        })

        # Mount the code in string to execute
        exec('result_query = query_set' +
             (query_opts if query_opts else '.all()') +
             ('.count()' if quantity else '') +
             (('; result_query = result_query%s;' % order_by) if order_by else ''),
             ns)

        if isinstance(ns['result_query'], int):
            ns['result_query'] = {'quantity': ns['result_query']}

        return ns['result_query'] if ns['result_query'] is not None else query_obj
