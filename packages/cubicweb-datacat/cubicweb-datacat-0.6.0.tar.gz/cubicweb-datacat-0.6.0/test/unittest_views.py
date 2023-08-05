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

"""cubicweb-datacat tests for views"""

from datetime import datetime
from tempfile import NamedTemporaryFile

from mock import patch
from pytz import utc
from rdflib.compare import to_isomorphic

from cubicweb.devtools.testlib import CubicWebTC

from cubes.skos.rdfio import default_graph


class RDFAdapterTC(CubicWebTC):
    """Test case for RDF data export."""

    def setup_database(self):
        # patch now() so that computed datetime attributes always return the same datetime
        # See https://docs.python.org/3/library/unittest.mock-examples.html#partial-mocking
        with patch('cubes.datacat.hooks.datetime') as mock_dt:
            mock_dt.now.return_value = datetime(2016, 02, 02, 15, 25, 0, tzinfo=utc)
            mock_dt.side_effect = datetime
            # Now set up entities
            with self.admin_access.repo_cnx() as cnx:
                scheme = cnx.create_entity('ConceptScheme', cwuri=u'http://example.org/scheme',
                                           title=u'Concept Scheme')
                nat_concept = scheme.add_concept(u'National authority')
                attribution_concept = scheme.add_concept(u'Attribution')
                annual_concept = scheme.add_concept(u'Annual')
                csv_concept = scheme.add_concept(u'CSV')
                xls_concept = scheme.add_concept(u'Excel XLS')
                appxls_concept = scheme.add_concept(u'application/vnd.ms-excel')
                zip_concept = scheme.add_concept(u'ZIP')
                appzip_concept = scheme.add_concept(u'application/zip')
                eng_concept = scheme.add_concept(u'English')
                edu_concept = scheme.add_concept(u'Education, culture and sport')
                publisher = cnx.create_entity('Agent', name=u'The Publisher',
                                              publisher_type=nat_concept,
                                              email=u'publisher@example.org')
                contact = cnx.create_entity('Agent', name=u'The Contact Point',
                                            email=u'contact@example.org')
                license = cnx.create_entity('LicenseDocument', license_type=attribution_concept)
                cat = cnx.create_entity('DataCatalog', title=u'My Catalog',
                                        description=u'A nice catalog', catalog_publisher=publisher,
                                        homepage=u'http://cat.example.org', language=eng_concept,
                                        theme_taxonomy=scheme, license=license,
                                        issued=datetime(2016, 02, 01, 20, 40, 0, tzinfo=utc),
                                        modified=datetime(2016, 02, 02, 18, 25, 0, tzinfo=utc))
                ds = cnx.create_entity('Dataset', title=u'First Dataset', description=u'A dataset',
                                       in_catalog=cat, dataset_publisher=publisher,
                                       dataset_contact_point=contact, keyword=u'keyword',
                                       dataset_frequency=annual_concept, dcat_theme=edu_concept)
                cnx.create_entity('Distribution', title=u'First Dataset (CSV)',
                                  description=u'First Dataset in CSV format', of_dataset=ds,
                                  license=license, distribution_format=csv_concept,
                                  access_url=u'http://www.example.org')
                cnx.create_entity('Distribution', title=u'First Dataset (XLS)',
                                  description=u'First Dataset in XLS format', of_dataset=ds,
                                  license=license, distribution_format=xls_concept,
                                  distribution_media_type=appxls_concept,
                                  access_url=u'http://www.example.org')
                cnx.create_entity('Distribution', title=u'First Dataset (ZIP)',
                                  description=u'First Dataset in ZIP format', of_dataset=ds,
                                  license=license, distribution_format=zip_concept,
                                  distribution_media_type=appzip_concept,
                                  access_url=u'http://www.example.org')
                cnx.commit()
                self.cat_eid = cat.eid

    def test_complete_rdf_view(self):
        with self.admin_access.client_cnx() as cnx:
            cat = cnx.entity_from_eid(self.cat_eid)
            with NamedTemporaryFile() as f:
                f.write(cat.view('dcat.rdf.complete'))
                f.seek(0)
                graph = default_graph()
                graph.load('file://' + f.name, rdf_format='xml')
            expected_graph = default_graph()
            expected_graph.load('file://' + self.datapath('valid_export.xml'), rdf_format='xml')
            self.assertEqual(to_isomorphic(graph._graph), to_isomorphic(expected_graph._graph))


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
