import codecs
import os
import xml.etree.ElementTree as ET

from .basemodel import BaseModel
from ..unicodecsv import UnicodeDictReader

class NestedOrdinalModel(BaseModel):

    def __init__(self, model_config, global_config):

        BaseModel.__init__(self, model_config, global_config)

    def add_state(self, state):
        BaseModel.add_state(self, state)
        for f in self.features:
            fname = "%s:%s" % (self.name, f)
            alpha = ET.SubElement(state, "parameter", {"id":"nested_alpha.s:%s" % fname, "lower":"1.0E-4", "name":"stateNode", "upper":"1.0"})
            alpha.text="0.5"

    def add_sitemodel(self, distribution, feature, fname):

            # Sitemodel
            if self.rate_variation:
                mr = "@featureClockRate:%s" % fname
            else:
                mr = "1.0"
            sitemodel = ET.SubElement(distribution, "siteModel", {"id":"geoSiteModel.%s"%fname,"spec":"SiteModel", "mutationRate":mr,"shape":"1","proportionInvariant":"0"})

            substmodel = ET.SubElement(sitemodel, "substModel",{"id":"nestedordinal.s:%s"%fname,"spec":"NestedOrdinal","alpha":"@nested_alpha.s:%s"%fname, "stateNumber":"%d" % self.valuecounts[feature]})
            if self.frequencies == "empirical":
                if self.pruned:
                    freq = ET.SubElement(substmodel,"frequencies",{"id":"featurefreqs.s:%s"%fname,"spec":"Frequencies", "data":"@%s.filt"%fname})
                else:
                    freq = ET.SubElement(substmodel,"frequencies",{"id":"featurefreqs.s:%s"%fname,"spec":"Frequencies", "data":"@%s"%fname})

    def add_operators(self, run):
        BaseModel.add_operators(self, run)
        for f in self.features:
            fname = "%s:%s" % (self.name, f)
            ET.SubElement(run, "operator", {"id":"nested_alpha_scaler.s:%s" % fname, "spec":"ScaleOperator","parameter":"@nested_alpha.s:%s" % fname,"scaleFactor":"0.5","weight":"1.0"})

    def add_param_logs(self, logger):
        BaseModel.add_param_logs(self, logger)
        for f in self.features:
            fname = "%s:%s" % (self.name, f)
            ET.SubElement(logger,"log",{"idref":"nested_alpha.s:%s" % fname})
