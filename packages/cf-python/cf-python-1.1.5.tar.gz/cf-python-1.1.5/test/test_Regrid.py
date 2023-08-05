# -*- coding: utf-8 -*-

import os
import numpy
import cf
import unittest
import inspect

class RegridTest(unittest.TestCase):
    filename1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'file1.nc')
    filename2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'file2.nc')
    filename3 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'file3.nc')
    filename4 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'file4.nc')
    filename5 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'test_file3.nc')
    filename6 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'test_file2.nc')
    
    chunk_sizes = (300, 10000, 100000)[::-1]
    original_chunksize = cf.CHUNKSIZE()
    
    test_only = ()
#    test_only = ('NOTHING!!!!!')
#    test_only = ('test_Field_regrids',)
#    test_only('test_Field_section',)
#    test_only('test_Data_section',)

    def test_Field_regrids(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return
        
        original_atol = cf.ATOL(1e-12)

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)
            f1 = cf.read(self.filename1)
            f2 = cf.read(self.filename2)
            f3 = cf.read(self.filename3)
            self.assertTrue(f3.equals(f1.regrids(f2), traceback=True),
                            'destination = global Field, CHUNKSIZE = %s' % chunksize)
            dst = {'longitude': f2.dim('X'), 'latitude': f2.dim('Y')}
            self.assertTrue(f3.equals(f1.regrids(dst, dst_cyclic=True),
                                      traceback=True),
                            'destination = global dict, CHUNKSIZE = %s' % chunksize)
            f4 = cf.read(self.filename4)
            f5 = cf.read(self.filename5)
            self.assertTrue(f4.equals(f1.regrids(f5, method='bilinear'), traceback=True),
                            'destination = regional Field, CHUNKSIZE = %s' % chunksize)
        #--- End: for
        cf.CHUNKSIZE(self.original_chunksize)

        cf.ATOL(original_atol)
    #--- End: def
    
    def test_Field_section(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)
            f = cf.read(self.filename6)
            self.assertTrue(len(f.section(('X','Y'))) == 1800,
                            'CHUNKSIZE = %s' % chunksize)
        #--- End: for
        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def
    
    def test_Data_section(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        for chunksize in self.chunk_sizes:
            cf.CHUNKSIZE(chunksize)
            f = cf.read(self.filename6)
            self.assertTrue(list(sorted(f.Data.section((1,2)).keys()))
                            == [(x, None, None) for x in range(1800)])
        #--- End: for
        cf.CHUNKSIZE(self.original_chunksize)
    #--- End: def
    
#--- End: class

if __name__ == "__main__":
    print 'cf-python version:'     , cf.__version__
    print 'cf-python path:'        , os.path.abspath(cf.__file__)
    print ''
    unittest.main(verbosity=2)
