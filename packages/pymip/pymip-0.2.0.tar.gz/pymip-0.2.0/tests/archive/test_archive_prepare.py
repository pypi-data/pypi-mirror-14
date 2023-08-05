# -*- coding: utf-8 -*-
import pytest

from pymip.archive.prepare import convert_bcf, family_args


def test_convert_bcf(tmpdir):
    bcf_out = tmpdir.join('test.bcf')
    vcf_in = 'tests/fixtures/mip/vcf/test.vcf'
    convert_bcf(vcf_in, str(bcf_out))
    assert bcf_out.exists()

    # test dry_run
    assert convert_bcf(vcf_in, str(bcf_out), dry_run=True) == (0, 0)


def test_family_args(analysis):
    with pytest.raises(ValueError):
        family_args(analysis.new)

    args = family_args(analysis.old)
    assert args.vcf_file == analysis.old.ready_vcf
    assert list(args.bam_files) == list(analysis.old.lane_bams)
    assert args.jobname == 'BAM2CRAM_family'
