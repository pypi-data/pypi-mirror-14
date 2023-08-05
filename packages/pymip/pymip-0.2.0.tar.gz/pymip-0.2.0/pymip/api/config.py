# -*- coding: utf-8 -*-
from path import path
import yaml


class BaseConfig(object):

    def load_config(self, stream):
        """Load the MIP config as YAML file."""
        self.config = yaml.load(stream)

    @property
    def sampleinfo_path(self):
        """Return the path to the sample info file."""
        return self.config['sampleInfoFile']

    @property
    def log_path(self):
        """Return the MIP log file path for the analysis."""
        return self.config['logFile']

    @property
    def mip_analysistype(self):
        """Return the crude analysis type indicator.

        Doesn't take into acocunt mixed analyses.
        """
        return self.config['analysisType']

    @property
    def instance_tags(self):
        """Return the list of instance tags."""
        return self.config['instanceTag']

    @property
    def family_id(self):
        """Return the family id for the analysis."""
        return self.config['familyID']

    @property
    def sample_ids(self):
        """Return the list of sample ids in the analysis."""
        return self.config['sampleIDs']

    @property
    def is_wgs(self):
        """Check if the analysis is whole genome."""
        # infer this from the absolute path to the sample info file
        return False if self.mip_analysistype == 'exomes' else True

    @property
    def references_dir(self):
        return self.config['referencesDir']

    @property
    def analysis_dir(self):
        """Return path to base analysis dir."""
        cc_path = path(self.config['clusterConstantPath'])
        return cc_path.joinpath(self.config['analysisConstantPath'])

    @property
    def aligner(self):
        """Return the aligner used for the analysis."""
        return (self.config['aligner'] if 'aligner' in self.config else
                self.config['alignerOutDir'])


class OldConfigMixin(BaseConfig):
    pass


class ConfigMixin(BaseConfig):
    pass
