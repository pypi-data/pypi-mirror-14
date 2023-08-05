# copyright 2011-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""cubicweb-vcreview primary views and adapters for the web ui"""

__docformat__ = "restructuredtext en"
_ = unicode

from difflib import unified_diff

from logilab.mtconverter import xml_escape

from cubicweb import tags
from cubicweb.predicates import score_entity, is_instance, one_line_rset
from cubicweb.view import EntityView, View
from cubicweb.web.views import tabs, ibreadcrumbs, uicfg

from cubes.vcsfile.views import primary as vcsfile
from cubes.vcreview.views import final_patch_states_rql
from cubes.vcreview.site_cubicweb import COMPONENT_CONTEXT

_pvs = uicfg.primaryview_section
_pvdc = uicfg.primaryview_display_ctrl
_abaa = uicfg.actionbox_appearsin_addmenu
_afs = uicfg.autoform_section


# patch primary view ###########################################################

_pvs.tag_subject_of(('Patch', 'patch_reviewer', '*'), 'attributes')
_pvs.tag_subject_of(('Patch', 'patch_committer', '*'), 'attributes')

class PatchPrimaryView(tabs.TabbedPrimaryView):
    """Main Patch primary view"""
    __select__ = is_instance('Patch')

    tabs = [_('vcreview.patch.tab_main'),
            _('vcreview.patch.tab_head'),
            _('vcreview.patch.revisions')]
    default_tab = 'vcreview.patch.tab_main'

    def render_entity_title(self, entity):
        self.w(u'<h1>%s <span class="state">[%s]</span></h1>'
               % (xml_escape(entity.dc_title()),
                  xml_escape(entity.cw_adapt_to('IWorkflowable').printable_state)))


class PatchPrimaryTab(tabs.PrimaryTab):
    """Summary tab for Patch"""
    __regid__ = 'vcreview.patch.tab_main'
    __select__ = is_instance('Patch')

    def render_entity_attributes(self, entity):
        super(PatchPrimaryTab, self).render_entity_attributes(entity)

class PatchHeadTab(EntityView):
    """Revision view of the tip most version of the patch

    (with comment and task)"""
    __regid__ = 'vcreview.patch.tab_head'
    __select__ = is_instance('Patch')

    def entity_call(self, entity):
        tip = entity.tip()
        if tip:
            tip.view('primary', w=self.w)


class PatchRevisions(EntityView):
    """A view that allow to view the diff between two revisions of the same
    patch.
    """
    __regid__ = 'vcreview.patch.revisions'
    __select__ = (is_instance('Patch')
                  & score_entity(lambda x: len(x.patch_revision) > 1))

    def entity_call(self, entity):
        w = self.w
        self._cw.add_css('cubes.vcreview.css')
        self._cw.add_js('cubes.vcreview.js')
        self._cw.add_css('pygments.css')
        w(tags.h4(self._cw._('Patch revisions')))
        w(u'<ul class="list-group">')
        parent_eid = entity.patch_revision[0].eid
        eids = []
        for i, rev in enumerate(entity.patch_revision):
            eids.append(rev.eid)
            w(u'<li class="list-group-item" id="rev-%s">' % rev.eid)
            w(rev.view('incontext'))
            if i != 0:
                w(u'<div class="pull-right">')
                w(u'<span title="%s">' % self._cw._('Diff'))
                w(u'<a class="icon-diff" href="#"><span class="icon-code"></span></a>')
                w(u'</span>')
                w(u'</div>')
            w(u'<div>')
            w(u'<span class="text-muted">%s %s %s %s' % (
                self._cw._('created on'), rev.printable_value('creation_date'),
                self._cw._('by'), rev.author))
            if rev.parent_revision:
                parent = rev.parent_revision[0]
                w(u' (%s %s)' % (self._cw.__('parent_revision'), parent.view('oneline')))
            w(u'</span>')
            w(u'</div>')
            w(u'</li>')
        w(u'</ul>')

        self._cw.add_onload(u'cw.cubes.vcreview.addClickTrigger(%s);' % eids)
        self.w(tags.div(klass='clear'))
        self.w(tags.div(id="diff-div", klass="content"))


