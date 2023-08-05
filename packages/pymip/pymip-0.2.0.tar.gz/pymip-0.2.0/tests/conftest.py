# -*- coding: utf-8 -*-
from collections import namedtuple
import codecs

import pytest

from pymip.api import (ConfigMixin, OldConfigMixin, OldSampleInfoMixin,
                       SampleInfoMixin, PedigreeMixin, Analysis, OldAnalysis)

Versions = namedtuple('Config', ['old', 'new'])
Pedigrees = namedtuple('Pedigrees', ['single', 'multi', 'mixed'])
Sampleinfo = namedtuple('Sampleinfo', ['notfinished', 'error'])


@pytest.yield_fixture(scope='session')
def config():
    old_config = OldConfigMixin()
    new_config = ConfigMixin()

    old_conf_path = 'tests/fixtures/mip/config/old_config.yaml'
    with codecs.open(old_conf_path, 'r') as stream:
        old_config.load_config(stream)

    new_conf_path = 'tests/fixtures/mip/config/new_config.yaml'
    with codecs.open(new_conf_path, 'r') as stream:
        new_config.load_config(stream)

    yield Versions(old=old_config, new=new_config)


@pytest.yield_fixture(scope='session')
def sampleinfo():
    old_sampleinfo = OldSampleInfoMixin()
    new_sampleinfo = SampleInfoMixin()

    old_path = 'tests/fixtures/mip/sampleinfo/old_qc_sampleInfo.yaml'
    with codecs.open(old_path, 'r') as stream:
        old_sampleinfo.load_sampleinfo(stream)

    new_path = 'tests/fixtures/mip/sampleinfo/new_qc_sampleInfo.yaml'
    with codecs.open(new_path, 'r') as stream:
        new_sampleinfo.load_sampleinfo(stream)

    yield Versions(old=old_sampleinfo, new=new_sampleinfo)


@pytest.yield_fixture(scope='session')
def alt_sampleinfo():
    error_sampleinfo = OldSampleInfoMixin()
    error_path = 'tests/fixtures/mip/sampleinfo/error_qc_sampleInfo.yaml'
    with codecs.open(error_path, 'r') as stream:
        error_sampleinfo.load_sampleinfo(stream)

    notfinished_sampleinfo = SampleInfoMixin()
    notfinished_path = 'tests/fixtures/mip/sampleinfo/notfinished_qc_sampleInfo.yaml'
    with codecs.open(notfinished_path, 'r') as stream:
        notfinished_sampleinfo.load_sampleinfo(stream)

    yield Sampleinfo(notfinished=notfinished_sampleinfo, error=error_sampleinfo)


@pytest.yield_fixture(scope='session')
def pedigree():
    single_path = 'tests/fixtures/mip/pedigree/single-complete_pedigree.txt'
    single = PedigreeMixin()
    with codecs.open(single_path) as stream:
        single.load_pedigree(stream)

    multi_path = 'tests/fixtures/mip/pedigree/multi-minimal_pedigree.txt'
    multi = PedigreeMixin()
    with codecs.open(multi_path) as stream:
        multi.load_pedigree(stream)

    mixed_path = 'tests/fixtures/mip/pedigree/multi-mixed_pedigree.txt'
    mixed = PedigreeMixin()
    with codecs.open(mixed_path) as stream:
        mixed.load_pedigree(stream)

    _pedigree = Pedigrees(single, multi, mixed)

    yield _pedigree


@pytest.yield_fixture(scope='session')
def genelist():
    _genelist = {
        'Acronym': 'FullList',
        'CompleteName': 'Clinical master list',
        'Date': '2016-02-22',
        'FileName': 'cust000-Clinical_master_list.txt',
        'GenomeBuild': 'GRCh37.p13',
        'Version': '16.1'
    }
    yield _genelist


@pytest.yield_fixture(scope='session')
def analysis():
    new = Analysis()
    config = 'tests/fixtures/mip/config/new_config.yaml'
    sampleinfo = 'tests/fixtures/mip/sampleinfo/new_qc_sampleInfo.yaml'
    pedigree = 'tests/fixtures/mip/pedigree/single-complete_pedigree.txt'
    with codecs.open(config) as stream:
        new.load_config(stream)
    with codecs.open(sampleinfo) as stream:
        new.load_sampleinfo(stream)
    with codecs.open(pedigree) as stream:
        new.load_pedigree(stream)

    old = OldAnalysis()
    config = 'tests/fixtures/mip/config/old_config.yaml'
    sampleinfo = 'tests/fixtures/mip/sampleinfo/old_qc_sampleInfo.yaml'
    pedigree = 'tests/fixtures/mip/pedigree/multi-minimal_pedigree.txt'
    with codecs.open(config) as stream:
        old.load_config(stream)
    with codecs.open(sampleinfo) as stream:
        old.load_sampleinfo(stream)
    with codecs.open(pedigree) as stream:
        old.load_pedigree(stream)

    _analysis = Versions(new=new, old=old)
    yield _analysis


@pytest.yield_fixture(scope='session')
def archived():
    _archived = Analysis()
    qc_path = ("tests/fixtures/mip/configs/archived/family/exomes/family/"
               "family_qc_sampleInfo.yaml")
    with open(qc_path) as stream:
        _archived.load_sampleinfo(stream)
    yield _archived
