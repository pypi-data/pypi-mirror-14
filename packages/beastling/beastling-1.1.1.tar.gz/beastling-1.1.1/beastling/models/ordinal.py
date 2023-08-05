import codecs
import os
import xml.etree.ElementTree as ET

from .basemodel import BaseModel
from ..unicodecsv import UnicodeDictReader

class OrdinalModel(BaseModel):

    def __init__(self, model_config, global_config):

        BaseModel.__init__(self, model_config, global_config)

    def add_sitemodel(self, distribution, feature, fname):

            # Sitemodel
            if self.rate_variation:
                mr = "@featureClockRate:%s" % fname
            else:
                mr = "1.0"
            sitemodel = ET.SubElement(distribution, "siteModel", {"id":"geoSiteModel.%s"%fname,"spec":"SiteModel", "mutationRate":mr,"shape":"1","proportionInvariant":"0"})

            substmodel = ET.SubElement(sitemodel, "substModel",{"id":"ordinal.s:%s"%fname,"spec":"Ordinal","stateNumber":"%d" % self.valuecounts[feature]})

            # Empirical frequencies
            if self.frequencies == "empirical":
                if self.pruned:
                    freq = ET.SubElement(substmodel,"frequencies",{"id":"featurefreqs.s:%s"%fname,"spec":"Frequencies", "data":"@%s.filt"%fname})
                else:
                    freq = ET.SubElement(substmodel,"frequencies",{"id":"featurefreqs.s:%s"%fname,"spec":"Frequencies", "data":"@%s"%fname})
