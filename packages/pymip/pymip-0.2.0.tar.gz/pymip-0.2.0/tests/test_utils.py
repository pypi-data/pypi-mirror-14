# -*- coding: utf-8 -*-
import pytest

from pymip.utils import fastq_name


def test_fastq_name():
    """Test FASTQ file name generator."""
    args = ['1', '140127', 'H8A7MADXX', '0002P021', 'ACTTGA', '2']
    name = fastq_name(*args)
    expected = '1_140127_H8A7MADXX_0002P021_ACTTGA_2.fastq.gz'

    assert name == expected

    args[-1] = '4'
    with pytest.raises(ValueError):
        fastq_name(*args)

    args[-1] = '1'
    args[3] = 'sample_fact'
    with pytest.raises(ValueError):
        fastq_name(*args)
