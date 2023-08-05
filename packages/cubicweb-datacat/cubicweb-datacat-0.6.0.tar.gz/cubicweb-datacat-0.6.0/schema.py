# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-datacat schema"""

from yams.buildobjs import (EntityType, RelationDefinition, String,
                            RichString, TZDatetime, Int)
from cubicweb.schema import (RRQLExpression, ERQLExpression,
                             WorkflowableEntityType, RQLConstraint,
                             RQLVocabularyConstraint)

from cubes.file.schema import File


_ = unicode


def publication_metadata(cls):
    """Class decorator that adds publication metadata to an entity type."""
    cls.add_relation(TZDatetime(description=_('publication date')),
                     name='issued')
    cls.add_relation(TZDatetime(description=_('modification date')),
                     name='modified')
    return cls


class Agent(EntityType):
    name = String(required=True, fulltextindexed=True)
    email = String()
    description = _(
        'An agent (eg. person, group, software or physical artifact).')


class publisher_type(RelationDefinition):
    subject = 'Agent'
    object = 'Concept'
    cardinality = '?*'
    inlined = True
    description = _("type of agent")


@publication_metadata
class DataCatalog(EntityType):
    """A data catalog is a curated collection of metadata about datasets."""
    title = String(required=True, fulltextindexed=True)
    description = RichString(required=True, fulltextindexed=True)
    homepage = String(description=_('URL to the catalog home page'))


class language(RelationDefinition):
    subject = 'DataCatalog'
    object = 'Concept'
    description = _('languages used in the catalog')


class theme_taxonomy(RelationDefinition):
    subject = 'DataCatalog'
    object = 'ConceptScheme'


class catalog_publisher(RelationDefinition):
    subject = 'DataCatalog'
    object = 'Agent'
    inlined = True
    cardinality = '1*'
    description = _(
        'relate a catalog to an agent (organization) responsible for making it available')


@publication_metadata
class Dataset(EntityType):
    # DCAT attributes.
    identifier = String(fulltextindexed=True)
    title = String(required=True, fulltextindexed=True)
    description = RichString(required=True, fulltextindexed=True)
    keyword = String(fulltextindexed=True,
                     description=_('keyword or tag describing the Dataset'))
    landing_page = String(
        description=_('a web page that provides access to the dataset, its '
                      'distributions and/or additional information.'))
    provenance = String(fulltextindexed=True)  # Not in DCAT-AP spec.


class dataset_frequency(RelationDefinition):
    subject = 'Dataset'
    object = 'Concept'
    cardinality = '?*'
    inlined = True
    description = _('the frequency at which a dataset is updated')


class in_catalog(RelationDefinition):
    subject = 'Dataset'
    object = 'DataCatalog'
    cardinality = '?*'
    inlined = True
    description = _('relate a dataset to its associated catalog')


class of_dataset(RelationDefinition):
    subject = 'Distribution'
    object = 'Dataset'
    cardinality = '1*'
    composite = 'object'
    inlined = True
    description = _('relate a Distribution to its associated Dataset')


class dataset_contact_point(RelationDefinition):
    subject = 'Dataset'
    object = 'Agent'
    cardinality = '?*'
    description = _('contact information that can be used for flagging '
                    'errors in the Dataset or sending comments')


class dataset_publisher(RelationDefinition):
    subject = 'Dataset'
    object = 'Agent'
    cardinality = '?*'
    description = _('relate an entity (organization) responsible for making '
                    'the Dataset available')


class dataset_contributors(RelationDefinition):
    subject = 'Dataset'
    object = 'Agent'
    cardinality = '**'
    description = _('relate an entity (organization) responsible for making '
                    'contributions to the dataset')


class dcat_theme(RelationDefinition):
    subject = 'Dataset'
    object = 'Concept'
    constraints = [RQLConstraint('O in_scheme CS, S in_catalog C, C theme_taxonomy CS',
                                 msg=_("Theme must belong to a dataset's catalog vocabulary"))]


class LicenseDocument(EntityType):
    """A legal document giving official permission to do something with a
    Resource.
    """
    title = String(fulltextindexed=True, description=_("A short title for the license"))
    uri = String(description=_('URI where the license description can be found'))


class license_type(RelationDefinition):
    subject = 'LicenseDocument'
    object = 'Concept'
    cardinality = '1*'
    inlined = True


class license(RelationDefinition):
    subject = ('DataCatalog', 'Distribution')
    object = 'LicenseDocument'
    cardinality = '?*'
    inlined = True
    composite = 'subject'
    description = _('the licence under which the entity is made available')


