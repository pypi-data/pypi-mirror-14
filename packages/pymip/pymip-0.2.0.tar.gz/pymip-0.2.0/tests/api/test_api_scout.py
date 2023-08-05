# -*- coding: utf-8 -*-
import pytest


def test_scout_config_clinical(analysis):
    config = analysis.new.scout_config('clinical')
    assert config['load_vcf'] == analysis.new.clinical_vcf
    assert config['variant_type'] == 'clinical'


def test_scout_config_research(analysis):
    config = analysis.new.scout_config('research')
    assert config['load_vcf'] == analysis.new.research_vcf
    assert config['variant_type'] == 'research'

    # test with invalid variant type
    with pytest.raises(ValueError):
        analysis.new.scout_config('future')
