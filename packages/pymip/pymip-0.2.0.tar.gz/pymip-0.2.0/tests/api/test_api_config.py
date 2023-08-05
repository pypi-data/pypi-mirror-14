# -*- coding: utf-8 -*-


def test_aligner(config):
    assert config.old.aligner == 'mosaik'
    assert config.new.aligner == 'bwa'


def test_log_path(config):
    ending = 'family/mip_log/2015-03-03/mip.pl_2015-03-03T13:12:12.log'
    assert config.old.log_path.endswith(ending)

    ending = 'family/mip_log/2016-03-07/mip.pl_2016-03-07T13:26:29.log'
    assert config.new.log_path.endswith(ending)


def test_mip_analysistype(config):
    assert config.old.mip_analysistype == 'exomes'
    assert config.new.mip_analysistype == 'exomes'


def test_family_id(config):
    assert config.old.family_id == 'family'
    assert config.new.family_id == 'family'


def test_instance_tags(config):
    assert config.old.instance_tags == ['CMMS']
    assert config.new.instance_tags == ['cust000']


def test_sample_ids(config):
    assert config.old.sample_ids == ['sample', 'sample2', 'sample3']
    assert config.new.sample_ids == ['sample']


def test_sampleinfo_path(config):
    ending = 'exomes/family/family_qc_sampleInfo.yaml'
    assert config.old.sampleinfo_path.endswith(ending)

    ending = 'exomes/family/family_qc_sampleInfo.yaml'
    assert config.new.sampleinfo_path.endswith(ending)


def test_is_wgs(config):
    assert config.old.is_wgs is False
    assert config.new.is_wgs is False


def test_references_dir(config):
    assert config.old.references_dir == '/vagrant/tests/fixtures/references'
    assert config.new.references_dir == ("/mnt/hds/proj/bioinfo/MIP_ANALYSIS/"
                                         "references_2.6")


def test_analysis_dir(config):
    assert config.old.analysis_dir.endswith('cust003/develop/analysis')
    assert config.new.analysis_dir.endswith('cust000/family/analysis')
