# coding: utf-8
"""Base class for all Mambu objects.

Includes functionality to download such objects using GET requests to
Mambu, and to POST requests to Mambu.

Some caching may be achieved. Please look at caching done at
mambuproduct.AllMambuProducts class for an example of how caching should
be done.

Official Mambu dev documentation at Mambu Developer Center:
https://developer.mambu.com

You must configure your Mambu client in mambuconfig.py Please read the
pydocs there for more information.

Some basic definitions:

* MambuStruct refers to the parent class of all Mambu Objects and

* MambuPy Mambu objects refers to any child of MambuStruct, usually
defined at some mambu-somename- python module file. Sometimes referred
as implemented MambuStruct or something fancy

* Mambu entity refers to an entity retrieved via a request via Mambu
REST API. It's a more abstract thing in fact. Also may refer to entities
on a relational database but the term table is preferred in this case.
"""

from mambuutil import MambuCommError, MambuError, OUT_OF_BOUNDS_PAGINATION_LIMIT_VALUE, iriToUri, encoded_dict

from urllib import urlopen, urlencode
import json
from datetime import datetime

import logging

def setup_logging(default_path='mambulogging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    import os, logging.config, yaml
    from codecs import open as copen
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with copen(path, 'rt', 'utf-8') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

logger = logging.getLogger(__name__)
"""The logger.

TODO: no logging is currently done at MambuPy. At least here it gets
configured...
"""

class RequestsCounter(object):
    """Singleton that counts requests.

    If you want to control the number of requests you do to Mambu, you
    may find this counter useful. Since it is a Singleton, every Mambu
    object shares it and increases the amount of requests counted here,
    so you may read it on every Mambu object you have per Python
    session you hold.
    """
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(RequestsCounter, cls).__new__(cls, *args, **kwargs)
            cls.requests = []
            cls.cnt = 0
        return cls.__instance
    def add(cls, temp):
        cls.requests.append(temp)
        cls.cnt += 1
    def reset(cls):
        cls.cnt = 0
        cls.requests = []


class MambuStructIterator:
    """Enables iteration for some Mambu objects that may want to have iterators.

    Loans, Transactions, Repayments, Clients, Groups, Users, Branches
    are some of the Mambu entitites that may be iterable. Here at
    MambuPy, all of them have an iterator class for requesting several
    entitites to Mambu, instead of just one of them. Please refer to
    each MambuObject pydoc for more info.
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.offset = 0

    def next(self):
        if self.offset >= len(self.wrapped):
            raise StopIteration
        else:
            item = self.wrapped[self.offset]
            self.offset += 1
            return item

class MambuStruct(object):
    """This one is the Father of all Mambu objects at MambuPy.

    It's a dictionary-like structure by default, self.attr attribute
    holds all the info respondend by Mambu REST API.

    This object is flexible enough to hold a list instead of a
    dictionary for certain objects holding iterators.

    Further work is needed to hold list-like behaviour however.
    """
    setup_logging()

    RETRIES = 5
    """This one holds the maximum number of retries for requests to Mambu.

    Some networks have a lot of lag, so a safe maximum has been added
    here. If after RETRIES attempts to connect to Mambu, MambuPy can't
    connect, a MambuCommError will be raised.
    """

    @staticmethod
    def serializeFields(data):
        """Turns every attribute of the Mambu object in to a string representation.

        If the object is an iterable one, it goes down to each of its
        elements and turns its attributes too, recursively.

        The base case is when it's a MambuStruct class (this one) so it
        just 'serializes' the attr atribute. Refer to
        MambuStruct.serializeStruct pydoc.

        This is perhaps the worst way to do it, still looking for a better way.
        """
        if isinstance(data, MambuStruct):
            return data.serializeStruct()
        try:
            it = iter(data)
        except TypeError as terr:
            return unicode(data)
        if type(it) == type(iter([])):
            l = []
            for e in it:
                l.append(MambuStruct.serializeFields(e))
            return l
        elif type(it) == type(iter({})):
            d = {}
            for k in it:
                d[k] = MambuStruct.serializeFields(data[k])
            return d
        # elif ... tuples? sets?
        return unicode(data)

    def __getitem__(self, key):
        """Dict-like key query"""
        return self.attrs[key]

    def __setitem__(self, key, value):
        """Dict-like set"""
        self.attrs[key] = value

    def __repr__(self):
        """Mambu object repr tells the class name and the usual 'id' for it.

        If an iterable, it instead gives its length.
        """
        try:
            return self.__class__.__name__ + " - id: %s" % self.attrs['id']
        except AttributeError:
            return self.__class__.__name__ + " - id: '%s' (not synced with Mambu)" % self.entid
        except TypeError:
            return self.__class__.__name__ + " - len: %s" % len(self.attrs)

    def __str__(self):
        """Mambu object str gives a string representation of the attrs attribute."""
        try:
            return self.__class__.__name__ + " - " + str(self.attrs)
        except AttributeError:
            return self.__class__.__name__ + " - " + str(self)

    def __len__(self):
        """Length of the attrs attribute.

        If dict-like (not iterable), it's the number of keys holded on the attrs dictionary.
        If list-like (iterable), it's the number of elements of the attrs list.
        """
        return len(self.attrs)

    def __eq__(self, other):
        """Very basic way to compare to Mambu objects.

        Only looking at their EncodedKey field (its primary key on the
        Mambu DB).

        TODO: a lot of improvements may be done here.
        """
        if isinstance(other, MambuStruct):
            try:
                if not other.attrs.has_key('encodedKey') or not self.attrs.has_key('encodedKey'):
                    return NotImplemented
            except AttributeError:
                return NotImplemented
            return other['encodedKey'] == self['encodedKey']

    def has_key(self, key):
        """Dict-like behaviour.

        TODO: throw NotImplemented exception when not a dict
        """
        return self.attrs.has_key(key)

    def items(self):
        """Dict-like behaviour.

        TODO: throw NotImplemented exception when not a dict
        """
        return self.attrs.items()

    def init(self, attrs={}, *args, **kwargs):
        """Default initialization from a dictionary responded by Mambu
        in to the elements of the Mambu object.

        It assings the response to attrs attribute and converts each of
        its elements from a string to an adequate python object: number,
        datetime, etc.

        Basically it stores the response on the attrs attribute, then
        runs some customizable preprocess method, then runs
        convertDict2Attrs method to convert the string elements to an
        adequate python object, then a customizable postprocess method.

        It also executes each method on the 'methods' attribute given on
        instantiation time, and sets new customizable 'properties' to
        the object.

        Why not on __init__? two reasons:

        * __init__ optionally connects to Mambu, if you don't connect to
        Mambu, the Mambu object will be configured but it won't have any
        Mambu info on it. Only when connected, the Mambu object will be
        initialized, here.

        Useful to POST several times the same Mambu object. You make a
        POST request over and over again by calling it's connect()
        method every time you wish. This init method will configure the
        response in to the attrs attribute each time.

        You may also wish to update the info on a previously initialized
        Mambu object and refresh it with what Mambu now has. Instead of
        building a new object, you just connect() again and it will be
        refreshed.

        * Iterable Mambu objects (lists) do not initialize here, the
        iterable Mambu object __init__ goes through each of its elements
        and then initializes with this code one by one. Please look at
        some Mambu iterable object code and pydoc for more details.
        """
        self.attrs = attrs
        self.preprocess()
        self.convertDict2Attrs(*args, **kwargs)
        self.postprocess()
        try:
            for meth in kwargs['methods']:
                try:
                    getattr(self,meth)()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            for propname,propval in kwargs['properties'].iteritems():
                try:
                    setattr(self,propname,propval)
                except Exception:
                    pass
        except Exception:
            pass

    def serializeStruct(self):
        """Makes a string from each element on the attrs attribute.

        Read the class attribute MambuStruct.serializeFields pydoc for
        more info.

        It DOES NOT serializes the class, for persistence or network
        transmission, just the fields on the attrs attribute.

        Remember that attrs may have any type of elements: numbers,
        strings, datetimes, Mambu objects, etc. This is a way to convert
        it to a string in an easy, however ugly, way.

        WARNING: it may fall in a stack overflow, TODO check recursion levels.
        """
        serial = MambuStruct.serializeFields(self.attrs)
        return serial

    def __init__(self, urlfunc, entid='', *args, **kwargs):
        """Initializes a new Mambu object.

        urlfunc is the only required parameter. The urlfunc returns a
        string of the URL to make a request to Mambu. You may read about
        the valid urlfuncs supported by MambuPy at mambuutil.py

        If you send a None urlfunc, the object will be configured, but
        won't connect to Mambu, never. Useful for iterables that
        configure their elements but can't or won't need Mambu to send
        further information. See MambuRepayments for an example of this.

        Should you need to add support for more functionality, add them
        at mambuutuil.

        entid is the usual ID of a Mambu entity you like to GET from
        Mambu. The ID of a loan account, a client, a group, etc. Or the
        transactions or repayments of certain loan account. It's an
        optional parameter because the iterable Mambu objects don't need
        an specific ID, just some other filtering parameters supported
        on the urlfunc function.

        Many other arguments may be sent here to further configure the
        Mambu object or the response by Mambu REST API:

        * debug flag (currently not implemented, just stored on the object)
        * connect flag, to optionally omit the connection to Mambu (see
          the init() (with no underscores) method pydoc)
        * data parameter for POST requests (see connect() method pydoc)
        * dateFormat parameter (see util_dateFormat() method pydoc)

        Also, parameters to be sent to Mambu on the request, such as:
        * limit parameter (for pagination, see connect() method pydoc)
        * offset parameter (for pagination, see connect() method pydoc)
        * fullDetails, accountState and other filtering parameters (see
          mambuutil pydocs)
        * user, password, url to connect to Mambu, to bypass mambuconfig
          configurations (see mambuutil pydoc)
        """

        self.entid = entid
        """ID of the Mambu entity, or empty if not wanting a specific entity to be GETted"""

        self.rc = RequestsCounter()
        """Request Count Singleton"""

        try:
            self.__debug=kwargs['debug']
            """Debug flag.

            TODO: not currently furtherly implemented
            """
        except KeyError:
            self.__debug=False

        try:
            self.__formatoFecha=kwargs['dateFormat']
            """The default date format to be used for any datettime elements on the attrs attribute.

            Remember to use valid Python datetime strftime formats.
            """
        except KeyError:
            self.__formatoFecha="%Y-%m-%dT%H:%M:%S+0000"

        try:
            self.__data=kwargs['data']
            """POST data to be sent to Mambu for POST requests."""
        except KeyError:
            self.__data=None

        try:
            self.__limit=kwargs['limit']
            """Limit the number of elements to be retrieved from Mambu on GET requests.

            Defaults to 0 which means (for the connect method) that you
            don't care how many elements Mambu has, you wish to retrieve
            them all.
            """
            kwargs.pop('limit')
        except KeyError:
            self.__limit=0

        try:
            self.__offset=kwargs['offset']
            """When retrieving several elements from Mambu on GET
            requests, offset for the first element to be retrieved.
            """
            kwargs.pop('offset')
        except KeyError:
            self.__offset=0

        self.__urlfunc = urlfunc
        """The given urlfunc argument is saved here.

        It's used at the connect() method, when called.
        """

        if self.__urlfunc == None: # Only used when GET returns an array, meaning the MambuStruct must be a list of MambuStucts
            return          # and each element is init without further configs. EDIT 2015-07-11: Really?

        try:
            if kwargs.pop('connect'):
                connect = True
            else:
                connect = False
        except KeyError:
            connect = True

        if connect:
            self.connect(*args, **kwargs)

    def connect(self, *args, **kwargs):
        """Connect to Mambu, make the request to the REST API.

        If there's no urlfunc to use, nothing is done here.

        When done, initializes the attrs attribute of the Mambu object
        by calling the init method. Please refer to that code and pydoc
        for further information.

        Uses urllib module to connect. Since all Mambu REST API
        responses are json, uses json module to translate the response
        to a valid python object (dictionary or list).

        When Mambu returns a response with returnCode and returnStatus
        fields, it means something went wrong with the request, and a
        MambuError is thrown detailing the error given by Mambu itself.

        If you need to make a POST request, send a data argument to the
        new Mambu object.

        Provides to prevent errors due to using special chars on the
        request URL. See mambuutil.iriToUri() method pydoc for further
        info.

        Provides to prevent errors due to using special chars on the
        parameters of a POST request. See mambuutil.encoded_dict()
        method pydoc for further info.

        For every request done, the request counter Singleton is
        increased.

        Includes retry logic, to provide for a max number of connection
        failures with Mambu. If maximum retries are reached,
        MambuCommError is thrown.

        Includes pagination code. Mambu supports a max of 500 elements
        per response. Such an ugly detail is wrapped here so further
        pagination logic is not needed above here. You need a million
        elements? you got them by making several 500 elements requests
        later joined together in a sigle list. Just send a limit=0
        (default) and that's it.

        TODO: improve raised exception messages. Sometimes MambuCommErrors
        are thrown due to reasons not always clear when catched down the
        road, but that perhaps may be noticed in here and aren't fully
        reported to the user. Specially serious on
        retries-MambuCommError situations (the except Exception that
        increases the retries counter is not saving the exception
        message, just retrying).
        """
        jsresp = {}

        if not self.__urlfunc:
            return

        # Pagination window, Mambu restricts at most 500 elements in response
        offset = self.__offset
        window = True
        jsresp = {}
        while window:
            if not self.__limit or self.__limit > OUT_OF_BOUNDS_PAGINATION_LIMIT_VALUE:
                limit = OUT_OF_BOUNDS_PAGINATION_LIMIT_VALUE
            else:
                limit = self.__limit

            # Retry mechanism, for awful connections
            retries = 0
            while retries < MambuStruct.RETRIES:
                try:
                    # POST
                    if self.__data:
                        resp = urlopen(iriToUri(self.__urlfunc(self.entid, *args, **kwargs)), urlencode(encoded_dict(self.__data)))
                    # GET
                    else:
                        resp = urlopen(iriToUri(self.__urlfunc(self.entid, limit=limit, offset=offset, *args, **kwargs)))
                    # Always count a new request when done!
                    self.rc.add(datetime.now())
                    try:
                        jsonresp = json.load(resp)
                        # Returns list: extend list for offset
                        if type(jsonresp) == list:
                            try:
                                jsresp.extend(jsonresp)
                            except AttributeError:
                                # First window, forget that jsresp was a dict, turn it in to a list
                                jsresp=jsonresp
                            if len(jsonresp) < limit:
                                window = False
                        # Returns dict: in theory Mambu REST API doesn't takes limit/offset in to account
                        else:
                            jsresp = jsonresp
                            window = False
                    except ValueError as ex:
                        raise ex
                    except Exception as ex:
                        raise MambuError("JSON Error: %s" % repr(ex))
                    break
                except MambuError as merr:
                    raise merr
                except Exception as ex:
                    retries += 1
            else:
                raise MambuCommError("ERROR I can't communicate with Mambu")

            offset = offset + limit
            if self.__limit:
                self.__limit -= limit
                if self.__limit <= 0:
                    window = False

        try:
            if jsresp.has_key(u'returnCode') and jsresp.has_key(u'returnStatus'):
                raise MambuError(jsresp[u'returnStatus'])
        except AttributeError:
            pass

        self.init(attrs=jsresp, *args, **kwargs)

    def preprocess(self):
        """Each MambuStruct implementation may massage the info on the
        Mambu response before conversion to an appropiate format/style
        adequate for its needs.

        Perfect example, custom fields on certain objects is a mess
        (IMHO) when retrieved from Mambu, so some easiness is
        implemented here to access them. See some of this objects
        modules and pydocs for further info.
        """
        pass

    def postprocess(self):
        """Each MambuStruct implementation may massage the info on the
        Mambu response after conversion to an appropiate format/style
        adequate for its needs.
        """
        pass

    def convertDict2Attrs(self, *args, **kwargs):
        """Each element on the atttrs attribute gest converted to a proper python object, depending on type.

        Some default constantFields are left as is (strings), because they are better treated as strings.
        """
        constantFields = ['id', 'groupName', 'name', 'homePhone', 'mobilePhone1', 'phoneNumber', 'postcode']
        def convierte(data):
            """Recursively convert the fields on the data given to a python object."""
            # Iterators, lists and dictionaries
            # Here comes the recursive calls!
            try:
                it = iter(data)
                if type(it) == type(iter({})):
                    d = {}
                    for k in it:
                        if k in constantFields:
                            d[k] = data[k]
                        else:
                            d[k] = convierte(data[k])
                    data = d
                if type(it) == type(iter([])):
                    l = []
                    for e in it:
                        l.append(convierte(e))
                    data = l
            except TypeError as terr:
                pass
            except Exception as ex:
                raise ex

            # Python built-in types: ints, floats, or even datetimes. If it
            # cannot convert it to a built-in type, leave it as string, or
            # as-is. There may be nested Mambu objects here!
            # This are the recursion base cases!
            try:
                d = int(data)
                if str(d) != data: # if string has trailing 0's, leave it as string, to not lose them
                    return data
                return d
            except (TypeError, ValueError) as tverr:
                try:
                    return float(data)
                except (TypeError, ValueError) as tverr:
                    try:
                        return self.util_dateFormat(data)
                    except (TypeError, ValueError) as tverr:
                        return data

            return data

        self.attrs = convierte(self.attrs)

    def util_dateFormat(self, field, formato=None):
        """Converts a datetime field to a datetime using some specified format.

        What this really means is that, if specified format includes
        only for instance just year and month, day and further info gets
        ignored and the objects get a datetime with year and month, and
        day 1, hour 0, minute 0, etc.

        A useful format may be %Y%m%d, then the datetime objects
        effectively translates into date objects alone, with no relevant
        time information.

        PLEASE BE AWARE, that this may lose useful information for your
        datetimes from Mambu. Read this for why this may be a BAD idea:
        https://julien.danjou.info/blog/2015/python-and-timezones
        """
        if not formato:
            try:
                formato = self.__formatoFecha
            except AttributeError:
                formato = "%Y-%m-%dT%H:%M:%S+0000"
        return datetime.strptime(datetime.strptime(field, "%Y-%m-%dT%H:%M:%S+0000").strftime(formato), formato)