@publication_metadata
class Distribution(EntityType):
    title = String(fulltextindexed=True)
    description = RichString(fulltextindexed=True)
    access_url = String(
        description=_('A URL that gives access to a distribution of the '
                      'dataset. The resource at the access URL may contain '
                      'information about how to get the Dataset.')
    )
    download_url = String(
        description=_('URL to directly download the distribution. '
                      '(Usually unspecified if the distribution is associated '
                      'with a file in the catalog.)')
    )
    byte_size = Int()


class distribution_media_type(RelationDefinition):
    subject = 'Distribution'
    object = 'Concept'
    cardinality = '?*'
    inlined = True
    description = _('The media type of the distribution as defined in the official register of '
                    'media types managed by IANA')


class distribution_format(RelationDefinition):
    subject = 'Distribution'
    object = 'Concept'
    cardinality = '?*'
    inlined = True
    description = _('The file format of the distribution')


class file_distribution(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': (RRQLExpression('U has_update_permission O'), ),
        'delete': (RRQLExpression('U has_update_permission O, '
                                  'NOT EXISTS(S produced_by R)'), ),
    }
    subject = 'File'
    object = 'Distribution'
    cardinality = '??'
    inlined = True
    composite = 'object'
    constraints = [
        RQLVocabularyConstraint('NOT EXISTS(SC implemented_by S)'),
    ]


class replaces(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': (
            RRQLExpression(
                'U has_update_permission O, NOT EXISTS(O produced_by P)'),
        ),
        'delete': (
            RRQLExpression(
                'U has_update_permission O, U has_update_permission S, '
                'NOT EXISTS(S produced_by P), NOT EXISTS(O produced_by P1)'),
        ),
    }
    subject = 'File'
    object = 'File'
    cardinality = '??'
    inlined = True


class ResourceFeed(EntityType):
    """A resource feed is associated to a dataset distribution. It regularly
    fetches files from the specified URL and attached them to this
    distribution.
    """
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'update': (
            'managers',
            ERQLExpression('X resource_feed_of D, U has_update_permission D')),
        'delete': (
            'managers',
            ERQLExpression('X resource_feed_of D, U has_update_permission D')),
        'add': ('managers', 'users')
    }
    title = String(
        description=_('this title will be used to set the title '
                      'of the associated distribution'))
    url = String(required=True)
    data_format = String(
        required=True, maxsize=128, default='text/plain',
        description=_('MIME type of files served by the resource feed.'))
    __unique_toguether__ = [('url', 'resource_feed_of')]


class resource_feed_of(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', RRQLExpression('U has_update_permission O')),
        'delete': ('managers', RRQLExpression('U has_update_permission O')),
    }
    subject = 'ResourceFeed'
    object = 'Dataset'
    cardinality = '1*'
    composite = 'object'
    inlined = True


class resourcefeed_distribution(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': (),
        'delete': (),
    }
    subject = 'ResourceFeed'
    object = 'Distribution'
    cardinality = '1*'
    inlined = True


class resource_feed_source(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': (),
        'delete': (),
    }
    subject = 'ResourceFeed'
    object = 'CWSource'
    cardinality = '1*'
    inlined = True
    # TODO a constraint checking compatibility of data_format between resource
    # feeds sharing the same CWSource.


SCRIPT_UPDATE_PERMS_RQLEXPR = (
    'NOT EXISTS(P1 process_script X) OR '
    'EXISTS(P2 process_script X, P2 in_state S,'
    '       S name "wfs_dataprocess_initialized")')


class Script(EntityType):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'update': ('managers', ERQLExpression(SCRIPT_UPDATE_PERMS_RQLEXPR)),
        'delete': ('managers', ERQLExpression(SCRIPT_UPDATE_PERMS_RQLEXPR)),
        'add': ('managers', 'users')
    }
    name = String(required=True, fulltextindexed=True)
    accepted_format = String(
        maxsize=128,
        description=_('the MIME type of input files that this script accepts '
                      '(if unspecified, the script is assumed to handle any '
                      'kind of format)'),
    )


class implemented_by(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': (RRQLExpression('U has_update_permission S'), ),
        'delete': (RRQLExpression('U has_update_permission S'), ),
    }
    subject = 'Script'
    object = 'File'
    cardinality = '1?'
    inlined = True
    composite = 'subject'
    description = _('the resource (file) implementing a script')
    constraints = [
        RQLVocabularyConstraint(
            'NOT EXISTS(O file_distribution DI, DI of_dataset D)'),
    ]


