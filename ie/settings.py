import os
from os import path

global ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
data_root = ROOT_DIR + '/data/'


def proj_relpath(*path_segs):
    u"""相对于项目根路径

    假设项目部署在 /home/work/code/cie/
    >>> proj_relpath('a', 'b', 'c')
    '/home/work/code/cie/a/b/c'
    """
    return path.join(ROOT_DIR, *path_segs)
