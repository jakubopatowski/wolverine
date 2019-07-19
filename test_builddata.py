import unittest
import builddata


class TestBuildData(unittest.TestCase):

    def setUp(self):
        self.bd = builddata.BuildData()

    def test_get_qt_target(self):
        self.assertEqual(self.bd.get_qt_target('Qt3Supportd.lib'),
                         'Qt4::Qt3Support')
        self.assertEqual(self.bd.get_qt_target(''), '')
        self.assertEqual(self.bd.get_qt_target('phonon'), 'phonon')
        self.assertEqual(self.bd.get_qt_target('phonond.lib'), 'Qt4::phonon')
        self.assertEqual(self.bd.get_qt_target('QtJopad.lib'), 'QtJopad.lib')
        self.assertEqual(self.bd.get_qt_target('QtCored.lib'), 'Qt4::QtCore')
        self.assertEqual(self.bd.get_qt_target('QtGuid.lib'), 'Qt4::QtGui')
        self.assertEqual(self.bd.get_qt_target('QtAssistantd.lib'),
                         'Qt4::QtAssistant')
        self.assertEqual(self.bd.get_qt_target('QtAssistantClientd.lib'),
                         'Qt4::QtAssistantClient')
        self.assertEqual(self.bd.get_qt_target('QAxContainerd.lib'),
                         'Qt4::QAxContainer')
        self.assertEqual(self.bd.get_qt_target('QtAxContainerd.lib'),
                         'QtAxContainerd.lib')
        self.assertEqual(self.bd.get_qt_target('QAxServerd.lib'),
                         'Qt4::QAxServer')
        self.assertEqual(self.bd.get_qt_target('QtAxServerd.lib'),
                         'QtAxServerd.lib')
        self.assertEqual(self.bd.get_qt_target('QtDBusd.lib'), 'Qt4::QtDBus')


if __name__ == '__main__':
    unittest.main()