DATAPROCESS_UPDATE_PERMS_RQLEXPR = (
    'X in_state S, S name "wfs_dataprocess_initialized"')


class _DataProcess(WorkflowableEntityType):
    __abstract__ = True
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'update': (),
        'delete': ('managers',
                   ERQLExpression(DATAPROCESS_UPDATE_PERMS_RQLEXPR)),
        'add': ()
    }


class DataTransformationProcess(_DataProcess):
    """Data transformation process"""


class DataValidationProcess(_DataProcess):
    """Data validation process"""


class process_for_resourcefeed(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', RRQLExpression('U has_update_permission O')),
        'delete': ('managers', RRQLExpression('U has_update_permission O')),
    }
    subject = ('DataTransformationProcess', 'DataValidationProcess')
    object = 'ResourceFeed'
    cardinality = '?*'
    composite = 'object'


PROCESS_DEPENDS_ON_UPDATE_PERMS = (
    'managers', RRQLExpression(
        'NOT EXISTS(S process_for_resourcefeed RF1) '
        'OR (S process_for_resourcefeed RF, U has_update_permission RF)')
)


class process_depends_on(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': PROCESS_DEPENDS_ON_UPDATE_PERMS,
        'delete': PROCESS_DEPENDS_ON_UPDATE_PERMS,
    }
    subject = 'DataTransformationProcess'
    object = 'DataValidationProcess'
    cardinality = '??'
    constraints = [
        RQLConstraint(
            'NOT EXISTS(S process_for_resourcefeed RF1,'
            '           S process_for_resourcefeed RF2) '
            'OR EXISTS(S process_for_resourcefeed RF,'
            '          O process_for_resourcefeed RF)',
            msg=_('dependency between data process must be within the same '
                  'resource feed')),
    ]


class process_input_file(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', RRQLExpression(
            'S in_state ST, ST name "wfs_dataprocess_initialized"')),
        'delete': ('managers', RRQLExpression('U has_update_permission S'))}
    subject = ('DataTransformationProcess', 'DataValidationProcess')
    object = 'File'
    cardinality = '?*'
    description = _('input file of the data process')


class validated_by(RelationDefinition):
    """A File may be validated by a validation process"""
    __permissions__ = {'read': ('managers', 'users', 'guests'),
                       'add': (),
                       'delete': ()}
    subject = 'File'
    object = 'DataValidationProcess'
    cardinality = '**'


class produced_by(RelationDefinition):
    """A File may be produced by a transformation process"""
    __permissions__ = {'read': ('managers', 'users', 'guests'),
                       'add': (),
                       'delete': ()}
    subject = 'File'
    object = 'DataTransformationProcess'
    cardinality = '?*'


# Set File permissions:
#  * use `produced_by` relation to prevent modification of generated files
#  * use relative permissions on the Distribution which the file may be a resource
#    of
#  * bind the update permissions on the Script which uses the File as
#    implementation if any
_update_file_perms = ('managers', ERQLExpression(
    'NOT EXISTS(X produced_by Y), '
    'NOT EXISTS(X file_distribution D1)'
    ' OR EXISTS(X file_distribution D, U has_update_permission D), '
    'NOT EXISTS(S1 implemented_by X)'
    ' OR EXISTS(S implemented_by X, U has_update_permission S)'
))
File.__permissions__ = File.__permissions__.copy()
File.__permissions__.update({'update': _update_file_perms,
                             'delete': _update_file_perms})


class process_script(RelationDefinition):
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', 'users'),
        'delete': (RRQLExpression('U has_update_permission S'), )
    }
    subject = ('DataTransformationProcess', 'DataValidationProcess')
    object = 'Script'
    cardinality = '1*'
    inlined = True


class _resourcefeed_script(RelationDefinition):
    __abstract__ = True
    __permissions__ = {
        'read': ('managers', 'users', 'guests'),
        'add': ('managers', 'users'),
        'delete': (RRQLExpression('U has_update_permission S'), )
    }
    subject = 'ResourceFeed'
    object = 'Script'
    cardinality = '?*'
    inlined = True
    constraints = [
        RQLConstraint(
            'O accepted_format NULL OR (O accepted_format F, S data_format F)',
            msg=_('script does not handle resource feed data format')),
    ]


class validation_script(_resourcefeed_script):
    description = u'a Script used to validated files from this resource'


class transformation_script(_resourcefeed_script):
    description = u'a Script used to transform files from this resource'
