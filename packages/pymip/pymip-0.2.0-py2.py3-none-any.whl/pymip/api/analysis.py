# -*- coding: utf-8 -*-
from __future__ import division
from collections import namedtuple

from path import path
import yaml

from .archive import ArchiveMixin
from .config import ConfigMixin, OldConfigMixin
from .genelist import GenelistMixin
from .pedigree import PedigreeMixin
from .sampleinfo import OldSampleInfoMixin, SampleInfoMixin
from .scout import ScoutMixin

Configs = namedtuple('Configs', ['config', 'sampleinfo', 'pedigree'])


def load_analysis(family_dir, insanity=False):
    """Load the correct variant of the API."""
    configs = find_files(family_dir)
    with open(configs.sampleinfo, 'r') as stream:
        sampleinfo = yaml.load(stream)

    family_id = sampleinfo.keys()[0]
    family_data = sampleinfo[family_id][family_id]
    if 'MIPVersion' in family_data:
        return Analysis(family_dir, insanity=insanity)
    else:
        return OldAnalysis(family_dir, insanity=insanity)


def find_files(family_dir):
    """Guess the paths to the YAML files with configs."""
    family_dir = path(family_dir)
    family_id = family_dir.basename()

    config_file = "{}_config.yaml".format(family_id)
    config_path = family_dir.joinpath(config_file)
    assert config_path.exists(), "config not found: {}".format(config_path)

    ped_file = "{}_pedigree.txt".format(family_id)
    ped_path = family_dir.joinpath(ped_file)
    assert ped_path.exists(), "ped file not found: {}".format(config_path)

    sampleinfo_file = "{}_qc_sampleInfo.yaml".format(family_id)
    sampleinfo_path = family_dir.joinpath(sampleinfo_file)
    assert sampleinfo_path.exists(), ("sampleinfo file not found: {}"
                                      .format(sampleinfo_path))
    configs = Configs(config_path, sampleinfo_path, ped_path)
    return configs


class BaseAnalysis(ArchiveMixin, PedigreeMixin, GenelistMixin, ScoutMixin):

    """Interface to a MIP analysis.

    Args:
        family_dir (path): root level path to the top level family dir
    """

    def __init__(self, family_dir=None, insanity=False):
        super(BaseAnalysis, self).__init__()
        if family_dir:
            self.load(family_dir, insanity=insanity)

    def load(self, family_dir, insanity=False):
        """Initialize the loaders with the correct input files."""
        self.family_dir = path(family_dir)
        self.configs = find_files(self.family_dir)

        with self.configs.config.open('r') as stream:
            self.load_config(stream)

        with self.configs.pedigree.open('r') as stream:
            self.load_pedigree(stream)

        with self.configs.sampleinfo.open('r') as stream:
            self.load_sampleinfo(stream)

        if not insanity:
            self.sanity_check()

    def sanity_check(self):
        """Raise errors if something is not as expected.

        You need to run `load` before the checks will work.
        """
        if not hasattr(self, 'configs'):
            raise ValueError('load configs using `load` method')

        # check that analysis hasn't been moved without updating the configs
        config_sampleinfo = self.config['QCCollectSampleInfoFile']
        assert self.configs.sampleinfo == config_sampleinfo, (
            "sample info file mismatch: {} vs. {}".format(
                self.configs.sampleinfo, config_sampleinfo))

    def analysis_type(self):
        """Determine the analysis type."""
        ped_type = self.ped_analysistype
        if ped_type is None:
            # no sequencing type annotated, fall back to MIP config
            return 'wgs' if self.is_wgs else 'wes'
        else:
            return ped_type


class Analysis(BaseAnalysis, ConfigMixin, SampleInfoMixin):
    pass


class OldAnalysis(BaseAnalysis, OldConfigMixin, OldSampleInfoMixin):
    pass
