import copy
import datetime
from collections import OrderedDict
from decimal import Decimal
from functools import wraps

from six import add_metaclass

#: Defines the version of the `normalazy` library.
__version__ = "0.0.2"


def iffnotnull(func):
    """
    Wraps a function, returns None if the first argument is None, invokes the method otherwise.

    :param func: The function to be wrapped.
    :return: None or the result of the function.

    >>> test1 = iffnotnull(lambda x: x)
    >>> test1(None)
    >>> test1(1)
    1
    """
    @wraps(func)
    def wrapper(value, *args, **kwargs):
        return None if value is None else func(value, *args, **kwargs)
    return wrapper


def iffnotblank(func):
    """
    Wraps a function, returns None if the first argument is empty, invokes the method otherwise.

    :param func: The function to be wrapped.
    :return: Empty string or the result of the function.

    >>> test1 = iffnotblank(lambda x: x)
    >>> test1("")
    ''
    >>> test1(1)
    1
    """
    @wraps(func)
    def wrapper(value, *args, **kwargs):
        return value if value == "" else func(value, *args, **kwargs)
    return wrapper


def identity(x):
    """
    Defines an identity function.

    :param x: value
    :return: value

    >>> identity(None)
    >>> identity(1)
    1
    """
    return x


@iffnotnull
def as_string(x):
    """
    Converts the value to a trimmed string.

    :param x: Value.
    :return: Trimmed string value.

    >>> as_string(None)
    >>> as_string("")
    ''
    >>> as_string("a")
    'a'
    >>> as_string(" a ")
    'a'
    """
    return str(x).strip()


@iffnotnull
def as_factor(x):
    """
    Converts the value to a factor string.

    :param x: Value.
    :return: Trimmed, up-cased string value.

    >>> as_factor(None)
    >>> as_factor("")
    ''
    >>> as_factor("a")
    'A'
    >>> as_factor(" a ")
    'A'
    """
    return as_string(x).upper()


@iffnotnull
@iffnotblank
def as_number(x):
    """
    Converts the value to a decimal value.

    :param x: The value to be converted to a decimal value.
    :return: A Decimal instance.

    >>> as_number(None)
    >>> as_number(1)
    Decimal('1')
    >>> as_number("1")
    Decimal('1')
    >>> as_number(" 1 ")
    Decimal('1')
    """
    return Decimal(as_string(x))


def as_boolean(x, predicate=None):
    """
    Converts the value to a boolean value.

    :param x: The value to be converted to a boolean value.
    :param predicate: The predicate function if required.
    :return: Boolean

    >>> as_boolean(None)
    False
    >>> as_boolean("")
    False
    >>> as_boolean(" ")
    True
    >>> as_boolean(1)
    True
    >>> as_boolean(0)
    False
    >>> as_boolean("1")
    True
    >>> as_boolean("0")
    True
    >>> as_boolean("1", predicate=lambda x: int(x) != 0)
    True
    >>> as_boolean("0", predicate=lambda x: int(x) != 0)
    False
    >>> as_boolean("1", predicate=int)
    True
    >>> as_boolean("0", predicate=int)
    False
    >>> as_boolean("1", int)
    True
    >>> as_boolean("0", int)
    False
    """
    return bool(x if predicate is None else predicate(x))


@iffnotnull
@iffnotblank
def as_datetime(x, fmt=None):
    """
    Converts the value to a datetime value.

    :param x: The value to be converted to a datetime value.
    :param fmt: The format of the date/time string.
    :return: A datetime.date instance.

    >>> as_datetime(None)
    >>> as_datetime("")
    ''
    >>> as_datetime("2015-01-01 00:00:00")
    datetime.datetime(2015, 1, 1, 0, 0)
    >>> as_datetime("2015-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
    datetime.datetime(2015, 1, 1, 0, 0)
    >>> as_datetime("2015-01-01T00:00:00", fmt="%Y-%m-%dT%H:%M:%S")
    datetime.datetime(2015, 1, 1, 0, 0)
    """
    return datetime.datetime.strptime(x, fmt or "%Y-%m-%d %H:%M:%S")


