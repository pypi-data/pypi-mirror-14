from utils import getvalue
import operator

class Filters(list):
    def apply(self, objects):
        for filter in self:
            objects = filter.apply(objects)
        return objects

    def __repr__(self):
        string = 'Filters='
        for item in sorted(self, key=operator.attrgetter('field_name')):
            string += str(item) + ';'
        return string

    def to_dict(self):
        """
        Doesn't include excludes or filters which are not exact or iexact
        """
        dictionary = {}
        for filter in self:
            if filter.operator == 'exact':
                dictionary[filter.field_name] = filter.value
            elif filter.operator == 'iexact':
                dictionary[filter.field_name] = filter.value.lower()
        return dictionary

class Filter(object):
    def __init__(self, field, operator, is_exclude, value):
        self.field = field
        self.field_name = field.column
        self.field_type = field.get_internal_type()
        self.operator = operator
        self.is_exclude = is_exclude
        self.value = value

    def __repr__(self):
        value = str(self.value).replace(', ', ',')
        return 'Filter=%s;%s;%s;%s' % (self.field_name, self.is_exclude, self.operator, value)

    def get(self, obj, sensitive=True):
        value = getvalue(obj, self.field_name, returnIfNone='')
        if not sensitive:
            return value.lower()
        return value

    def apply(self, objlist):
        if self.is_exclude:
            if self.operator == 'exact':
                return [d for d in objlist if not self.get(d) == self.value]
            elif self.operator == 'iexact':
                return [d for d in objlist if not self.get(d, sensitive=False) == self.value.lower()]
            elif self.operator == 'contains':
                return [d for d in objlist if not self.value in self.get(d)]
            elif self.operator == 'icontains':
                return [d for d in objlist if not self.value.lower() in self.get(d, sensitive=False)]
            elif self.operator == 'in':
                return [d for d in objlist if not self.get(d) in self.value]
            elif self.operator == 'gt':
                return [d for d in objlist if not self.get(d) > self.value]
            elif self.operator == 'gte':
                return [d for d in objlist if not self.get(d) >= self.value]
            elif self.operator == 'lt':
                return [d for d in objlist if not self.get(d) < self.value]
            elif self.operator == 'lte':
                return [d for d in objlist if not self.get(d) <= self.value]
            elif self.operator == 'startswith':
                return [d for d in objlist if not self.get(d).startswith(self.value)]
            elif self.operator == 'istartswith':
                return [d for d in objlist if not self.get(d, sensitive=False).lower().startswith(self.value.lower())]
            elif self.operator == 'endswith':
                return [d for d in objlist if not self.get(d).endswith(self.value)]
            elif self.operator == 'iendswith':
                return [d for d in objlist if not self.get(d, sensitive=False).endswith(self.value.lower())]
            elif self.operator == 'isnull':
                return [d for d in objlist if bool(self.get(d)) == self.value]
            else:
                raise NotImplementedError('Operator ' + self.operator + ' not supported.')
        else:
            if self.operator == 'exact':
                return [d for d in objlist if self.get(d) == self.value]
            elif self.operator == 'iexact':
                return [d for d in objlist if self.get(d, sensitive=False) == self.value.lower()]
            elif self.operator == 'contains':
                return [d for d in objlist if self.value in self.get(d)]
            elif self.operator == 'icontains':
                return [d for d in objlist if self.value.lower() in self.get(d, sensitive=False)]
            elif self.operator == 'in':
                return [d for d in objlist if self.get(d) in self.value]
            elif self.operator == 'gt':
                return [d for d in objlist if self.get(d) > self.value]
            elif self.operator == 'gte':
                return [d for d in objlist if self.get(d) >= self.value]
            elif self.operator == 'lt':
                return [d for d in objlist if self.get(d) < self.value]
            elif self.operator == 'lte':
                return [d for d in objlist if self.get(d) <= self.value]
            elif self.operator == 'startswith':
                return [d for d in objlist if self.get(d).startswith(self.value)]
            elif self.operator == 'istartswith':
                return [d for d in objlist if self.get(d, sensitive=False).lower().startswith(self.value.lower())]
            elif self.operator == 'endswith':
                return [d for d in objlist if self.get(d).endswith(self.value)]
            elif self.operator == 'iendswith':
                return [d for d in objlist if self.get(d, sensitive=False).endswith(self.value.lower())]
            elif self.operator == 'isnull':
                return [d for d in objlist if not bool(self.get(d)) == self.value]
            else:
                raise NotImplementedError('Operator ' + self.operator + ' not supported.')