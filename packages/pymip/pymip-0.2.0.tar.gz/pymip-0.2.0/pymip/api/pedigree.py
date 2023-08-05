# -*- coding: utf-8 -*-
from ped_parser import FamilyParser


class PedigreeMixin(object):

    def load_pedigree(self, stream):
        """Load the pedigree using `ped_parser`."""
        self.ped = FamilyParser(stream, family_type='alt', cmms_check=False)

    def default_genelist_ids(self, ped_key='Clinical_db'):
        """Return a simple list of ids for the default gene lists."""
        ind_lists = (data.extra_info.get(ped_key, '').split(';')
                     for ind_id, data in self.ped.individuals.items()
                     if ped_key in data.extra_info)

        # flatten list of lists
        return [item for sublist in ind_lists for item in sublist]

    @property
    def ped_analysistype(self):
        """Determine the analysis type."""
        ped_types = (ind.extra_info.get('Sequencing_type') for ind in
                     self.ped.individuals.values())
        inc_pedtypes = set(filter(None, ped_types))
        if len(inc_pedtypes) > 1:
            return 'mixed'
        elif len(inc_pedtypes) == 1:
            return inc_pedtypes.pop().lower()
        else:
            return None
