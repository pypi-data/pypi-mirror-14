#!/usr/bin/env python
# encoding: utf-8

import pandas as pd

'''
'''
class trec_res:

    def __init__(self):
        pass

    def read_res(self, filename, result_header=["metric", "query", "value"]):
        self.res_data = pd.read_csv(filename, sep="\s+", names=result_header)

'''
'''
class trec_qrel:
    def __init__(self):
        pass

    def read_qrel(self, filename, qrels_header=["query","q0","filename","rel"]):
        self.qrels_data = pd.read_csv(filename, sep="\s+", names=qrels_header)

'''
'''
class trec_run:
    def __init__(self):
        pass

    def read_run(self, filename, run_header=["query", "q0", "docid", "rank", "score", "system"]):
        self.run_data = pd.read_csv(filename, sep="\s+", names=run_header)


