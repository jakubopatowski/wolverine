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
        self.assertEqual(self.bd.get_qt_target('QtDesignerd.lib'),
                         'Qt4::QtDesigner')
        self.assertEqual(self.bd.get_qt_target('QtDesignerComponentsd.lib'),
                         'Qt4::QtDesignerComponents')
        self.assertEqual(self.bd.get_qt_target('QtHelpd.lib'), 'Qt4::QtHelp')
        self.assertEqual(self.bd.get_qt_target('QtMotifd.lib'), 'Qt4::QtMotif')
        self.assertEqual(self.bd.get_qt_target('QtMultimediad.lib'),
                         'Qt4::QtMultimedia')
        self.assertEqual(self.bd.get_qt_target('QtNetworkd.lib'),
                         'Qt4::QtNetwork')
        self.assertEqual(self.bd.get_qt_target('QtNsPlugind.lib'),
                         'Qt4::QtNsPlugin')
        self.assertEqual(self.bd.get_qt_target('QtOpenGLd.lib'),
                         'Qt4::QtOpenGL')
        self.assertEqual(self.bd.get_qt_target('QtScriptd.lib'),
                         'Qt4::QtScript')
        self.assertEqual(self.bd.get_qt_target('QtScriptToolsd.lib'),
                         'Qt4::QtScriptTools')
        self.assertEqual(self.bd.get_qt_target('QtSqld.lib'), 'Qt4::QtSql')
        self.assertEqual(self.bd.get_qt_target('QtSvgd.lib'), 'Qt4::QtSvg')
        self.assertEqual(self.bd.get_qt_target('QtTestd.lib'), 'Qt4::QtTest')
        self.assertEqual(self.bd.get_qt_target('QtUiToolsd.lib'),
                         'Qt4::QtUiTools')
        self.assertEqual(self.bd.get_qt_target('QtWebKitd.lib'),
                         'Qt4::QtWebKit')
        self.assertEqual(self.bd.get_qt_target('QtXmld.lib'), 'Qt4::QtXml')
        self.assertEqual(self.bd.get_qt_target('QtXmlPatternsd.lib'),
                         'Qt4::QtXmlPatterns')


if __name__ == '__main__':
    unittest.main()
