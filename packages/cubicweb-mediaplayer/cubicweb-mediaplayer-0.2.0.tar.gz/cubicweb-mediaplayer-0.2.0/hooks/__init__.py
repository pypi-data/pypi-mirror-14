# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-mediaplayer specific hooks and operations"""

from cubicweb import ObjectNotFound, validation_error
from cubicweb.predicates import is_instance
from cubicweb.server.hook import Hook, Operation, DataOperationMixIn

from cubes.mediaplayer.utils.media import probe_media, id3infos


def hook_implements(*etypes):
    return Hook.__select__ & is_instance(*etypes)


class SetMediaFormatHook(Hook):
    __regid__ = 'mediaplayer.media-format'
    __select__ = hook_implements('SoundFile', 'VideoFile')
    events = ('before_add_entity', 'before_update_entity',)

    def __call__(self):
        entity = self.entity
        if 'data' in entity.cw_edited:
            self.entity.set_format_and_encoding()
            meta = probe_media(entity.data)
            for attr, value in meta.iteritems():
                if hasattr(entity, attr):
                    entity.cw_edited[attr] = value

                    
class EnsurePerformerTaskHook(Hook):
    __regid__ = 'mediaplayer.celery.check_performer'
    __select__ = Hook.__select__ & is_instance('EncodingTask')
    events = ('before_add_entity',)

    def __call__(self):
        task = self.entity
        try:
            performer = self._cw.repo.vreg['encoder.performer'].select(task.operation)
        except ObjectNotFound:
            raise validation_error(task,
                                   {'operation': _('performer %s not found') % task.operation})


class UpdateMediaTitleHook(Hook):
    __regid__ = 'mediaplayer.update-media-title'
    __select__ = hook_implements('SoundFile', 'VideoFile')
    events = ('after_update_entity',)

    def __call__(self):
        entity = self.entity
        if 'title' not in entity.cw_edited:
            SetMediaTitleOp.get_instance(self._cw).add_data(entity.eid)


class SetMediaTitleOp(DataOperationMixIn, Operation):
    """ set video or audio title"""
    def precommit_event(self):
        for entity_eid in self.get_data():
            entity = self.cnx.entity_from_eid(entity_eid)
            try:
                infos = id3infos(entity)
                entity.cw_set(title=unicode(infos.title))
            except Exception, err:
                continue


class AddEncodeSoundHook(Hook):
    __regid__ = 'mediaplayer.encode-sound'
    __select__ = hook_implements('SoundFile')
    events = ('after_add_entity', 'after_update_entity')

    def __call__(self):
        if 'data' in self.entity.cw_edited:
            self._cw.create_entity(
                'EncodingTask',
                operation=u'mediaplayer.reencode_sound',
                target_media_entity=self.entity)


class AddEncodeVideoHook(Hook):
    __regid__ = 'mediaplayer.encode-video'
    __select__ = hook_implements('VideoFile')
    events = ('after_add_entity', 'after_update_entity')

    def __call__(self):
        if 'data' in self.entity.cw_edited:
            self._cw.create_entity(
                'EncodingTask',
                operation=u'mediaplayer.reencode_video',
                target_media_entity=self.entity)
