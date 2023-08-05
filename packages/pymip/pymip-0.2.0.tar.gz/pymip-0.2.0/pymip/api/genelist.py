# -*- coding: utf-8 -*-
from path import path


def parse_gene_list(gene_list, list_type, ref_dir):
    """Parse relevant information for scout from gene list."""
    data = {'name': gene_list['Acronym'],
            'version': gene_list['Version'],
            'full_name': gene_list.get('CompleteName', gene_list['Acronym']),
            'date': gene_list.get('Date'),
            'file': path(ref_dir).joinpath(gene_list.get('FileName', '')),
            'type': list_type}
    return data


class GenelistMixin(object):

    def gene_lists(self):
        """Return meta data on all gene lists.

        This includes both research and clinical lists.
        """
        clinical_lists = self._family['VCFParser']['SelectFile']['Database']
        research_lists = self._family['VCFParser']['RangeFile']['Database']
        ref_dir = self.config['referencesDir']

        all_lists = {}
        for data in clinical_lists.values():
            list_data = parse_gene_list(data, 'clinical', ref_dir)
            all_lists[data['Acronym']] = list_data

        for data in research_lists.values():
            list_data = parse_gene_list(data, 'research', ref_dir)
            all_lists[data['Acronym']] = list_data

        return all_lists

    def default_genelists(self):
        """Return a simple list of default gene lists."""
        genelist_ids = self.default_genelist_ids()

        return [data for list_id, data in self.gene_lists().items()
                if list_id in genelist_ids]

    def genelist_name(self):
        """Generate stringified caption for default gene lists."""
        default_genelists = self.default_genelists()
        assert len(default_genelists) > 0, 'No default gene lists'

        gene_lists = ("{} ({})".format(gene_list.get('full_name'),
                                       gene_list.get('version'))
                      for gene_list in default_genelists)

        return ' + '.join(gene_lists)
