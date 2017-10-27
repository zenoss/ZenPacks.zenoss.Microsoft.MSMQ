##############################################################################
#
# Copyright (C) Zenoss, Inc. 2014-2017, all rights reserved.
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
        queue_plugin = MSMQQueueMap()

        device = Mock()
        device.zMSMQIgnoreQueues = False

        public_queue_1 = Mock(
            Name='win-tl4mu7a971n\\public_queue_1')

        private_queue_1 = Mock(
            Name='win-tl4mu7a971n\\private$\\private_queue_1')

        results = {'MSMQQueue': [public_queue_1, private_queue_1]}

        res = queue_plugin.process(device, results, Mock())

        self.assertEquals(len(res.maps), 2)
        self.assertEquals(
            res.maps[0].id, 'win-tl4mu7a971n_public_queue_1')
        self.assertEquals(
            res.maps[1].id, 'win-tl4mu7a971n_private_private_queue_1')

        results['AdditionalQueues'] = Mock(
            exit_code=0,
            stderr=[],
            stdout=[
                'QueueName',
                '---------',
                'FormatName:DIRECT=OS:win-tl4mu7a971n\\private$\\private_queue_1',
                'WIN-TL4MU7A971N\\public_queue_1',
                'WIN-TL4MU7A971N\\public_queue_2'])

        res = queue_plugin.process(device, results, Mock())

        self.assertEquals(len(res.maps), 3)
        self.assertEquals(res.maps[0].id, 'win-tl4mu7a971n_public_queue_1')
        self.assertEquals(res.maps[1].id, 'win-tl4mu7a971n_private_private_queue_1')
        self.assertEquals(res.maps[2].id, 'win-tl4mu7a971n_public_queue_2')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMSMQQueueMap))
    return suite
