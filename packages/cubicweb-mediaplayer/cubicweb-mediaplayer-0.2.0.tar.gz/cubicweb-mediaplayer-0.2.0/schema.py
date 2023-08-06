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

"""cubicweb-mediaplayer schema"""

from yams.buildobjs import (EntityType, RichString, String, Float,
                            Bytes, Int, RelationType, RelationDefinition)
from yams.constraints import IntervalBoundConstraint
from cubicweb.schema import WorkflowableEntityType

_ = unicode


def FileBytes(**kwargs):
    meta = {
        'format': String(maxsize=50),
        'name': String(maxsize=255),
        }
    return Bytes(metadata=meta, **kwargs)


class SoundFile(EntityType):
    title = String(maxsize=256)
    data = FileBytes(required=True)
    data_encoding = String(
        maxsize=32,
        description=_('encoding of the file when it applies (e.g. text). '
                      'Should be dynamically set at upload time.'))
    description = RichString(internationalizable=True,
                             default_format='text/rest')
    # data_mpeg attribute is mandatory (for Safari)
    data_mp3 = FileBytes(required=False)
    # data_oga attribute is mandatory as FF do not read mp3
    data_oga = FileBytes(required=False)
    # data attributes
    length = Int(description=_('track length in secs'))


class VideoFile(EntityType):
    title = String(maxsize=256)
    data = FileBytes(required=True)
    data_encoding = String(
        maxsize=32,
        description=_('encoding of the file when it applies (e.g. text). '
                      'Should be dynamically set at upload time.'))
    description = RichString(internationalizable=True,
                             default_format='text/rest')
    # data_mpeg attribute is mandatory (for Safari)
    data_mp4 = FileBytes(required=False)
    data_ogv = FileBytes(required=False)
    data_webm = FileBytes(required=False)
    # data attributes
    length = Int(description=_('track length in secs'))
    # video attributes
    width = Int()  # compressed video width, not the original
    height = Int()  # compressed video height, not the original


# encoder tasks #######################################################

class EncodingTask(WorkflowableEntityType):
    __permissions__ = {'read': ('users', 'managers'),
                       'add': ('managers', 'users'),
                       'update': ('managers', 'users'),
                       'delete': ('managers', 'users'),
                       }

    stdout = Bytes()
    stderr = Bytes()

    operation = String(
        description="""'name' of the operation to be performed:

        A performer of __regid__ <operation> will be selected to
        execute the task.""",
        required=True)

    progress = Float(description=_('Between 0 and 1'),
                     default=0, required=True,
                     constraints=[IntervalBoundConstraint(minvalue=0, maxvalue=1)])

class poster_of(RelationType):
    subject = 'File'
    object = ('VideoFile')
    cardinality = '*?'


class target_media_entity(RelationDefinition):
    subject = 'EncodingTask'
    object = ('SoundFile', 'VideoFile')
    cardinality = '?*'
    inlined = True
    composite = 'object'
