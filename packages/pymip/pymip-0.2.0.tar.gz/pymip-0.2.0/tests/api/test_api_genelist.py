# -*- coding: utf-8 -*-
from datetime import date
import os

import pytest

from pymip.api.genelist import parse_gene_list


def test_parse_gene_list(genelist):
    list_type = 'clinical'
    ref_dir = '/tmp/references'
    data = parse_gene_list(genelist, list_type, ref_dir)
    assert data['name'] == genelist['Acronym']
    assert data['version'] == genelist['Version']
    assert data['full_name'] == genelist['CompleteName']
    assert data['date'] == genelist['Date']
    assert data['file'] == os.path.join(ref_dir, genelist['FileName'])
    assert data['type'] == list_type


def test_gene_lists(analysis):
    lists = analysis.old.gene_lists()
    assert isinstance(lists, dict)
    assert len(lists) == 8
    assert lists['IEM']['full_name'] == 'Inborn Errors of Metabolism'

    lists = analysis.new.gene_lists()
    assert isinstance(lists, dict)
    assert len(lists) == 12
    assert lists['SKD']['full_name'] == 'Skeletal dysplasia'
    assert lists['SKD']['date'] == date(2016, 1, 24)


def test_default_genelists(analysis):
    lists = analysis.old.default_genelists()
    assert isinstance(lists, list)
    assert lists == []

    lists = analysis.new.default_genelists()
    assert isinstance(lists, list)
    assert len(lists) == 1
    assert lists[0]['name'] == 'IEM'


def test_genelist_name(analysis):
    # no default gene lists
    with pytest.raises(AssertionError):
        analysis.old.genelist_name()

    assert analysis.new.genelist_name() == 'Inborn Errors of Metabolism (8.1)'
