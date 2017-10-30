##############################################################################
#
# Copyright (C) Zenoss, Inc. 2009-2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import collections
import re

from ZenPacks.zenoss.Microsoft.Windows.modeler.WinRMPlugin import WinRMPlugin


Queue = collections.namedtuple('Queue', ['Name'])


class MSMQQueueMap(WinRMPlugin):
    """Modeler plugin to get list of Microsoft Message Queues."""

    relname = "microsoftmq"
    modname = "ZenPacks.zenoss.Microsoft.MSMQ.MSMQQueue"

    deviceProperties = WinRMPlugin.deviceProperties + (
        'zMSMQIgnoreQueues',
    )

    powershell_commands = {
        'MSMQQueue': 'Get-MsmqQueue | Select Path',
    }

    def process(self, device, results, log):
        log.info('Collecting MSMQ components for device %s', device.id)

        ignore = getattr(device, 'zMSMQIgnoreQueues', None)
        if ignore:
            ignore = re.compile(ignore).search

        output = results.get('MSMQQueue')
        if output and hasattr(output, 'stdout'):
            queue_names = [
                path.lower().replace('formatname:direct=os:', '')
                for path in output.stdout[2:]]
        else:
            queue_names = []

        rm = self.relMap()
        for q_name in queue_names:
            om = self.objectMap()

            # Skip queue names that match zMSMQIgnoreQueues.
            if ignore and ignore(q_name):
                continue

            om.id = self.prepId(q_name.replace('$', ''))
            om.queueName = q_name
            om.perfmonInstance = '\MSMQ Queue(%s)' % q_name
            rm.append(om)

        return rm
