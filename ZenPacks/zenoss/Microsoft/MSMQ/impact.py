######################################################################
#
# Copyright (C) Zenoss, Inc. 2014, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is
# installed.
#
######################################################################


from zope.component import adapts
from zope.interface import implements

from Products.ZenRelations.ToManyRelationship import ToManyRelationshipBase
from Products.ZenRelations.ToOneRelationship import ToOneRelationship
from Products.ZenUtils.guid.interfaces import IGlobalIdentifier
from Products.Zuul.interfaces import ICatalogTool

from ZenPacks.zenoss.Impact.impactd import Trigger
from ZenPacks.zenoss.Impact.impactd.relations import ImpactEdge
from ZenPacks.zenoss.Impact.impactd.interfaces import IRelationshipDataProvider
from ZenPacks.zenoss.Impact.impactd.interfaces import INodeTriggers

AVAILABILITY = 'AVAILABILITY'
PERCENT = 'policyPercentageTrigger'
THRESHOLD = 'policyThresholdTrigger'
RP = 'ZenPacks.zenoss.Microsoft.MSMQ'


def guid(obj):
    return IGlobalIdentifier(obj).getGUID()


def edge(source, target):
    return ImpactEdge(source, target, RP)


def getRedundancyTriggers(guid, format, **kwargs):
    """Return a general redundancy set of triggers."""

    return (
        Trigger(guid, format % 'DOWN', PERCENT, AVAILABILITY, dict(
            kwargs, state='DOWN', dependentState='DOWN', threshold='100',
        )),
        Trigger(guid, format % 'DEGRADED', THRESHOLD, AVAILABILITY, dict(
            kwargs, state='DEGRADED', dependentState='DEGRADED', threshold='1',
        )),
        Trigger(guid, format % 'ATRISK_1', THRESHOLD, AVAILABILITY, dict(
            kwargs, state='ATRISK', dependentState='DOWN', threshold='1',
        )),
        Trigger(guid, format % 'ATRISK_2', THRESHOLD, AVAILABILITY, dict(
            kwargs, state='ATRISK', dependentState='ATRISK', threshold='1',
        )),
    )


def getPoolTriggers(guid, format, **kwargs):
    """Return a general pool set of triggers."""

    return (
        Trigger(guid, format % 'DOWN', PERCENT, AVAILABILITY, dict(
            kwargs, state='DOWN', dependentState='DOWN', threshold='100',
        )),
        Trigger(guid, format % 'DEGRADED', THRESHOLD, AVAILABILITY, dict(
            kwargs, state='DEGRADED', dependentState='DEGRADED', threshold='1',
        )),
        Trigger(guid, format % 'ATRISK_1', THRESHOLD, AVAILABILITY, dict(
            kwargs, state='DEGRADED', dependentState='DOWN', threshold='1',
        )),
    )

# ----------------------------------------------------------------------------
# Impact relationships

class MSMQQueueRelationsProvider(object):
    implements(IRelationshipDataProvider)

    relationship_provider = RP
    impact_relationships = None
    impacted_by_relationships = None

    def __init__(self, adapted):
        self._object = adapted

    def belongsInImpactGraph(self):
        return True

    def guid(self):
        if not hasattr(self, '_guid'):
            self._guid = guid(self._object)

        return self._guid

    def getEdges(self):
        yield edge(self.guid(), guid(self.device()))
