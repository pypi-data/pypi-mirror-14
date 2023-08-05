# -*- coding: utf-8 -*-


def fastq_name(lane, date, flowcell, sample, index, read):
    """Build a string representing FASTQ file name.
    The naming follows MIP conventions. The syntax is as follows:
        1_140818_H9FD3ADXX_000127T_GATCAG_1.fastq.gz
    """
    if read not in ('1', '2'):
        raise ValueError("'read' must be either of directions: '1' or '2'")

    elif '_' in sample:
        raise ValueError("'sample' must not contain any underscores")

    return ("{lane}_{date}_{flowcell}_{sample}_{index}_{read}.fastq.gz"
            .format(lane=lane, date=date, flowcell=flowcell, sample=sample,
                    index=index, read=read))
