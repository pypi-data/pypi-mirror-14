
def suite():
    #import unittest
    import doctest
    return doctest.DocFileSuite('event_detector.doctest.rst')
    #suite = unittest.TestSuite()
    #suite.addTests(doctest.DocFileSuite('event_detector.doctest.rst'))
    #return suite

def test():
    from unittest import TextTestRunner
    t = TextTestRunner()
    t.run(suite())
