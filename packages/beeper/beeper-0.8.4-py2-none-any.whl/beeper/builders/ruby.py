# -*- coding: utf-8 -*-

def build(conf):
    run('rm -rf $DATA_DIR && mkdir -p $DATA_DIR')
    run('bundle package --path $DATA_DIR')
