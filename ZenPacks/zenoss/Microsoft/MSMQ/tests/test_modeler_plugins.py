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

        results = {
            'Additional': Mock(
                exit_code=0,
                stderr=[],
                stdout=[
                    u'Name',
                    u'----',
                    u'win-tl4mu7a971n\\public_queue_1',
                    u'win-tl4mu7a971n\\private$\\private_queue_1',
                    u'win-tl4mu7a971n\\private$\\notify_queue$',
                    u'win-tl4mu7a971n\\private$\\order_queue$',
                    u'win-tl4mu7a971n\\private$\\admin_queue$',
                    u'Computer Queues']),
            'SystemJournal': Mock(
                exit_code=0,
                stderr=[],
                stdout=[
                    u'Path',
                    u'----',
                    u'FormatName:DIRECT=OS:.\\SYSTEM$;JOURNAL']),
            'SystemTransactionalDeadLetter': Mock(
                exit_code=0,
                stderr=[],
                stdout=[
                    u'Path',
                    u'----',
                    u'FormatName:DIRECT=OS:.\\SYSTEM$;DEADXACT']),
            'SystemDeadLetter': Mock(
                exit_code=0,
                stderr=[],
                stdout=[
                    u'Path',
                    u'----',
                    u'FormatName:DIRECT=OS:.\\SYSTEM$;DEADLETTER']),
            'PrivateAndPublic': Mock(
                exit_code=0,
                stderr=[],
                stdout=[
                    u'Path',
                    u'----',
                    u'FormatName:DIRECT=OS:win-tl4mu7a971n\\private$\\private_queue_1',
                    u'WIN-TL4MU7A971N\\public_queue_1'])}

        res = queue_plugin.process(device, results, Mock())

        self.assertEquals(len(res.maps), 9)
        self.assertEquals(res.maps[0].id, 'system_deadletter')
        self.assertEquals(res.maps[2].id, 'win-tl4mu7a971n_private_private_queue_1')
        self.assertEquals(res.maps[4].id, 'win-tl4mu7a971n_private_notify_queue')
        self.assertEquals(res.maps[6].id, 'win-tl4mu7a971n_private_admin_queue')
        self.assertEquals(res.maps[8].id, 'system_deadxact')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMSMQQueueMap))
    return suite
