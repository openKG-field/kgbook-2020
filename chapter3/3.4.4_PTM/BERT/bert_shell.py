#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@File     : bert_shell.py
@Time     : 2021/3/29 20:21
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


from bert_serving.server.helper import get_args_parser
from bert_serving.server import BertServer
args = get_args_parser().parse_args(['-model_dir', 'D:\\bert_model\\chinese_L-12_H-768_A-12',
                                     '-port', '5555',
                                     '-port_out', '5556',
                                     '-max_seq_len', '50',
                                     '-num_worker','3',
                                     '-mask_cls_sep',
                                     '-cpu'])
server = BertServer(args)
server.start()