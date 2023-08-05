# coding: utf-8

from DepthProjector._shape import Obj

__author__ = 'kanairen'


def read_obj(file_path):
    """
    objファイルを読み込み、頂点情報、法線情報、面情報を取得
    :param file_path: ファイルパス
    :return: 頂点リスト、法線リスト、面リスト
    """
    # 10.41s/10000time(v=298,f=492)
    # vertices = []
    # normals = []
    # faces = []
    # with open(file_path) as f:
    #     while True:
    #         line = f.readline()
    #         if line == '':
    #             break
    #         items = line.strip().split()
    #         if len(items) == 0:
    #             continue
    #         if items[0] == 'v':
    #             vertices.append(list(map(float, items[1:])))
    #         elif items[0] == 'vn':
    #             normals.append(list(map(float, items[1:])))
    #         elif items[0] == 'f':
    #             faces.append(list(map(int, items[1:])))

    # 8.98s/10000time(v=298,f=492)
    with open(file_path) as f:
        lines = filter(lambda x: len(x) > 0,
                       [line.strip().split() for line in f.readlines()])
        vertices = [list(map(float, line[1:])) for line in lines if
                    line[0] == 'v']
        normals = [list(map(float, line[1:])) for line in lines if
                   line[0] == 'vn']

        def split_face_info(s):
            return [int(s) if s.isdigit() else None for s in s.split('/')]

        faces = [list(map(split_face_info, line[1:])) for line in lines if
                 line[0] == 'f']

    return Obj(vertices, normals, faces)
