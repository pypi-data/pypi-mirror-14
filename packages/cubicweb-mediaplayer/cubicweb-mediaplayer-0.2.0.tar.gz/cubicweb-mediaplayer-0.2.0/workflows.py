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

_ = unicode

def define_worker_task_workflow(add_workflow):
    wf = add_workflow('encoding_task', 'EncodingTask', default=True)
    pending = wf.add_state(_('task_pending'), initial=True)
    assigned = wf.add_state(_('task_assigned'))
    failed = wf.add_state(_('task_failed'))
    aborted = wf.add_state(_('task_aborted'))
    done = wf.add_state(_('task_done'))
    wf.add_transition(_('task_acquire'), (pending,), assigned)
    wf.add_transition(_('task_release'), (assigned, failed), pending)
    wf.add_transition(_('task_complete'), (assigned,), done)
    wf.add_transition(_('task_fail'), (assigned,), failed)
    wf.add_transition(_('task_abort'), (assigned,), aborted)
