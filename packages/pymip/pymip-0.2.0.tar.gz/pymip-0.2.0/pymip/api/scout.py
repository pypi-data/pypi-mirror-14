# -*- coding: utf-8 -*-


class ScoutMixin(object):

    """Provide higher order Scout functionality.

    Depends on pretty much all other mixins.
    """

    def scout_config(self, variant_type='clinical'):
        """Build a base Scout config."""
        individuals = {sample_id: {
            'name': sample_id,
            'bam_path': sample['MostCompleteBAM']['Path'],
            'capture_kit': sample.get('Capture_kit', []),
        } for sample_id, sample in self._samples.items()}

        owner = self.instance_tags[0]
        collaborators = self.instance_tags[1:]
        config = {
            'load': True,
            'ped': self._family['PedigreeFile']['Path'],
            'igv_vcf': self.ready_vcf,
            'human_genome_build': self.human_genome.build,
            'human_genome_version': self.human_genome.version,
            'owner': owner,
            'collaborators': collaborators,
            'madeline': self.pedigree_svgpath,
            'gene_lists': self.gene_lists(),
            'default_panels': self.default_genelist_ids(),
            'individuals': individuals,
            'rank_model_version': self.rankmodel_version,
            'analysis_type': self.analysis_type(),
            'analysis_date': str(self.analyzed_at),
            'variant_type': variant_type,
            'family_type': 'alt'
        }

        if variant_type == 'clinical':
            config['load_vcf'] = self.clinical_vcf
        elif variant_type == 'research':
            config['load_vcf'] = self.research_vcf
        else:
            raise ValueError("invalid option for 'variant_type': {}"
                             .format(variant_type))

        return config
