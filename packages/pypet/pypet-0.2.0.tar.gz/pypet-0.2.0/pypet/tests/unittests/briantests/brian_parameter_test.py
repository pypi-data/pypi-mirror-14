__author__ = 'Robert Meyer'

import sys

import numpy as np
if (sys.version_info < (2, 7, 0)):
    import unittest2 as unittest
else:
    import unittest

try:
    import brian
    from pypet.brian.parameter import BrianParameter, BrianResult
    from brian.stdunits import mV, mA, kHz,ms
except ImportError as exc:
    #print('Import Error: %s' % str(exc))
    brian = None

from pypet.tests.unittests.parameter_test import ParameterTest, ResultTest
from pypet.utils.explore import cartesian_product
from pypet.tests.testutils.ioutils import parse_args, run_suite


@unittest.skipIf(brian is None, 'Can only be run with brian!')
class BrianParameterTest(ParameterTest):

    tags = 'unittest', 'brian', 'parameter'

    def setUp(self):

        if not hasattr(self,'data'):
            self.data = {}

        self.data['mV1'] = 1*mV
        self.data['ampere1'] = 1*mA
        self.data['msecond17'] = 16*ms
        self.data['kHz05'] = 0.5*kHz

        super(BrianParameterTest,self).setUp()

        self.dynamic_imports = [BrianParameter, BrianResult]


    def make_params(self):
        self.param = {}
        for key, val in self.data.items():
            self.param[key] = BrianParameter(self.location+'.'+key, val, comment=key)



    def explore(self):
        self.explore_dict=cartesian_product({'npstr':[np.array(['Uno', 'Dos', 'Tres']),
                               np.array(['Cinco', 'Seis', 'Siette']),
                            np.array(['Ocho', 'Nueve', 'Diez'])],
                           'val0':[1,2,3],
                           'mV1' : [42.0*mV,3*mV,4*mV]})




        ## Explore the parameter:
        for key, vallist in self.explore_dict.items():
            self.param[key]._explore(vallist)
            self.assertTrue(self.param[key].v_explored and self.param[key].f_has_range())


@unittest.skipIf(brian is None, 'Can only be run with brian!')
class BrianParameterStringModeTest(BrianParameterTest):

    tags = 'unittest', 'brian', 'parameter', 'string_mode'

    def make_params(self):
        self.param = {}
        for key, val in self.data.items():
            self.param[key] = BrianParameter(self.location+'.'+key, val, comment=key)
            self.param[key].v_storage_mode = BrianParameter.STRING_MODE


@unittest.skipIf(brian is None, 'Can only be run with brian!')
class BrianResultTest(ResultTest):

    tags = 'unittest', 'brian', 'result'

    def make_constructor(self):
        self.Constructor=BrianResult
        self.dynamic_imports=[BrianResult]

    def test_illegal_naming(self):
        for res in self.results.values():
            data_dict = {'val'+BrianResult.IDENTIFIER:42}
            with self.assertRaises(AttributeError):
                res.f_set(**data_dict)


    def setUp(self):

        if not hasattr(self,'data'):
            self.data = {}

        self.data['mV1'] = 1*mV
        self.data['ampere1'] = 1*mA
        self.data['msecond17'] = 16*ms
        self.data['kHz05'] = 0.5*kHz

        super(BrianResultTest, self).setUp()


@unittest.skipIf(brian is None, 'Can only be run with brian!')
class BrianResultStringModeTest(BrianResultTest):

    tags = 'unittest', 'brian', 'result', 'string_mode'

    def setUp(self):
        super(BrianResultStringModeTest, self).setUp()

        for res in self.results.values():
            res.v_storage_mode=BrianResult.STRING_MODE

if __name__ == '__main__':
    opt_args = parse_args()
    run_suite(**opt_args)

