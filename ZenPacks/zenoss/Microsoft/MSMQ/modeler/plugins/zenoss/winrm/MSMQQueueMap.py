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

    queries = {
        'MSMQQueue': 'Select Name From Win32_PerfFormattedData_MSMQ_MSMQQueue',
    }

    powershell_commands = {
        'AdditionalQueues': 'Get-MsmqQueue | Select Path',
    }

    def _convertAdditionalQueues(self, additionalQueues):
        """Convert additional queues according to MSMQQueue output format."""
        return [
            Queue(Name=path.lower().replace('formatname:direct=os:', ''))
            for path in additionalQueues.stdout[2:]]

    def process(self, device, results, log):
        log.info('Collecting MSMQ queues for device %s', device.id)

        ignore = getattr(device, 'zMSMQIgnoreQueues', None)
        if ignore:
            ignore = re.compile(ignore).search

        if 'MSMQQueue' not in results:
            results['MSMQQueue'] = []

        additionalQueues = results.get('AdditionalQueues')
        if additionalQueues:
            results['MSMQQueue'].extend(
                self._convertAdditionalQueues(additionalQueues))

        rm = self.relMap()
        queues_names = set()
        for queue in results['MSMQQueue']:
            if not getattr(queue, 'Name', None):
                continue

            # Don't add duplicates to the model.
            if queue.Name in queues_names:
                continue
            else:
                queues_names.add(queue.Name)

            om = self.objectMap()

            # Skip queue names that match zMSMQIgnoreQueues.
            if ignore and ignore(queue.Name):
                continue

            om.id = self.prepId(queue.Name.replace('$', ''))
            om.queueName = queue.Name
            om.perfmonInstance = '\MSMQ Queue(%s)' % queue.Name
            rm.append(om)

        return rm
