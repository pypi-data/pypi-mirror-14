# -*- coding: utf-8 -*-
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

from logilab.mtconverter import xml_escape

from cubicweb.web.views.baseviews import OutOfContextView
from cubicweb.predicates import is_instance

class EncodingTaskOutOfContext(OutOfContextView):
    __select__ = OutOfContextView.__select__ & is_instance('EncodingTask')
    field_ea_div = (u'<div class="entity-attributes"><div>%(label)s</div>\n'
                    u'%(data)s</div>')

    def cell_call(self, row, col, **kw):
        _ = self._cw._
        entity = self.cw_rset.get_entity(row, col)
        self._cw.add_css('cubes.mediaplayer.encoder.css')
        div_classes = ['mediaplayer-encoder']
        state = entity.cw_adapt_to('IWorkflowable').state or 'task_pending'
        div_classes.append(state)
        w = self.w
        media = entity.target_media_entity[0]
        track = media.track
        w(u'<div>\n')
        if track:
            w(u'<h4>{0}</h4>\n'.format(_('Media')))
            for label, data in ((_('Order'), track.order),
                                (_(media.__regid__), media.dc_title()),):
                w(self.field_ea_div % {'label': label,
                                       'data': data})
        w(u'<div class="{klass}" title="{title}" id="{id}">\n'.format(
            klass=u' '.join(div_classes),
            title=state,
            id=u'js-cw-encoding-task-{0}'.format(entity.eid),))
        w(u'<div>\n')
        w(u'<label>{0}</label>\n'.format(_('Reencoding state')))
        w(u'</div>\n')
        
        if not entity.finished:
            self._cw.add_js(('cubicweb.htmlhelpers.js',
                             'cubicweb.ajax.js',
                             'cubes.mediaplayer.encoder.js',))
            self._cw.add_onload('cw.mediaplayer.autorefreshprogress("{0}");'.format(entity.eid))

            w(u'<span class="{klass}" onclick="{onclick}">&nbsp;</span>'.format(
                klass=u'glyphicon glyphicon-off',
                onclick=xml_escape(u'asyncRemoteExec("abort_task", {0});'.format(entity.eid)),
            ))
            
        advratio = entity.progress or 0
        w(u'<progress value="{value}" max="{max}">{percentage:.0f} %</progress>'.format(
            max=1, value=advratio, percentage=100 * advratio))
        self.wview('oneline', rset=entity.as_rset())
        self.w(self.field_ea_div % {'label': _('reencoding date'),
                                    'data': entity.printable_value('creation_date')})
        w(u'</div>\n')
        w(u'</div>\n')
 
