# -*- coding: utf-8 -*-

from __future__ import absolute_import
import re
from mapdepot.schemas.base import Base


class Topographic(Base):
    """Topographic Series Schemas.

    <Series>_<Sheet>_<Edition>_<Distributor>_(<Area>_<Country>)
    G628_4565_ED01_TGD_(ACHA_N_ANIR_MALI)
    """

    name = 'Topographic Series'

    @property
    def series(self):
        return self._search(r'^([a-zA-Z\d]+)', self.basename)

    @property
    def sheet(self):
        return self._search(r'_([a-zA-Z\d\-]+)', self.basename)

    @property
    def distributor(self):
        return self._search(r'[\-_ ]?([a-zA-Z\d]+)[\-_ ]?\(', self.basename)

    @property
    def location(self):
        return self._search(r'\(([\w ,\-_]+)\)', self.basename)

    @property
    def cities(self):
        location = re.split(r'[,_]', self.location)
        if location:
            del location[-1]
            return location

    @property
    def countries(self):
        location = re.split(r'[,_]', self.location)
        if location:
            return re.split(r'[\-]', location[-1])

    @property
    def validation(self):
        return {
            'series': bool(self.directories[-1] == self.series),
            'sheet': bool(self.directories[-2][0] == self.series[0])
        }

    @property
    def json(self):
        """Building JSON object."""
        return {
            'tags': {
                'series': self.series,
                'edition': self.edition,
                'sheet': self.sheet,
                'distributor': self.distributor,
                'location': {
                    'cities': self.cities,
                    'countries': self.countries
                }
            },
            'validation': self.validation,
            'accuracy': self.accuracy,
            'directories': self.directories,
            'filename': self.filename,
            'extension': self.extension,
            'schema': self.name
        }

if __name__ == '__main__':
    filename = 'P761_1990-1_ed3_DMA_(TAJURA, LIBYA).tif'
    topo = Topographic(filename)
    print(topo.json)