class PatchRevisionsDiff(View):
    """A view that show a diff between two revisions.
    The revisions eid are found in the request parameters.
    The parameters are rev1 for the first revision and rev2
    for the second revision.
    """
    __regid__ = 'vcreview.patch.revisions_diff'
    templatable = False

    def call(self):
        form = self._cw.form
        if 'rev1' not in form or 'rev2' not in form:
            return
        rev1 = self._cw.entity_from_eid(form['rev1'])
        rev2 = self._cw.entity_from_eid(form['rev2'])
        transformer = rev1._cw_mtc_transform
        message_diff = self.get_message_diff(rev1, rev2)
        content_diff = self.get_content_diff(rev1, rev2)
        self.w(tags.h4(self._cw._('Diff')))
        self.w(tags.h5(self._cw._('Message')))
        self.write_diff(transformer, message_diff, self.w)
        self.w(tags.h5(self._cw._('Content')))
        self.write_diff(transformer, content_diff, self.w)

    def get_content_diff(self, rev1, rev2):
        """Return the diff between two revisions.

        :param Revision rev1: the first revision
        :param Revision rev2: the second revision
        """
        repo = rev1.from_repository[0]
        assert repo == rev2.from_repository[0]
        diff = self._cw.call_service(
            'vcsfile.export-rev-diff', repo_eid=repo.eid,
            rev1=rev1.changeset, rev2=rev2.changeset)
        return diff or u''

    @staticmethod
    def get_message_diff(rev1, rev2):
        """Return the diff between the commit messages of
        the two revisions. It return a diff in the `text/x-diff`
        format

        :param Revision rev1: the first revision
        :param Revision rev2: the second revision
        """
        message_one = rev1.description.split('\n')
        message_two = rev2.description.split('\n')
        first_message = rev1.view('shorttext')
        second_message = rev2.view('shorttext')
        diffcontent = unified_diff(
            message_one, message_two, fromfile=first_message,
            tofile=second_message, lineterm='')
        return u'\n'.join(diffcontent)

    def write_diff(self, transformer, diff, w):
        """Transform the diff which is supposed to be in format
        `text/x-diff` to the HTML format and write the result
        to the given writer.

        :param transformer: the transformer tu use to do the conversion
        :param diff: the diff
        :param w: the list to which to append the HTML content
        """
        if diff:
            html = transformer(diff, 'text/x-diff', 'text/html', 'utf8')
            w(html)
        else:
            w(tags.div(self._cw._('no diff'), klass='alert alert-warning'))


#_pvs.tag_object_of(('*', 'patch_revision', '*'), 'hidden') # in breadcrumbs

# repository primary view ######################################################

_pvs.tag_subject_of(('Repository', 'repository_committer', '*'), 'attributes')
_pvs.tag_subject_of(('Repository', 'repository_reviewer', '*'), 'attributes')


class RepositoryPatchesTab(EntityView):
    __regid__ = _('vcreview.patches_tab')
    __select__ = is_instance('Repository') & score_entity(lambda x: x.has_review)

    def entity_call(self, entity):
        entity.view('vcreview.repository.patches', w=self.w)

vcsfile.RepositoryPrimaryView.tabs.append(RepositoryPatchesTab.__regid__)


class RepositoryPatchesTable(EntityView):
    __regid__ = 'vcreview.repository.patches'
    __select__ = is_instance('Repository') & score_entity(lambda x: x.has_review)

    rql = ('Any P,P,P,P,PB,PS ' # XXX need a sub query to find patch tip
           'GROUPBY P,PB,PS '
           'WHERE '
           '      RE branch PB, '
           '      P in_state PS, '
           '      P patch_revision RE, '
           '      RE from_repository R, '
           '      R eid %(x)s')

    def entity_call(self, entity):
        linktitle = self._cw._('Patches for %s') % entity.dc_title()
        linkurl = self._cw.build_url(rql=self.rql % {'x': entity.eid},
                                     vtitle=linktitle)
        self.w('<p>%s. <a href="%s">%s</a></p>' % (
            self._cw._('Table below only show active patches'),
            xml_escape(linkurl), self._cw._('Show all patches')))
        rql = self.rql + ', NOT PS name %s' % final_patch_states_rql()
        rset = self._cw.execute(rql, {'x': entity.eid})
        self.wview('vcreview.patches.table.filtered', rset, 'noresult')

# task primary view ############################################################

_pvs.tag_object_of(('*', 'has_activity', 'Task'), 'attributes')

class InsertionPointInContextView(EntityView):
    __regid__ = 'incontext'
    __select__ = is_instance('InsertionPoint')
    def entity_call(self, entity):
        purl = entity.parent.absolute_url()
        url = '%s#%s%s' % (purl, COMPONENT_CONTEXT, entity.eid)
        self.w(u'<a href="%s">%s</a>' % (url, entity.parent.dc_title()))


# breadcrumbs ##################################################################

class PatchIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('Patch')

    def parent_entity(self):
        return self.entity.repository

class TaskBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = (is_instance('Task')
                  & score_entity(lambda x: x.reverse_has_activity))

    def parent_entity(self):
        return self.entity.reverse_has_activity[0]


class InsertionPointBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('InsertionPoint')

    def parent_entity(self):
        return self.entity.parent

    def breadcrumbs(self, view=None, recurs=None):
        path = super(InsertionPointBreadCrumbsAdapter, self).breadcrumbs(
            view, recurs)
        return [x for x in path if getattr(x, 'eid', None) != self.entity.eid]
