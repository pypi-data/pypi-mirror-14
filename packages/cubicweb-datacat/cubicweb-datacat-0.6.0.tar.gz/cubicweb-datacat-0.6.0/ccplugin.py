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
"""cubicweb-datacat command plugins"""

from __future__ import print_function

from logilab.common.shellutils import ProgressBar

from cubicweb.cwctl import CWCTL
from cubicweb.toolsutils import Command
from cubicweb.utils import admincnx

from cubes.datacat import cwsource_pull_data


class SyncSKOSSchemes(Command):
    """Synchronize SKOS schemes for a datacat instance.

    <instance>
      identifier of a datacat instance.

    """
    arguments = '<instance>'
    name = 'sync-schemes'
    min_args = 1
    max_args = 1

    def run(self, args):
        appid = args[0]
        with admincnx(appid) as cnx:
            rset = cnx.execute(
                'Any S ORDERBY X WHERE X is SKOSSource, X through_cw_source S')
            title = '-> synchronizing SKOS sources'
            pb = ProgressBar(len(rset), title=title)
            created, updated = set([]), set([])
            for eid, in rset:
                stats = cwsource_pull_data(cnx.repo, eid, raise_on_error=False)
                pb.update()
                created.update(stats['created'])
                updated.update(stats['updated'])
            print('\n   {0} created, {1} updated'.format(len(created), len(updated)))


CWCTL.register(SyncSKOSSchemes)
