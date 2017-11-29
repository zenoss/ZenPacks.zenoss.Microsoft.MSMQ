##############################################################################
#
# Copyright (C) Zenoss, Inc. 2009-2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import re

from ZenPacks.zenoss.Microsoft.Windows.modeler.WinRMPlugin import WinRMPlugin


class MSMQQueueMap(WinRMPlugin):
    """Modeler plugin to get list of Microsoft Message Queues."""

    relname = "microsoftmq"
    modname = "ZenPacks.zenoss.Microsoft.MSMQ.MSMQQueue"

    deviceProperties = WinRMPlugin.deviceProperties + (
        'zMSMQIgnoreQueues',
    )

    powershell_commands = {
        'PrivateAndPublic': 'Get-MsmqQueue -QueueType PrivateAndPublic | Select Path',
        'SystemDeadLetter': 'Get-MsmqQueue -QueueType SystemDeadLetter | Select Path',
        'SystemJournal': 'Get-MsmqQueue -QueueType SystemJournal | Select Path',
        'SystemTransactionalDeadLetter': 'Get-MsmqQueue -QueueType SystemTransactionalDeadLetter | Select Path',
        'Additional': 'Get-WmiObject Win32_PerfFormattedData_msmq_MSMQQueue | Select Name',
    }

    def _get_queue_names(self, results):
        q_names = []
        for q_output in results.itervalues():
            if q_output and hasattr(q_output, 'stdout'):
                for raw_q_name in q_output.stdout[2:]:
                    q_name = raw_q_name.lower().replace(
                        'formatname:direct=os:', '').strip('._')
                    if q_name not in q_names:
                        q_names.append(q_name)
        return q_names

    def process(self, device, results, log):
        log.info('Collecting MSMQ components for device %s', device.id)

        ignore = getattr(device, 'zMSMQIgnoreQueues', None)
        if ignore:
            ignore = re.compile(ignore).search

        rm = self.relMap()
        for q_name in self._get_queue_names(results):
            om = self.objectMap()

            # Skip queue names that match zMSMQIgnoreQueues.
            if ignore and ignore(q_name):
                continue

            om.id = self.prepId(q_name.replace('$', ''))
            om.queueName = q_name
            om.perfmonInstance = '\MSMQ Queue(%s)' % q_name
            rm.append(om)

        return rm
