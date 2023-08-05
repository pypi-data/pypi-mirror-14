# -*- coding: utf-8 -*-
import pytest

from pymip.api.analysis import find_files
from pymip.api import Analysis


def test_find_files():
    family_dir = 'tests/fixtures/mip/configs/started/family'
    configs = find_files(family_dir)
    assert configs.config.endswith('family/family_config.yaml')
    assert configs.sampleinfo.endswith('family/family_qc_sampleInfo.yaml')
    assert configs.pedigree.endswith('family/family_pedigree.txt')


def test_find_files_not_started():
    family_dir = 'tests/fixtures/mip/configs/not-started/family'
    with pytest.raises(AssertionError):
        find_files(family_dir)


def test_analysis_type(analysis):
    assert analysis.old.analysis_type() == 'wes'
    assert analysis.new.analysis_type() == 'wes'


def test_sanity_check(analysis):
    with pytest.raises(ValueError):
        analysis.old.sanity_check()
    with pytest.raises(ValueError):
        analysis.new.sanity_check()


def test_load():
    # for new analysis
    family_dir = 'tests/fixtures/mip/output/family/exomes/family'
    analysis = Analysis(family_dir)
    assert analysis.aligner == 'bwa'
    assert analysis.family_dir == family_dir
