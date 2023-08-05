# coding=utf-8


import os
import _config
import threading
import numpy as np

from _gl import GL
from _shape_io import read_obj

__author__ = 'kanairen'


class PerspectiveProjection(object):
    """
    perspective-projection
    """

    def __init__(self, theta_angle_range, phi_angle_range, r):
        self.gl = GL(r=r)

        self.theta_angle = None
        self.phi_angle = None

        self.gen_angle = self.__generate_angle(theta_angle_range,
                                               phi_angle_range)

        self.is_displayed_since_captured = True
        self.is_capture_called = False

    @staticmethod
    def __generate_angle(theta_angle_range, phi_angle_range):
        for t in xrange(*theta_angle_range):
            for p in xrange(*phi_angle_range):
                yield (t, p)

    def depth_image(self, shape_file_path, init_rotate, is_view_only=False):

        # 保存先フォルダがない場合、作成
        if not os.path.exists(_config.PATH_DEPTH_ARRAY):
            os.makedirs(_config.PATH_DEPTH_ARRAY)
        if not os.path.exists(_config.PATH_DEPTH_IMG):
            os.makedirs(_config.PATH_DEPTH_IMG)

        self.__set_shape(shape_file_path, init_rotate)

        if not is_view_only:
            self.gl.display_func = self.__on_display
            self.gl.idle_func = self.__on_idle

        self.gl.start()

    def __update(self):
        try:
            self.theta_angle, self.phi_angle = self.gen_angle.next()
        except StopIteration:
            self.gl.display_func = None
            self.gl.idle_func = None
            self.gl.finish()
            return

    def __set_shape(self, file_path, fix_rotate=None, is_centerized=True,
                    is_normalized=True):
        ext = os.path.splitext(file_path)[1]

        if ext == '.obj':

            # objファイル読み込み
            obj = read_obj(file_path)

            # モデル位置修正
            if is_centerized:
                obj.center()
            if is_normalized:
                obj.normal()
            if fix_rotate:
                assert isinstance(fix_rotate, tuple) and len(fix_rotate) == 3
                obj.rotate(fix_rotate)

        else:
            raise NotImplementedError(
                    'the extension of specified path is not supported.')

        self.gl.shape = obj

    def __on_display(self):
        if self.is_capture_called:
            self.__save()
            self.is_capture_called = False
            self.is_displayed_since_captured = True

    def __on_idle(self):
        if self.is_displayed_since_captured and self.gl.shape:
            self.is_displayed_since_captured = False
            self.__update()
            # 深度マップのキャプチャ
            threading.Thread(target=self.__capture).start()

    # 深度マップ取得
    def __capture(self):
        # カメラ位置を変更し、描画
        theta = self.theta_angle * np.pi / 180.
        phi = self.phi_angle * np.pi / 180.
        self.gl.camera_rotate(theta, phi)
        self.is_capture_called = True

    def __save(self):
        # 描画が完了したら保存
        file_name = 't{}_p{}'.format(self.theta_angle, self.phi_angle)
        self.gl.save_depthimage(file_name)
        self.gl.save_deptharray(file_name)