@iffnotnull
@iffnotblank
def as_date(x, fmt=None):
    """
    Converts the value to a date value.

    :param x: The value to be converted to a date value.
    :param fmt: The format of the date string.
    :return: A datetime.date instance.

    >>> as_date(None)
    >>> as_date('')
    ''
    >>> as_date("2015-01-01")
    datetime.date(2015, 1, 1)
    >>> as_date("Date: 2015-01-01", "Date: %Y-%m-%d")
    datetime.date(2015, 1, 1)
    >>> as_date("Date: 2015-01-01", fmt="Date: %Y-%m-%d")
    datetime.date(2015, 1, 1)
    """
    return datetime.datetime.strptime(x, fmt or "%Y-%m-%d").date()


class Value:
    """
    Defines an immutable *[sic.]* boxed value with message, status and extra data as payload if required.

    >>> value = Value(value=42, message=None, status=Value.Status.Success, extras="41 + 1")
    >>> value.value
    42
    >>> value.message
    >>> value.status == Value.Status.Success
    True
    >>> value.extras
    '41 + 1'
    >>> value = Value.success(42, date="2015-01-01")
    >>> value.value
    42
    >>> value.status == Value.Status.Success
    True
    >>> value.date
    '2015-01-01'
    >>> value = Value.warning(value="fortytwo", message="Failed to convert to integer.", date="2015-01-01")
    >>> value.value
    'fortytwo'
    >>> value.status == Value.Status.Warning
    True
    >>> value.date
    '2015-01-01'
    >>> value.message
    'Failed to convert to integer.'
    >>> value = Value.error(message="Failed to compute the value.", date="2015-01-01")
    >>> value.value
    >>> value.status == Value.Status.Error
    True
    >>> value.date
    '2015-01-01'
    >>> value.message
    'Failed to compute the value.'
    """

    class Status:
        """
        Defines an enumeration for value status.
        """

        #: Indicates that value is mapped successfully.
        Success = 1

        #: Indicates that value is mapped successfully with warnings.
        Warning = 2

        #: Indicates that value could not be mapped successfully.
        Error = 3

    def __init__(self, value=None, message=None, status=None, **kwargs):
        """
        Constructs an immutable Value class instance.

        Note that the classmethods `success`, `warning` and `error` should be preferred over this
        constructor.

        :param value: The atomic value.
        :param message: Any messages if required.
        :param status: The value status.
        :param kwargs: Extra payload for the value.
        """
        self.__value = value
        self.__status = status or self.Status.Success
        self.__message = message
        self.__payload = kwargs

    @property
    def value(self):
        return self.__value

    @property
    def status(self):
        return self.__status

    @property
    def message(self):
        return self.__message

    @property
    def payload(self):
        return self.__payload

    def __getattr__(self, item):
        """
        Provides access to payload through attributes.

        :param item: The name of the attribute.
        :return: The value for the attribute if the attribute name is in payload.
        """
        ## Check if the item is in the payload:
        if item in self.payload:
            ## Yes, return it.
            return self.payload.get(item)

        ## Nope, escalate:
        return super(Value, self).__getattr__(item)

    @classmethod
    def success(cls, value=None, message=None, **kwargs):
        """
        Provides a convenience constructor for successful Value instances.

        :param value: The value of the Value instance to be constructed.
        :param message: The message, if any.
        :param kwargs: Extra payload for the value.
        :return: A successful Value instance.
        """
        return cls(value=value, message=message, status=cls.Status.Success, **kwargs)

    @classmethod
    def warning(cls, value=None, message=None, **kwargs):
        """
        Provides a convenience constructor for Values instances with warnings.

        :param value: The value of the Value instance to be constructed.
        :param message: The message, if any.
        :param kwargs: Extra payload for the value.
        :return: A Value instance with warnings.
        """
        return cls(value=value, message=message, status=cls.Status.Warning, **kwargs)

    @classmethod
    def error(cls, value=None, message=None, **kwargs):
        """
        Provides a convenience constructor for Values instances with errors.

        :param value: The value of the Value instance to be constructed.
        :param message: The message, if any.
        :param kwargs: Extra payload for the value.
        :return: A Value instance with errors.
        """
        return cls(value=value, message=message, status=cls.Status.Error, **kwargs)


