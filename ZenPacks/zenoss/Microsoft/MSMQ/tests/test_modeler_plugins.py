##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from mock import Mock

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ..modeler.plugins.zenoss.winrm.MSMQQueueMap import MSMQQueueMap


class TestMSMQQueueMap(BaseTestCase):
    def test_return_results(self):
        map = MSMQQueueMap()

        device = Mock()
        device.zMSMQIgnoreQueues = False

        a = Mock()
        b = Mock()
        a.Name = 'a'
        b.Name = 'b'
        results = {'MSMQQueue': [a, b]}
        res = map.process(device, results, Mock())
        self.assertEquals(len(res.maps), 2)
        self.assertEquals(res.maps[0].id, a.Name)
        self.assertEquals(res.maps[1].id, b.Name)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMSMQQueueMap))
    return suite
