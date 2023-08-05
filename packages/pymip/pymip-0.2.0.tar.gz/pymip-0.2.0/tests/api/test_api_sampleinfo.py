# -*- coding: utf-8 -*-
import pytest


def test_sampleinfo_class(sampleinfo):
    assert sampleinfo.old.is_old is True
    assert sampleinfo.new.is_old is False


def test_status(sampleinfo):
    assert sampleinfo.old.status == 'Finished'
    assert sampleinfo.new.status == 'Finished'


def test_analyzed_at(sampleinfo):
    assert sampleinfo.old.analyzed_at.year == 2015
    assert sampleinfo.old.analyzed_at.month == 3
    assert sampleinfo.old.analyzed_at.day == 3

    assert sampleinfo.new.analyzed_at.year == 2016
    assert sampleinfo.new.analyzed_at.month == 3
    assert sampleinfo.new.analyzed_at.day == 8


def test_is_complete(sampleinfo, alt_sampleinfo):
    assert sampleinfo.old.is_complete is True
    assert sampleinfo.new.is_complete is True
    assert alt_sampleinfo.notfinished.is_complete is False
    with pytest.raises(ValueError):
        alt_sampleinfo.error.is_complete


def test_human_genome(sampleinfo):
    assert sampleinfo.old.human_genome.build == 'GRCh'
    assert sampleinfo.old.human_genome.version == 37

    assert sampleinfo.new.human_genome.build == 'GRCh'
    assert sampleinfo.new.human_genome.version == 37


def test_ready_vcf(sampleinfo):
    ending = 'bwa/gatk/family_sorted_pmd_rreal_brecal_gvcf_vrecal_BOTH.vcf'
    assert sampleinfo.old.ready_vcf.endswith(ending)

    ending = 'family_sorted_smd_rreal_brecal_gvcf_vrecal_comb_BOTH.vcf'
    assert sampleinfo.new.ready_vcf.endswith(ending)


def test_clinical_vcf(sampleinfo):
    ending = ("family_sorted_pmd_rreal_brecal_gvcf_vrecal_vep_parsed_snpeff_"
              "ranked_BOTH.selected.vcf")
    assert sampleinfo.old.clinical_vcf.endswith(ending)

    ending = ("bwa/gatk/family_sorted_smd_rreal_brecal_gvcf_vrecal_"
              "comb_vt_vep_parsed_snpeff_ranked_BOTH.selected.vcf")
    assert sampleinfo.new.clinical_vcf.endswith(ending)


def test_research_vcf(sampleinfo):
    ending = ("bwa/gatk/family_sorted_pmd_rreal_brecal_gvcf_vrecal_vep_"
              "parsed_snpeff_ranked_BOTH.vcf")
    assert sampleinfo.old.research_vcf.endswith(ending)

    ending = ("bwa/gatk/family_sorted_smd_rreal_brecal_gvcf_vrecal_"
              "comb_vt_vep_parsed_snpeff_ranked_BOTH.vcf")
    assert sampleinfo.new.research_vcf.endswith(ending)


def test_version(sampleinfo):
    assert sampleinfo.old.version == '<2.5.1'
    assert sampleinfo.new.version == 'v2.6.1'


def test_bcf_path(sampleinfo):
    assert sampleinfo.old.bcf_path is None

    ending = ("family/bwa/gatk/family_sorted_smd_rreal_brecal_"
              "gvcf_vrecal_comb_BOTH.bcf")
    assert sampleinfo.new.bcf_path.endswith(ending)


def test_qcpedigree_path(sampleinfo):
    ending = 'family/analysis/exomes/family/qc_pedigree.yaml'
    assert sampleinfo.old.qcpedigree_path.endswith(ending)

    ending = 'family/analysis/exomes/family/qc_pedigree.yaml'
    assert sampleinfo.new.qcpedigree_path.endswith(ending)


def test_rankmodel_version(sampleinfo):
    assert sampleinfo.old.rankmodel_version == 1.5
    assert sampleinfo.new.rankmodel_version == 1.13


def test_pedigree_svgpath(sampleinfo):
    ending = 'family/analysis/exomes/family/madeline/family_madeline.xml'
    assert sampleinfo.old.pedigree_svgpath.endswith(ending)

    assert sampleinfo.new.pedigree_svgpath is None


def test_chanjo_sample_outputs(sampleinfo):
    ending = ("sample/bwa/coverageReport/sample_lanes_12_sorted_merged_pmd_"
              "rreal_brecal_coverage.bed")
    files = sampleinfo.old.chanjo_sample_outputs()
    assert len(files) == 1
    assert files[0][0] == 'sample'
    assert files[0][1].endswith(ending)

    ending = ("bwa/coveragereport/sample_lanes_1122_sorted_merged_"
              "smd_rreal_brecal_coverage.bed")
    files = sampleinfo.new.chanjo_sample_outputs()
    assert len(files) == 1
    assert files[0][0] == 'sample'
    assert files[0][1].endswith(ending)


def test_chanjo_outputs(sampleinfo):
    ending = ("sample/bwa/coverageReport/sample_lanes_12_sorted_merged_pmd_"
              "rreal_brecal_coverage.bed")
    files = sampleinfo.old.chanjo_outputs()
    assert len(files) == 1
    assert files[0].endswith(ending)

    ending = ("bwa/coveragereport/sample_lanes_1122_sorted_merged_"
              "smd_rreal_brecal_coverage.bed")
    files = sampleinfo.new.chanjo_outputs()
    assert len(files) == 1
    assert files[0].endswith(ending)


def test_qcmetrics_path(sampleinfo):
    ending = 'family/analysis/exomes/family/family_qcmetrics.yaml'
    assert sampleinfo.old.qcmetrics_path.endswith(ending)

    ending = 'family/analysis/exomes/family/family_qcmetrics.yaml'
    assert sampleinfo.new.qcmetrics_path.endswith(ending)


def test_sample_crams(sampleinfo):
    assert sampleinfo.old.sample_crams is None

    samples = sampleinfo.new.sample_crams
    assert len(samples) == 1
    crams = list(samples.values())[0]
    assert len(crams) == 4
    for cram in crams:
        assert (cram.endswith('.lane1_sorted.cram') or
                cram.endswith('.lane2_sorted.cram'))


def test_genelist_file(sampleinfo):
    assert sampleinfo.old.genelist_file == 'cust000-Clinical_master_list.txt'
    assert sampleinfo.new.genelist_file == 'cust000-Clinical_master_list.txt'
