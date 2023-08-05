# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-datacat vocabularies (concept schemes)"""

from __future__ import print_function

from os.path import dirname, join

from cubicweb.dataimport import massive_store, stores, ucsvreader
from cubicweb.dataimport.importer import ExtEntity, SimpleImportLog

from cubes.skos.sobjects import import_skos_extentities


DCAT_SCHEMES = [
    (u'ADMS vocabularies',
     u'https://joinup.ec.europa.eu/svn/adms/ADMS_v1.00/ADMS_SKOS_v1.00.rdf'),
    (u'European Frequency Named Authority List',
     u'http://publications.europa.eu/mdr/resource/authority/frequency/skos/frequencies-skos.rdf'),
    (u'European Filetypes Authority Table',
     u'http://publications.europa.eu/mdr/resource/authority/file-type/skos/filetypes-skos.rdf'),
    (u'European Languages Named Authority List',
     u'http://publications.europa.eu/mdr/resource/authority/language/skos/languages-skos.rdf'),
    (u'European Dataset Theme Vocabulary',
     u'http://publications.europa.eu/mdr/resource/authority/data-theme/skos/data-theme-skos.rdf'),
]


def add_source(cnx, name, url):
    return cnx.create_entity('SKOSSource', name=name, url=url)


def datapath(fname):
    return join(dirname(__file__), 'migration', 'data', fname)


def media_types_extentities(media_types=None):
    """Yield ExtEntity objects fetch from parsing IANA CSV files from
    http://www.iana.org/assignments/media-types/media-types.xml.

    If media_types is specified, it should be a list of domain to import.
    Otherwise all domains will be imported.
    """
    iana_uri = 'http://www.iana.org/assignments/media-types/media-types.xml'
    yield ExtEntity('ConceptScheme', iana_uri, {'title': set([u'IANA Media Types'])})
    if media_types is None:
        media_types = ('application', 'audio', 'image', 'message', 'model',
                       'multipart', 'text', 'video')
    for typename in media_types:
        with open(datapath(typename + '.csv')) as f:
            reader = ucsvreader(f, encoding='utf-8', delimiter=',', skipfirst=True)
            concepts = set([])
            for line in reader:
                fulltypename = typename + '/' + line[0]
                if fulltypename in concepts:
                    # Only consider first occurences.
                    continue
                concepts.add(fulltypename)
                yield ExtEntity('Concept', fulltypename, {'in_scheme': set([iana_uri])})
                yield ExtEntity('Label', fulltypename + '_label',
                                {'label': set([fulltypename]),
                                 'language_code': set([u'en']),
                                 'kind': set([u'preferred']),
                                 'label_of': set([fulltypename])})


def media_types_import(cnx, **kwargs):
    """Import of IANA media types concepts from CSV files."""
    import_log = SimpleImportLog('Media Types')
    if cnx.repo.system_source.dbdriver == 'postgres':
        store = massive_store.MassiveObjectStore(cnx)
    else:
        store = stores.NoHookRQLObjectStore(cnx)
    stats, (scheme, ) = import_skos_extentities(
        cnx, media_types_extentities(**kwargs), import_log, store=store,
        raise_on_error=True)
    return stats, scheme
