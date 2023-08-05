# -*- coding: utf-8 -*-
from collections import namedtuple

from path import path
import yaml

Genome = namedtuple('Genome', ['build', 'version'])


class BaseSampleInfo(object):

    def load_sampleinfo(self, stream):
        """Load the QC sample info file using YAML parser."""
        self._sampleinfo_data = yaml.load(stream)

        root_keys = list(self._sampleinfo_data)
        assert len(root_keys) == 1, 'Expected only one family id as root key'
        family_id = root_keys[0]

        # only care about loading a subtree of the data
        data_flat = self._sampleinfo_data[family_id]
        self._family = data_flat[family_id]

        # load the sample specific information
        self._samples = {key: value for key, value in data_flat.items()
                         if key != family_id}

    @property
    def analyzed_at(self):
        """Return the date of when the analysis was run.

        Returns:
            datetime: timestamp for when the analysis was run
        """
        # N.B. already parsed as datetime object by PyYAML
        return self._family['AnalysisDate']

    @property
    def status(self):
        """Return the overall status of the analysis.

        Returns:
            str: status category (Unfinished, Finished, Archived)
        """
        return self._family['AnalysisRunStatus']

    @property
    def is_complete(self):
        """Check the analysis run status of the family.

        Returns:
            bool: weather the status is completed or not
        """
        if self.status in ('Finished', 'Archived'):
            return True
        elif self.status == 'notFinished':
            return False
        else:
            raise ValueError("unknown run status: {}".format(self.status))

    @property
    def human_genome(self):
        """Return the human genome reference build info."""
        version = int(self._family['HumanGenomeBuild']['Version'])
        genome = Genome(build=self._family['HumanGenomeBuild']['Source'],
                        version=version)
        return genome

    @property
    def ready_vcf(self):
        """Return the path to the most complete VCF file."""
        return self._family['VCFFile']['ReadyVcf']['Path']

    @property
    def clinical_vcf(self):
        """Return the path to the clinical VCF file."""
        return self._family['VCFFile']['Clinical']['Path']

    @property
    def research_vcf(self):
        """Return the path to the research VCF file."""
        return self._family['VCFFile']['Research']['Path']

    @property
    def qcpedigree_path(self):
        """Return the path to the analysis PED file."""
        return self._family['PedigreeFileAnalysis']['Path']

    @property
    def rankmodel_version(self):
        """Return the version of the rank model used.

        Returns:
            float: version of rank model
        """
        version = float(self._family['Program']['RankVariants']['RankModel']
                                    ['Version'])
        return version

    @property
    def pedigree_svgpath(self):
        """Return the path to the Madeline SVG pedigree output."""
        return self._family['Program'].get('Madeline', {}).get('Path')

    def chanjo_sample_outputs(self):
        """Return a list of chanjo coverage outputs with samples ids."""
        # expect only one chanjo output per sample
        samples_flat = ((sample_id, data[0]) for sample_id, data in
                        self._raw_chanjo_outputs)

        return [(sample_id, path(data['Bed']['Path'])) for sample_id, data in
                samples_flat]

    def chanjo_outputs(self):
        """Return a list of chanjo coverage outputs."""
        return [cov_path for _, cov_path in self.chanjo_sample_outputs()]

    @property
    def qcmetrics_path(self):
        directory = self._family['Program']['QCCollect']['OutDirectory']
        filename = self._family['Program']['QCCollect']['OutFile']
        return path(directory).joinpath(filename)

    @property
    def bcf_path(self):
        """Return the path to the BCF file."""
        bcf_file = self._family.get('BCFFile', {}).get('Path')
        if bcf_file:
            return path(bcf_file)
        else:
            return None


class OldSampleInfoMixin(BaseSampleInfo):

    is_old = True

    @property
    def version(self):
        """MIP <v2.5.1 didn't report the version of the pipeline."""
        return '<2.5.1'

    @property
    def _raw_chanjo_outputs(self):
        """Return input for `chanjo_sample_outputs`."""
        samples = ((sample_id, list(data['Program']['ChanjoAnnotate'].values()))
                   for sample_id, data in self._samples.items())
        return samples

    @property
    def sample_crams(self):
        """Old MIP didn't produce any CRAM files."""
        return None

    @property
    def genelist_file(self):
        """Return the name of master gene list template file."""
        template_file = self._family['VCFParser']['SelectFile']['File']
        return template_file


class SampleInfoMixin(BaseSampleInfo):

    is_old = False

    @property
    def version(self):
        """Return the version of MIP that produced the analysis.

        Returns:
            str: version string
        """
        return self._family['MIPVersion']

    @property
    def _raw_chanjo_outputs(self):
        """Return input for `chanjo_sample_outputs`."""
        samples = ((sample_id, list(data['Program']['SambambaDepth'].values()))
                   for sample_id, data in self._samples.items())
        return samples

    @property
    def sample_crams(self):
        """Return grouped CRAM paths for each sample."""
        crams = {
            sample_id: [value['CramFile'] for key, value
                        in sample['File'].items()
                        if '_' not in key.split('.')[-1]]
            for sample_id, sample in self._samples.items()
        }
        return crams

    @property
    def genelist_file(self):
        """Return the name of master gene list template file."""
        template_path = self._family['VCFParser']['SelectFile']['Path']
        template_file = path(template_path).basename()
        return template_file
