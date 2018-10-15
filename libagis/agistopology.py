#!/usr/bin/env python

from utils import load_json

from agiscloud import AGISCloud
from agissite import AGISSite 
from agisqueue import AGISQueue 
from agisce import AGISCE
from agisacopytool import AGISAcopytool
from agisaprotocol import AGISAprotocol
from agisastorage import AGISAstorage
from agisastorage0 import AGISAstorage0
from agiscloudrshare import AGISCloudrshare
from agiscopytool import AGISCopytool


# =============================================================================

class AGISTopology(object):

    def __init__(self, schedconfig):

        self.cloud_d = {}
        self.site_d = {}
        self.queue_d = {}
        self.ce_d = {}

        # build the topology 
        self.__build_topology_from_schedconfig(schedconfig)

    # -------------------------------------------------------------------------
    
    def _get_cloud(self, cloudname):
        if cloudname not in self.cloud_d.keys():
            self.cloud_d[cloudname] = self._getNextCloud(cloudname)
        return self.cloud_d[cloudname]

    def _getNextCloud(self, cloudname):
        """
        To implement inheritance, 
        override this method in the child class
        """
        return AGISCloud(cloudname)

    # -------------------------------------------------------------------------

    def _get_site(self, sitename):
        if sitename not in self.site_d.keys():
            self.site_d[sitename] = self._getNextSite(sitename)
        return self.site_d[sitename]

    def _getNextSite(self, sitename):
        """
        To implement inheritance, 
        override this method in the child class
        """
        return AGISSite(sitename)

    # -------------------------------------------------------------------------

    def _get_queue(self, qname):
        if qname not in self.queue_d.keys():
            self.queue_d[qname] = self._getNextQueue(qname)
        return self.queue_d[qname]

    def _getNextQueue(self, qname):
        """
        To implement inheritance, 
        override this method in the child class
        """
        return AGISQueue(qname)

    # -------------------------------------------------------------------------

    def _get_ce(self, ce_name):
        if ce_name not in self.ce_d.keys():
            self.ce_d[ce_name] = self._getNextCE(ce_name)
        return self.ce_d[ce_name]

    def _getNextCE(self, ce_name):
        """
        To implement inheritance, 
        override this method in the child class
        """
        return AGISCE(ce_name)


    # -------------------------------------------------------------------------

    def __build_topology_from_schedconfig(self, schedconfig):
        """
        builds the ATLAS topology from AGIS schedconfig
        """
        self.schedconfig_data = load_json(schedconfig)
               
        for qname, qdata in self.schedconfig_data.items():

            # get the cloud
            cloudname = qdata['cloud']
            cloud = self._get_cloud(cloudname)

            # get the site
            sitename = qdata['atlas_site']
            site = self._get_site(sitename)
            cloud.site_d[sitename] = site

            # get the queue
            queue = self._get_queue(qname)
            site.queue_d[qname] = queue

            # get the CEs 
            queue_l = qdata['queues']
            for q in queue_l:
                name = q['ce_name']
                ce = self._get_ce(name)
                queue.ce_d[name] = ce
                for k, v in q.items():
                    setattr(ce, k, v)
             
            # get acopytools
            for name, data in qdata['acopytools'].items():
                acopytool = AGISAcopytool(name, data)
                queue.acopytool_d[name] = acopytool

            # get astorages
            for name, data in qdata['astorages'].items():
                astorage = AGISAstorage(name, data)
                queue.astorage_d[name] = astorage

            # get astorages0
            for name, data in qdata['astorages0'].items():
                astorage0 = AGISAstorage0(name, data)
                queue.astorage0_d[name] = astorage0

            # get cloudrshares
            for name, data in qdata['cloudrshares'].items():
                cloudrshare = AGISCloudrshare(name, data)
                queue.cloudrshare_d[name] = cloudrshare

            # get copytools
            for name, data in qdata['copytools'].items():
                copytool = AGISCopytool(name, data)
                queue.copytool_d[name] = copytool

            # add the rest of attributes
            for k,v in qdata.items():
                if k not in ['acopytools', 'aprotocols', 'astorages', 'astorages0', 'cloudrshares', 'copytools', 'queues']:
                    setattr(queue, k, v)





if __name__ == '__main__':
    #topology = AGISTopology('http://atlas-agis-api.cern.ch/request/pandaqueue/query/list/?json&preset=schedconf.all')
    topology = AGISTopology('schedconfig.json')
    print topology.cloud_d['US'].site_d['AGLT2'].queue_d['AGLT2_LMEM_SL7-condor'].allowjem
    print topology.cloud_d['US'].site_d['AGLT2'].queue_d['AGLT2_LMEM_SL7-condor'].astorage_d['es_events'].value
    print topology.cloud_d['US'].site_d['AGLT2'].queue_d['AGLT2_LMEM_SL7-condor'].astorage0_d['es_events'].value
    print topology.cloud_d['US'].site_d['AGLT2'].queue_d['AGLT2_LMEM_SL7-condor'].cloudrshare_d['analysis'].value
    print topology.cloud_d['US'].site_d['AGLT2'].queue_d['AGLT2_LMEM_SL7-condor'].copytool_d['lsm'].value
    for ce in topology.cloud_d['US'].site_d['AGLT2'].queue_d['AGLT2_LMEM_SL7-condor'].ce_d.values():
        print ce.name, ce.ce_endpoint, ce.ce_status




