# -*- coding: utf-8 -*-


def test_default_genelist_ids(pedigree):
    assert pedigree.single.default_genelist_ids() == ['IEM']
    assert pedigree.multi.default_genelist_ids() == []


def test_ped_analysistype(pedigree):
    assert pedigree.single.ped_analysistype == 'wes'
    assert pedigree.multi.ped_analysistype is None
    assert pedigree.mixed.ped_analysistype == 'mixed'