class Field(object):
    """
    Provides a concrete mapper field.

    >>> field = Field()
    >>> field.map(None, dict()).value
    >>> field.map(None, dict()).status == Value.Status.Success
    True
    >>> field = Field(null=False)
    >>> field.map(None, dict()).value
    >>> field.map(None, dict()).status == Value.Status.Error
    True
    >>> field = Field(func=lambda i, r: r.get("a", None))
    >>> field.map(None, dict(a="")).value
    ''
    >>> field.map(None, dict(a="")).status == Value.Status.Success
    True
    >>> field = Field(func=lambda i, r: r.get("a", None), blank=False)
    >>> field.map(None, dict(a="")).value
    ''
    >>> field.map(None, dict(a="")).status == Value.Status.Error
    True
    >>> field = Field(func=lambda i, r: r.get("a", None))
    >>> field.map(None, dict()).value
    >>> field.map(None, dict(a=1)).value
    1
    >>> field.map(None, dict(a=1)).status == Value.Status.Success
    True
    """

    def __init__(self, name=None, func=None, blank=True, null=True):
        """
        Constructs a mapper field with the given argument.

        :param name: The name of the field.
        :param func: The function which is to be used to map the value.
        :param blank: Boolean indicating if blank values are allowed.
        :param null: Boolean indicating if null values are allowed.
        """
        self.__name = name
        self.__func = func
        self.__blank = blank
        self.__null = null

    @property
    def name(self):
        """
        Returns the name of the field.

        :return: The name of the field.
        """
        return self.__name

    @property
    def func(self):
        """
        Returns the mapping function of the field.

        :return: The mapping function of the field.
        """
        return self.__func

    @property
    def blank(self):
        """
        Indicates if the value is allowed to be blank.

        :return: Boolean indicating if the value is allowed to be blank.
        """
        return self.__blank

    @property
    def null(self):
        """
        Indicates if the value is allowed to be null.

        :return: Boolean indicating if the value is allowed to be null.
        """
        return self.__null

    def rename(self, name):
        """
        Renames the field.

        :param name: The new name of the field.
        """
        self.__name = name

    def treat_value(self, value):
        """
        Treats the value and return.

        :param value: The value to be treated.
        :return: A Value instance.
        """
        ## By now we have a value. If it is an instance of Value
        ## class, return it as is:
        if isinstance(value, Value):
            return value

        ## If the value is string and empty, but is not allowed to be so, return
        ## with error:
        if not self.blank and isinstance(value, str) and value == "":
            return Value.error(value="", message="Value is not allowed to be blank.")

        ## If the value is None but is not allowed to be so, return
        ## with error:
        if not self.null and value is None:
            return Value.error(message="Value is not allowed to be None.")

        ## OK, we have a value to be boxed and returned successfully:
        return Value.success(value=value)

    def map(self, instance, record):
        """
        Returns the value of for field as a Value instance.

        :param instance: The instance for which the value will be retrieved.
        :param record: The raw record.
        :return: A Value instance.
        """
        ## Check if we have a function:
        if self.func is None:
            ## OK, value shall be None:
            value = None
        ## Check if the function is a callable or the name of an attribute of the instance:
        elif hasattr(self.func, "__call__"):
            ## The function is a callable. Call it directly on the
            ## instance and the record and get the raw value:
            value = self.func(instance, record)
        else:
            ## The function is not a callable. We assume that it is
            ## the name of a method of the instance. Apply the
            ## instance method on the record and get the raw value:
            value = getattr(instance, self.func)(record)

        ## Treat the value and return:
        return self.treat_value(value)


