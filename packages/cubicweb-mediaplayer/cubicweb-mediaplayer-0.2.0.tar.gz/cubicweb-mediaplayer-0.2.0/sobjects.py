# -*- coding: utf-8 -*-
# copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

import sys
import logging
import traceback

from six import StringIO

from cubicweb import ValidationError, Binary
from cubicweb.predicates import is_instance
from cubicweb.server.hook import Hook, Operation

from cubicweb_celery import app


logger = logging.getLogger('cubicweb')


class CeleryTaskOp(Operation):

    def postcommit_event(self):
        logging.warning('Operation launched %s', self.eid)
        return perform.delay(self.eid)


class NewTaskHook(Hook):
    __regid__ = 'mediaplayer.celery.new_task'
    __select__ = Hook.__select__ & is_instance('EncodingTask')
    events = ('after_add_entity',)

    def __call__(self):
        CeleryTaskOp(self._cw, eid=self.entity.eid)


@app.cwtask
def perform(self, task_eid):
    logger.error('performing Task %s', task_eid)
    task = self.cw_cnx.entity_from_eid(task_eid)
    adapted = task.cw_adapt_to('IWorkflowable')
    performer = self.app.cwrepo.vreg['encoder.performer'].select(task.operation)
    try:
        adapted.fire_transition('task_acquire')
        self.cw_cnx.commit()
    except ValidationError:
        logger.error('cannot acquire Task %s (state %s)',
                     task_eid, task.in_state[0].name)
        self.cw_cnx.rollback()
    else:
        _stdout, _stderr = sys.stdout, sys.stderr
        stdout = sys.stdout = StringIO()
        stderr = sys.stderr = StringIO()
        try:
            result = performer.perform_task(self.cw_cnx, task)
        except Exception as exc:
            self.cw_cnx.rollback()
            msg = u'unexpected: %s\n' % exc + traceback.format_exc()
            adapted.fire_transition('task_fail', msg)
        else:
            adapted.fire_transition('task_complete', result)
        finally:
            sys.stdout, sys.stderr = _stdout, _stderr
            task.cw_set(progress=1)
            self.cw_cnx.commit()
            task.cw_set(stdout=Binary(stdout.getvalue()))
            task.cw_set(stderr=Binary(stderr.getvalue()))
            self.cw_cnx.commit()


@app.cwtask
def check(self):
    logger.error('looking for waiting tasks')
    rql = 'EncodingTask T WHERE T in_state S, S name "task_pending"'
    for task_eid, in self.cw_cnx.execute(rql):
        logger.error('Found %s', task_eid)
        perform.delay(task_eid)
