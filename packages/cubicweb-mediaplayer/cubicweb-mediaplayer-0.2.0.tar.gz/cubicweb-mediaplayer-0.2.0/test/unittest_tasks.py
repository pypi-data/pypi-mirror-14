# copyright 2012-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-mediaplayer (encoding) tasks tests"""

from cubicweb import ValidationError
from cubes.mediaplayer.testlib import MediaPlayerBaseTestCase

class DefaultTC(MediaPlayerBaseTestCase):

    def test_bogus_operation(self):
        with self.admin_access.repo_cnx() as cnx:
            with self.assertRaises(ValidationError):
                cnx.create_entity('EncodingTask', operation=u'noop')
                cnx.commit()

    def test_work_is_done(self):
        with self.admin_access.repo_cnx() as cnx:
            orig_task = cnx.create_entity('EncodingTask',
                                          operation=u'test_operation',
                                          test_val=0)
            cnx.commit()
            task = cnx.find('EncodingTask', eid=orig_task.eid).one()
            state = task.cw_adapt_to('IWorkflowable').state
            self.assertEqual('task_done', state)
            self.assertEqual(task.test_val, 1)

    def test_task_are_acquired(self):
        with self.admin_access.repo_cnx() as cnx:
            task1 = cnx.create_entity('EncodingTask',
                                      operation=u'test_operation',
                                      test_val=0)
            task2 = cnx.create_entity('EncodingTask',
                                      operation=u'test_operation',
                                      test_val=0)
            cnx.commit()

            done_tasks = cnx.execute('EncodingTask T WHERE T in_state S, '
                                     'S name "task_done"')
            self.assertEqual(2, len(done_tasks))


    def test_failure(self):
        with self.admin_access.repo_cnx() as cnx:
            task_orig = cnx.create_entity('EncodingTask',
                                          operation=u'fail_validation',
                                          test_val=0)
            cnx.commit()

            task = cnx.find('EncodingTask', eid=task_orig.eid).one()
            task.cw_clear_all_caches()
            wfable = task.cw_adapt_to('IWorkflowable')
            self.assertEqual('task_failed', wfable.state)
            comment = wfable.latest_trinfo().comment
            self.assertIn(u"    raise Exception('kaboom')", comment)


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