class KeyField(Field):
    """
    Provides a mapper field for a given key which belongs to the
    record. The record can be an object which has `__getitem__` method
    or a simple object just with attribute access.

    The method starts reading the source value using the key provided
    checking `__getitem__` method (for iterables such as `dict` or
    `list`), then checks the attribute for simple object attribute
    access.

    >>> field = KeyField(key="a")
    >>> field.map(None, dict(a="")).value
    ''
    >>> field.map(None, dict(a="")).status == Value.Status.Success
    True
    >>> field = KeyField(key="a", blank=False)
    >>> field.map(None, dict(a="")).value
    ''
    >>> field.map(None, dict(a="")).status == Value.Status.Error
    True
    >>> field = KeyField(key="a", func=lambda i, r, v: as_number(v))
    >>> field.map(None, dict(a="12")).value
    Decimal('12')
    >>> field.map(None, dict(a="12")).status == Value.Status.Success
    True
    """

    def __init__(self, key=None, **kwargs):
        """
        Constructs a mapper field with the given argument.

        :param key: The key of the property of the record to be mapped.
        :param **kwargs: Keyword arguments to `Field`.
        """
        super(KeyField, self).__init__(**kwargs)
        self.__key = key

    @property
    def key(self):
        """
        Returns the key of for the field mapping.
        """
        return self.__key

    def rename(self, name):
        """
        Renames the field.

        :param name: The new name of the field.
        """
        ## Call the super:
        super(KeyField, self).rename(name)

        ## If the key is None, set it with joy:
        if self.__key is None:
            self.__key = name

    def map(self, instance, record):
        """
        Returns the value of for field as a Value instance.

        :param instance: The instance for which the value will be retrieved.
        :param record: The raw record.
        :return: A Value instance.
        """
        ## Does the record have __getitem__ method (Indexable) and key exist?
        if hasattr(record, "__getitem__") and self.key in record:
            ## Yes, get the value:
            value = record.get(self.key)
        ## Nope, let's check if the record has such an attribute:
        elif hasattr(record, self.key):
            ## Yes, get the value using attribute access:
            value = getattr(record, self.key)
        ## We can't access such a value in the record.
        else:
            ## OK, Value shall be None:
            value = None

        ## Do we have a function:
        if self.func is None:
            ## Nope, skip:
            pass
        ## Check if the function is a callable or the name of an attribute of the instance:
        elif hasattr(self.func, "__call__"):
            ## The function is a callable. Call it directly on the
            ## instance, the record and the raw value:
            value = self.func(instance, record, value)
        else:
            ## The function is not a callable. We assume that it is
            ## the name of a method of the instance. Apply the
            ## instance method on the record and the raw value:
            value = getattr(instance, self.func)(record, value)

        ## Done, treat the value and return:
        return self.treat_value(value)


class ChoiceKeyField(KeyField):
    """
    Defines a choice mapper for the index of the record provided.

    >>> field = ChoiceKeyField(key="a", choices=dict(a=1, b=2))
    >>> field.map(None, dict(a="a")).value
    1
    >>> field = ChoiceKeyField(key="a", choices=dict(a=1, b=2), func=lambda i, r, v: Decimal(str(v)))
    >>> field.map(None, dict(a="a")).value
    Decimal('1')
    """

    def __init__(self, *args, **kwargs):
        ## Choices?
        choices = kwargs.pop("choices", {})

        ## Get the function:
        functmp = kwargs.pop("func", None)

        ## Compute the func
        if functmp is not None:
            func = lambda i, r, v: functmp(i, r, choices.get(v, None))
        else:
            func = lambda i, r, v: choices.get(v, None)

        ## Add the func back:
        kwargs["func"] = func

        ## OK, proceed as usual:
        super(ChoiceKeyField, self).__init__(*args, **kwargs)


