# coding: utf-8

import mock
import unittest
from datetime import datetime

import mambustruct

class MambuStructTests(unittest.TestCase):
    def setUp(self):
        c = mambustruct.RequestsCounter()
        c.reset()
        self.func = lambda x:'http://example.com'+x

    def test_requestscountrer(self):
        c = mambustruct.RequestsCounter()
        self.assertEqual(c.cnt, 0)
        c.add(datetime.now())
        self.assertEqual(c.cnt,1)
        self.assertEqual(len(c.requests),1)
        c.reset()
        self.assertEqual(c.cnt,0)
        self.assertEqual(len(c.requests),0)
        c2 = mambustruct.RequestsCounter()
        self.assertEqual(c,c2)

    def test_init_(self):
        # Normal init
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False)
        self.assertEqual(s.entid, '1234')
        self.assertEqual(s.rc.cnt, 0)
        
        # Test that urlfunc=None sets no attributes
        s = mambustruct.MambuStruct(entid='1234', urlfunc=None)
        self.assertDictEqual(s.__dict__, {})

    @mock.patch('mambustruct.json')
    @mock.patch('mambustruct.urlencode')
    @mock.patch('mambustruct.urlopen')
    def test_connect(self, urlopen, urlencode, json):
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False)
        json.load.return_value = {}
        s.connect()

        # urlopen is called to open the URL given by func
        urlopen.assert_called_with(self.func('1234'))
        self.assertEqual(s.rc.cnt, 1)

        # simulate Mambu returns an error
        json.load.return_value = {'returnCode'  :'TestErrorCode',
                                  'returnStatus':'Test Error Status',}
        with self.assertRaisesRegexp(mambustruct.MambuError, "^Test Error Status$") as ex:
            s.connect()
        self.assertEqual(s.rc.cnt, 2)

        json.load.return_value = {}
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func)
        self.assertEqual(s.rc.cnt, 3)

        # POST to Mambu
        data={'test_data_1': 12345.67, 'test_data_2': "hello world"}
        urlencode.return_value="test_data_1=12345.67&test_data_2=hello+world"
        json.load.return_value = {}
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False, data=data)
        s.connect()
        urlencode.assert_called_with(data)
        urlopen.assert_called_with(self.func('1234'), 'test_data_1=12345.67&test_data_2=hello+world')

        # MambuCommError
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False)
        urlopen.side_effect = [Exception("")]
        with self.assertRaisesRegexp(mambustruct.MambuCommError, "^ERROR I can't communicate with Mambu$") as ex:
            s.connect()
        # Treat json ValueError as MambuCommError
        urlopen.side_effect = [""]
        json.load.side_effect = [ValueError("")]
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False)
        with self.assertRaisesRegexp(mambustruct.MambuCommError, "^ERROR I can't communicate with Mambu$") as ex:
            s.connect()
        # Other json errors raise MambuError
        urlopen.side_effect = [""]
        json.load.side_effect = [Exception("hello world")]
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False)
        with self.assertRaisesRegexp(mambustruct.MambuError, "^JSON Error: Exception\('hello world',\)$") as ex:
            s.connect()
        
    @mock.patch('mambustruct.json')
    @mock.patch('mambustruct.urlopen')
    def test_init(self, urlopen, json):
        test_data = {'attr01'       : "1", # integer
                     'attr02'       : "3.141592", # floating point
                     'attr03'       : "string", # string
                     'attr04'       : "001234", # integer defaults to string to preserve leading 0's
                     'attr05'       : "1979-10-23T10:36:00+0000", # datetime in default format
                     'attr06'       : "2014-10-23", # datetime in wrong format defaults to string

                     # iterables
                     'attr07'       : ["2","2.718282","cadena","001","1981-06-08T12:00:00+0000","1981-06-08"],
                     'attr08'       : {'subattr1' : "3",
                                       'subattr2' : "1.414214",
                                       'subattr3' : "chaîne",
                                       'subattr4' : "002",
                                       'subattr5' : "2010-05-03T21:00:00+0000",
                                       'subattr6' : "2010-05-03",
                                      },
                     'attr09'       : [{'subattr1': "1",'subattr2': "1.618034"},["2","0.841471"]],
                     'attr10'       : {'subattr1': {'subsubattr1': "1",'subsubattr2': "1.618034"},
                                       'subattr2': ["2","0.841471"],
                                      },

                     # Numbers which MUST remain as strings
                     'id'           : "1",
                     'homePhone'    : "123456789",
                     'mobilePhone1' : "987654321",
                     'phoneNumber'  : "001234567",
                     'postcode'     : "54321",
                    }

        urlopen.return_value = ""
        json.load.return_value = test_data
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=True)
        self.assertIsInstance(s.attrs, dict)

        self.assertIsInstance(repr(s),str)
        self.assertIsInstance(str(s),str)

        # Dict-like behaviour
        self.assertEqual(len(s), len(test_data))
        self.assertEqual(s['attr01'],1)
        s['attr03'] = "hello world!"
        self.assertEqual(s.attrs['attr03'], "hello world!")
        self.assertTrue(s.has_key('attr02'))
        self.assertListEqual(sorted(s.items()), [('attr01',1),
                                                 ('attr02',3.141592),
                                                 ('attr03',"hello world!"),
                                                 ('attr04',"001234"),
                                                 ('attr05',datetime(1979, 10, 23, 10, 36)),
                                                 ('attr06',"2014-10-23"),

                                                 ('attr07',[2, 2.718282, "cadena", "001", datetime(1981,6,8,12), "1981-06-08"]),
                                                 ('attr08',{'subattr1':3,
                                                            'subattr2':1.414214,
                                                            'subattr3':"chaîne",
                                                            'subattr4':"002",
                                                            'subattr5':datetime(2010,5,3,21),
                                                            'subattr6':"2010-05-03",
                                                           }),
                                                 ('attr09',[{'subattr1':1,'subattr2':1.618034},[2,0.841471]]),
                                                 ('attr10',{'subattr1':{'subsubattr1':1,'subsubattr2':1.618034},
                                                            'subattr2':[2,0.841471]
                                                           }),

                                                 ('homePhone',"123456789"),
                                                 ('id',"1"),
                                                 ('mobilePhone1',"987654321"),
                                                 ('phoneNumber',"001234567"),
                                                 ('postcode',"54321"),
                                                ])

        self.assertIsInstance(s['attr01'], int)
        self.assertIsInstance(s['attr02'], float)
        self.assertIsInstance(s['attr03'], str)
        self.assertIsInstance(s['attr04'], str)
        self.assertIsInstance(s['attr05'], datetime)
        self.assertIsInstance(s['attr06'], str)

        self.assertIsInstance(s['id'], str)
        self.assertIsInstance(s['homePhone'], str)
        self.assertIsInstance(s['mobilePhone1'], str)
        self.assertIsInstance(s['phoneNumber'], str)
        self.assertIsInstance(s['postcode'], str)

        # Calling pre and post process methods
        s.preprocess = mock.Mock()
        s.postprocess = mock.Mock()
        s.init(attrs=s.attrs)
        s.preprocess.assert_called_with()
        s.postprocess.assert_called_with()

        # __eq__
        json.load.side_effect = [{'encodedKey': "12345",},
                                 {'encodedKey': "12345",},
                                 {'encodedKey': "54321",},
                                 {},
                                ]
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func)
        s2 = mambustruct.MambuStruct(entid='1234', urlfunc=self.func)
        s3 = mambustruct.MambuStruct(entid='1234', urlfunc=self.func)
        s4 = mambustruct.MambuStruct(entid='1234', urlfunc=self.func)
        s5 = mambustruct.MambuStruct(entid='1234', urlfunc=None)

        self.assertTrue(s==s2)
        self.assertFalse(s==s3)
        self.assertFalse(s==s4)
        self.assertFalse(s==s5) # Not Implemented

    def test_util_dateFormat(self):
        s = mambustruct.MambuStruct(entid='1234', urlfunc=self.func, connect=False)
        self.assertEqual(s.util_dateFormat("1979-10-23T10:36:00+0000"), datetime(1979,10,23,10,36))
        self.assertEqual(s.util_dateFormat("1979-10-23T10:36:00+0000",formato="%Y%m%d"), datetime(1979,10,23))
        self.assertEqual(s.util_dateFormat("1979-10-23T10:36:00+0000",formato="%Y%m"), datetime(1979,10,1))
        self.assertEqual(s.util_dateFormat("1979-10-23T10:36:00+0000",formato="%Y"), datetime(1979,1,1))

    def test_iterator(self):
        array = range(10)
        class iterator():
            def __iter__(self):
                return mambustruct.MambuStructIterator(array)
        it = iterator()
        for n,e in enumerate(it):
            self.assertEqual(n,e)

        class iterator(mambustruct.MambuStruct):
            def __init__(self, urlfunc, entid):
                super(iterator,self).__init__(urlfunc, entid)
                self.attrs = []
                for e in array:
                    m = mambustruct.MambuStruct(urlfunc,entid)
                    m.attrs = [e]
                    self.attrs.append(m)
            def __iter__(self):
                return mambustruct.MambuStructIterator(self.attrs)
        ms_array = iterator(urlfunc=None, entid='')
        for n,e in enumerate(ms_array):
            self.assertIsInstance(repr(e),str)
            self.assertEqual([n],e.attrs)


if __name__ == '__main__':
    test_classes_to_run = [
                           MambuStructTests,
                          ]
    tl = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        print "%s testcases:" % test_class.__name__
        suite = tl.loadTestsFromTestCase(test_class)
        testcases = tl.getTestCaseNames(test_class)
        for t in testcases:
            print " ", t
        print ""
        suites_list.append(suite)
    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(big_suite)
