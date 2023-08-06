# -*- coding: utf-8 -*-
import unittest

from logilab.common.testlib import tag, Tags
from cubicweb import Binary

from cubes.mediaplayer.testlib import MediaPlayerBaseTestCase
from cubes.mediaplayer.utils.media import id3infos, probe_media

class VideoFileTC(MediaPlayerBaseTestCase):

    @tag('meta')
    def test_file_meta(self):
        with self.admin_access.repo_cnx() as cnx:
            orig_data = probe_media(open(self.datapath('video.flv')))
            self.assertEqual(orig_data['width'], 352)
            self.assertEqual(orig_data['height'], 288)
            self.assertEqual(orig_data['audiodatarate'], 352800)
            self.assertEqual(orig_data['videodatarate'], 200000)
            self.assertEqual(orig_data['framerate'], 25)
            self.assertEqual(orig_data['length'], 5.015)

            video = self.add_video_file(cnx, self.datapath('video.flv'))
            cnx.commit()
            video.cw_clear_all_caches()
            self.assertEqual(video.width, 512)
            self.assertEqual(video.height, 418)
            self.assertEqual(video.length, 5)

    @tag('encode')
    def test_encode_flv_video(self):
        with self.admin_access.repo_cnx() as cnx:
            video = self.add_video_file(cnx, self.datapath('video.flv'))
            cnx.commit()
            video.cw_clear_all_caches()
            self.assertIsNotNone(video.data_mp4)
            self.assertEqual(video.data_mp4_format, u'video/mp4')
            self.assertIsNotNone(video.data_ogv)
            self.assertEqual(video.data_ogv_format, u'video/ogg')

    @tag('encode')
    def test_encode_task(self):
        with self.admin_access.repo_cnx() as cnx:
            video = self.add_video_file(cnx, self.datapath('video.flv'))
            cnx.commit()
        with self.admin_access.repo_cnx() as cnx:
            task = cnx.find('EncodingTask').one()
            self.assertEqual(1, task.progress)
            # ensure stdout has at least some expected content
            self.assertTrue(task.stdout)
            stdout = task.stdout.getvalue()
            self.assertTrue(stdout)
            self.assertIn('first pass encoding', stdout)
            self.assertIn('second pass encoding', stdout)
            # stderr should be empty there
            self.assertFalse(task.stderr)

    def test_idownloadable(self):
        with self.admin_access.repo_cnx() as cnx:
            video = self.add_video_file(cnx, self.datapath('video.flv'))
            cnx.commit()
            idownloadable = video.cw_adapt_to('IDownloadable')
            self.assertEqual(idownloadable.download_url(),
                             u'http://testing.fr/cubicweb/%s/%s/raw' % (
                             video.__regid__.lower(), video.eid))
            self.assertEqual(idownloadable.download_content_type(), 'video/x-flv')
            mpeg_adaptor = video.cw_adapt_to('MpegIDownloadable')
            self.assertEqual(mpeg_adaptor.download_url(),
                             u'http://testing.fr/cubicweb/%s/%s/mp4' % (
                             video.__regid__.lower(), video.eid))
            ogg_adaptor = video.cw_adapt_to('OggIDownloadable')
            self.assertEqual(ogg_adaptor.download_url(),
                             u'http://testing.fr/cubicweb/%s/%s/ogv' % (
                             video.__regid__.lower(), video.eid))

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.ERROR)
    main()
