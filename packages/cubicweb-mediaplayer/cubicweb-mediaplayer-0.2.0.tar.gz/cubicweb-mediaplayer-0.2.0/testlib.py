# -*- coding: utf-8 -*-
import os.path as osp
import unittest2
import tempfile

from six import text_type

from logilab.common.testlib import tag, Tags
from cubicweb import Binary
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb_celery import app, init_repo

class MediaPlayerBaseTestCase(CubicWebTC):
    test_db_id = 'mediplayer-base'
    tags = CubicWebTC.tags | Tags('MP')

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        if self.config._cubes is None:
            self.config.init_cubes(self.config.expand_cubes(('mediaplayer', )))
        self.set_option('media-dir', self.tempdir)
        self.config._cubes = None # hack to avoid troubles in default setUp
        super(MediaPlayerBaseTestCase, self).setUp()
        app.cwrepo = init_repo(app.cwconfig)

    def add_sound(self, cnx, filepath, data_format=u'audio/mpeg', data_name=u''):
        with open(filepath, 'rb') as fobj:
            data = fobj.read()
        return cnx.create_entity('SoundFile',
                                 data=Binary(data),
                                 title=text_type(osp.basename(filepath)),
                                 data_name=text_type(osp.basename(filepath)),
                                 )

    def add_video_file(self, cnx, filepath, data_format=u'audio/mpeg', data_name=u''):
        with open(filepath, 'rb') as fobj:
            data = fobj.read()
        return cnx.create_entity('VideoFile',
                                 data=Binary(data),
                                 title=text_type(osp.basename(filepath)),
                                 data_name=text_type(osp.basename(filepath)),
                                 )


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.ERROR)
    unittest2.main()
