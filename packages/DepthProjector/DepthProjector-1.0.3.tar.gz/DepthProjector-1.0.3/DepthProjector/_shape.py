# coding=utf-8

import numpy as np
import warnings

__author__ = 'kanairen'


class Shape(object):
    """
    三次元形状クラス
    """

    def __init__(self, vertices):
        self.vertices = np.array(vertices)

    def center(self):
        """
        頂点座標をセンタライズする
        """
        if self.vertices is None:
            warnings.warn(
                    '{} : vertices is not exists.'.format(
                            self.__class__.__name__))
            return
        self.vertices -= self.vertices.mean(axis=0)

    def normal(self):
        """
        頂点座標を正規化する
        :return:
        """
        if self.vertices is None:
            warnings.warn(
                    '{} : vertices is not exists.'.format(
                            self.__class__.__name__))
            return
        self.vertices /= self.vertices.max()

    def rotate(self, r, rotate_priority=[0, 1, 2]):
        """
        頂点座標を三軸まわりに回転する
        :param r: 各軸の回転角 (rx,ry,rz)
        :param rotate_priority: 優先される回転軸 (px,py,pz) 小さい番号の軸から回転
        Note : rotate_priorityは添字なので、list型とする
        """
        assert len(r) == 3
        assert set(rotate_priority) == set([0, 1, 2])

        r_x, r_y, r_z = np.asarray(r, dtype=np.float32) / 180. * np.pi

        mtr_x = np.array([[1., 0., 0.],
                          [0., np.cos(r_x), np.sin(r_x)],
                          [0., -np.sin(r_x), np.cos(r_x)]])
        mtr_y = np.array([[np.cos(r_y), 0., -np.sin(r_y)],
                          [0., 1., 0.],
                          [np.sin(r_y), 0., np.cos(r_y)]])
        mtr_z = np.array([[np.cos(r_z), np.sin(r_z), 0.],
                          [-np.sin(r_z), np.cos(r_z), 0.],
                          [0., 0., 1.]])

        mtr_a, mtr_b, mtr_c = np.array((mtr_x, mtr_y, mtr_z))[rotate_priority]

        self.vertices = np.dot(np.dot(np.dot(self.vertices, mtr_a), mtr_b),
                               mtr_c)

    def __str__(self):
        s = [self.__class__.__name__ + ":",
             "vertices:" + str(len(self.vertices))]
        return "\n".join(s)


class Obj(Shape):
    """
    Objファイルから読み込んだ三次元形状クラス
    """

    DEFAULT_MODEL_COLOR = (0.5, 0.5, 0.5)

    def __init__(self, vertices, normals, faces, colors=None):
        super(Obj, self).__init__(vertices)
        self.normals = normals
        self.faces = faces
        if colors is None:
            colors = [self.DEFAULT_MODEL_COLOR] * len(faces)
        self.colors = colors

    def __str__(self):
        s = [super(Obj, self).__str__(),
             "normals:" + str(len(self.normals)),
             "faces:" + str(len(self.faces)),
             "colors:" + str(len(self.colors))]
        return "\n".join(s)
