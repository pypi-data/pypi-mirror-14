# -*- coding: utf-8 -*-
from datetime import datetime

from path import path
import pytest
import yaml


def test_archive_path(analysis, archived):
    with pytest.raises(ValueError):
        analysis.old.archive_path

    assert archived.archive_path.endswith('exomes/family/bundle')


def test_archive_date(analysis, archived):
    with pytest.raises(ValueError):
        analysis.new.archive_date

    assert archived.archive_date.year == 2016
    assert archived.archive_date.month == 2
    assert archived.archive_date.day == 3


def test_is_archived(analysis, archived):
    assert analysis.new.is_archived is False
    assert archived.is_archived is True


def test_archive_files(analysis):
    files = list(analysis.new.archive_files())
    assert len(files) == 9
    assert files[0].category == 'family'
    assert files[0].file == ("/mnt/hds/proj/bioinfo/develop/cust000/family/"
                             "analysis/exomes/family/family_qcmetrics.yaml")

    assert files[1].category == 'family'
    assert files[1].file == ("/mnt/hds/proj/bioinfo/develop/cust000/family/"
                             "analysis/exomes/family/qc_pedigree.yaml")

    bcf_path = ("/mnt/hds/proj/bioinfo/develop/cust000/family/analysis/exomes"
                "/family/bwa/gatk/family_sorted_smd_rreal_brecal_gvcf_vrecal_"
                "comb_BOTH.bcf")
    assert files[2].category == 'family'
    assert files[2].file == bcf_path

    assert files[3].category == 'family'
    assert files[3].file == bcf_path + '.csi'

    log_path = ("/mnt/hds/proj/bioinfo/develop/cust000/family/analysis/exomes"
                "/family/mip_log/2016-03-07/mip.pl_2016-03-07T13:26:29.log")
    assert files[4].category == 'family'
    assert files[4].file == log_path

    assert set(_file.category for _file in files[5:]).pop() == 'sample'
    crams = ["/mnt/hds/proj/bioinfo/develop/cust000/family/analysis/exomes/"
             "sample/bwa/sample.150724_H3JVYBCXX_GTCGTAGA.lane1_sorted.cram",
             "/mnt/hds/proj/bioinfo/develop/cust000/family/analysis/exomes/"
             "sample/bwa/sample.150724_H3JVYBCXX_GTCGTAGA.lane2_sorted.cram",
             "/mnt/hds/proj/bioinfo/develop/cust000/family/analysis/exomes/"
             "sample/bwa/sample.150724_H3KLYBCXX_GTCGTAGA.lane1_sorted.cram",
             "/mnt/hds/proj/bioinfo/develop/cust000/family/analysis/exomes/"
             "sample/bwa/sample.150724_H3KLYBCXX_GTCGTAGA.lane2_sorted.cram"]
    assert set(_file.file for _file in files[5:]) == set(crams)


def test_update_status(analysis, tmpdir):
    for ianalysis in [analysis.old, analysis.new]:
        qc_file = tmpdir.join('qc-test.yaml')
        archive_path = 'tests/fixtures/archive'
        status = 'Archived'
        now_date = datetime.now()
        ianalysis.update_status(status, archive_path, out_path=str(qc_file))
        with qc_file.open() as stream:
            sampleinfo_data = yaml.load(stream)
            new_status = sampleinfo_data['family']['family']['AnalysisRunStatus']
            new_archive_path = sampleinfo_data['family']['family']['ArchivePath']
            new_archive_date = sampleinfo_data['family']['family']['ArchiveDate']
        assert new_status == status
        assert new_archive_path == archive_path
        assert new_archive_date.year == now_date.year
        assert new_archive_date.month == now_date.month
        assert new_archive_date.day == now_date.day


def test_sample_bams(analysis):
    samples = analysis.old.sample_bams
    assert len(samples) == 1  # number of samples
    assert samples[0][0] == 'sample'  # sample id
    assert len(samples[0][1]) == 2  # number of BAM files
    filename = 'sample.141030_HAH66ADXX_TGACCA.lane1_sorted.bam'
    filenames = set(path(bam).basename() for bam in samples[0][1])
    assert filename in filenames

    samples = analysis.new.sample_bams
    assert len(samples) == 1  # number of samples
    assert samples[0][0] == 'sample'  # sample id
    assert len(samples[0][1]) == 4  # number of BAM files
    endings = ['sample.150724_H3JVYBCXX_GTCGTAGA.lane1_sorted.bam',
               'sample.150724_H3JVYBCXX_GTCGTAGA.lane2_sorted.bam',
               'sample.150724_H3KLYBCXX_GTCGTAGA.lane1_sorted.bam',
               'sample.150724_H3KLYBCXX_GTCGTAGA.lane2_sorted.bam']
    assert set(path(bam).basename() for bam in samples[0][1]) == set(endings)


def test_lane_bams(analysis):
    files = list(analysis.old.lane_bams)
    assert len(files) == 2
