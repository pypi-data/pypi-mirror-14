#!/bin/bash
set -e
set -x

pg tutorial00_basics

pg tutorial01_signals

pg tutorial03_config in=coastguard.mp4 out=coastguard03.avi

pg tutorial04_models in=coastguard.mp4 out=coastguard04.avi
 
pg tutorial05_config_advanced  in=coastguard.mp4 out=coastguard05.avi levels=8

pg tutorial06_signals_advanced 

pg tutorial07_simple_blocks

pg tutorial08_simple_blocks_conf

pg tutorial09_best_practices

pg tutorial10_stateful_blocks