class RecordMetaclass(type):
    """
    Provides a record metaclass.
    """

    def __new__(mcs, name, bases, attrs, **kwargs):
        ## Pop all fields:
        fields = dict([(key, attrs.pop(key)) for key in list(attrs.keys()) if isinstance(attrs.get(key), Field)])

        ## Check fields and make sure that names are added:
        for name, field in fields.items():
            if field.name is None:
                field.rename(name)

        ## Get the record class as usual:
        record_cls = super(RecordMetaclass, mcs).__new__(mcs, name, bases, attrs, **kwargs)

        ## Attach fields to the class:
        record_cls._fields = {}

        ## Now, process the fields:
        record_cls._fields.update(fields)

        ## Done, return the record class:
        return record_cls


@add_metaclass(RecordMetaclass)
class Record(object):
    """
    Provides a record normalizer base class.

    >>> class Test1Record(Record):
    ...     a = KeyField()
    >>> record1 = Test1Record(dict(a=1))
    >>> record1.a
    1
    >>> class Test2Record(Record):
    ...     a = KeyField()
    ...     b = ChoiceKeyField(choices={1: "Bir", 2: "Iki"})
    >>> record2 = Test2Record(dict(a=1, b=2))
    >>> record2.a
    1
    >>> record2.b
    'Iki'

    We can get the dictionary representation of records:

    >>> record1.as_dict()
    OrderedDict([('a', 1)])

    >>> record2.as_dict()
    OrderedDict([('a', 1), ('b', 'Iki')])

    Or detailed:

    >>> record1.as_dict(detailed=True)
    OrderedDict([('a', OrderedDict([('value', '1'), ('status', 1), ('message', None)]))])

    >>> record2.as_dict(detailed=True)
    OrderedDict([('a', OrderedDict([('value', '1'), ('status', 1), ('message', None)])), \
('b', OrderedDict([('value', 'Iki'), ('status', 1), ('message', None)]))])

    We can also create a new record from an existing record or dictionary:

    >>> class Test3Record(Record):
    ...     a = KeyField()
    ...     b = KeyField()
    >>> record3 = Test3Record.new(record2)
    >>> record3.a
    1
    >>> record3.b
    'Iki'
    >>> record3.a == record2.a
    True
    >>> record3.b == record2.b
    True

    With dictionary:

    >>> record4 = Test3Record.new({"a": 1, "b": "Iki"})
    >>> record4.a
    1
    >>> record4.b
    'Iki'
    >>> record4.a == record2.a
    True
    >>> record4.b == record2.b
    True

    Or even override some fields:

    >>> record5 = Test3Record.new(record3, b="Bir")
    >>> record5.a
    1
    >>> record5.b
    'Bir'
    """
    ## TODO: [Improvement] Rename _fields -> __fields, _values -> __value

    def __init__(self, record):
        ## Save the record slot:
        self.__record = record

        ## Declare the values map:
        self._values = {}

    def __getattr__(self, item):
        """
        Returns the value of the attribute named `item`, particularly from within the fields set or pre-calculated
        field values set.

        :param item: The name of the attribute, in particular the field name.
        :return: The value (value attribute of the Value).
        """
        return self.getval(item).value

    def hasval(self, name):
        """
        Indicates if we have a value slot called ``name``.

        :param name: The name of the value slot.
        :return: ``True`` if we have a value slot called ``name``, ``False`` otherwise.
        """
        return name in self._fields

    def getval(self, name):
        """
        Returns the value slot identified by the ``name``.

        :param name: The name of the value slot.
        :return: The value slot, ie. the boxed value instance of class :class:`Value`.
        """
        ## Did we compute this before?
        if name in self._values:
            ## Yes, return the value slot:
            return self._values.get(name)

        ## Do we have such a value slot?
        if not self.hasval(name):
            raise AttributeError("Record does not have value slot named '{}'".format(name))

        ## Apparently, we have never computed the value. Let's compute the value slot and return:
        return self.setval(name, self._fields.get(name).map(self, self.__record))

    def setval(self, name, value, status=None, message=None, **kwargs):
        """
        Sets a value to the value slot.

        :param name: The name of the value slot.
        :param value: The value to be set (Either a Python value or a :class:`Value` instance.)
        :param status: The status of the value slot if any.
        :param message: The message of the value slot if any.
        :param kwargs: Additional named values as payload to value.
        :return: The :class:`Value` instance set.
        """
        ## Do we have such a value slot?
        if not self.hasval(name):
            raise AttributeError("Record does not have value slot named '{}'".format(name))

        ## Create a value instance:
        if isinstance(value, Value):
            ## Get a copy of payload if any:
            payload = copy.deepcopy(value.payload)

            ## Update the payload with kwargs:
            payload.update(kwargs.copy())

            ## Create the new value:
            value = Value(value=value.value, status=status or value.status, message=message or value.message, **payload)
        else:
            value = Value(value=value, status=status or Value.Status.Success, message=message, **kwargs)

        ## Save the slot:
        self._values[name] = value

        ## Done, return the value set:
        return value

    def delval(self, name):
        """
        Deletes a stored value.

        :param name: The name of the value.
        """
        if name in self._values:
            del self._values[name]

    def allvals(self):
        """
        Returns all the value slots.

        :return: A dictionary of all computed value slots.
        """
        return {field: self.getval(field) for field in self._fields}

    def val_none(self, name):
        """
        Indicates if the value is None.

        :param name: The name of the value slot.
        :return: Boolean indicating if the value is None.
        """
        return self.getval(name).value is None

    def val_blank(self, name):
        """
        Indicates if the value is blank.

        :param name: The name of the value slot.
        :return: Boolean indicating if the value is blank.
        """
        return self.getval(name).value == ""

    def val_some(self, name):
        """
        Indicates if the value is something other than None or blank.

        :param name: The name of the value slot.
        :return: Boolean indicating if the value is something other than None or blank.
        """
        return not self.val_none(name) and not self.val_blank(name)

    def val_success(self, name):
        """
        Indicates if the value is success.

        :param name: The name of the value slot.
        :return: Boolean indicating if the value is success.
        """
        return self.getval(name).status == Value.Status.Success

    def val_warning(self, name):
        """
        Indicates if the value is warning.

        :param name: The name of the value slot.
        :return: Boolean indicating if the value is warning.
        """
        return self.getval(name).status == Value.Status.Warning

    def val_error(self, name):
        """
        Indicates if the value is error.

        :param name: The name of the value slot.
        :return: Boolean indicating if the value is error.
        """
        return self.getval(name).status == Value.Status.Error

    def as_dict(self, detailed=False):
        """
        Provides a JSON representation of the record instance.

        :param detailed: Indicates if we need detailed result, ie. with status and message for each field.
        :return: A JSON representation of the record instance.
        """
        ## We have the fields and values saved in the `_fields` and `_values` attributes respectively. We will
        ## simply iterate over these fields and their respective values.
        ##
        ## Let's start with defining the data dictionary:
        retval = OrderedDict([])

        ## Iterate over fields and get their values:
        for key in sorted(self._fields):
            ## Add the field to return value:
            retval[key] = getattr(self, key, None)

            ## If detailed, override with real Value instance:
            if detailed:
                ## Get the value:
                value = self._values.get(key, None)

                ## Add the value:
                retval[key] = OrderedDict([("value", str(value.value)),
                                           ("status", value.status),
                                           ("message", value.message)])

        ## Done, return the value:
        return retval

    @classmethod
    def new(cls, record, **kwargs):
        """
        Creates a new record from the provided record or dictionary and overriding values from the provided additional
        named arguments.

        :param record: The record or dictionary to be copied from.
        :param kwargs: Named arguments to override.
        :return: New record.
        """
        ## First of all, get the record as value dictionary:
        base = copy.deepcopy(record.as_dict() if isinstance(record, Record) else record)

        ## Update the dictionary:
        base.update(kwargs)

        ## Done, create the new record and return:
        return cls(base)
