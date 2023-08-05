# -*- coding: utf-8 -*-
import codecs
from collections import namedtuple
from datetime import datetime

from path import path
import yaml

Asset = namedtuple('Asset', ['category', 'file'])


class ArchiveMixin(object):

    """Provide higher level functions to handle archiving an analysis.

    Depends on :class:`pymip.api.SampleInfoMixin` and
    :class:`pymip.api.ConfigMixin`.
    """

    @property
    def is_archived(self):
        """Check if analysis has been marked as archived."""
        return self.status == 'Archived'

    @property
    def archive_path(self):
        """Return the archive path for an archived analysis."""
        if not self.is_archived:
            raise ValueError('analysis not archived')
        else:
            return self._family['ArchivePath']

    @property
    def archive_date(self):
        """Return the archive date for an archived analysis."""
        if not self.is_archived:
            raise ValueError('analysis not archived')
        else:
            return self._family['ArchiveDate']

    def archive_files(self):
        """Select the files to be bundled for archiving purposes.

        Files:
            - Non-annotated BCF file + index
            - QC metrics file
            - Analysis specific ped file
            - Latest MIP log file
            - CRAM files for each sample/lane
        """
        yield Asset(category=self.family_id, file=self.qcmetrics_path)
        yield Asset(category=self.family_id, file=self.qcpedigree_path)

        bcf_path = (self.ready_vcf.replace('.vcf', '.bcf')
                    if self.is_old else self.bcf_path)
        csi_path = "{}.csi".format(bcf_path)
        yield Asset(category=self.family_id, file=bcf_path)
        yield Asset(category=self.family_id, file=csi_path)
        yield Asset(category=self.family_id, file=self.log_path)

        for sample_id, cram_files in self.sample_crams.items():
            for cram_file in cram_files:
                yield Asset(category=sample_id, file=cram_file)

    def update_status(self, status, archive_path=None, out_path=None):
        """Update the analysis status in QC sample info."""
        family_data = self._sampleinfo_data[self.family_id][self.family_id]
        if status == 'Archived':
            family_data['ArchivePath'] = archive_path
            family_data['ArchiveDate'] = datetime.now()
        family_data['AnalysisRunStatus'] = status

        with codecs.open(out_path or self.configs.sampleinfo, 'w') as stream:
            yaml.dump(self._sampleinfo_data, stream=stream)

    @property
    def sample_bams(self):
        """Return per sample/lane BAM files."""
        aligner_id = 'MosaikAligner' if self.aligner == 'mosaik' else 'Bwa'
        files = [(sample_id,
                  ["{}_sorted.bam".format(path(data['OutDirectory'].rstrip('info/')).joinpath(lane_id))
                   for lane_id, data in sample['Program'][aligner_id].items()])
                 for sample_id, sample in self._samples.items()]
        return files

    @property
    def lane_bams(self):
        """Return all BAM files (one per lane and sample)."""
        for sample_id, bam_files in self.sample_bams:
            for bam_file in bam_files:
                yield bam_file
