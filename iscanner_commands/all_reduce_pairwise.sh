#!/bin/bash

## Run all_reduce pairwise node

clear && LOG_LEVEL=info iscanner --runner nccl_tests_runner --runner_config /engshare/xiaodongma/iscanner_configs/all_reduce_pairwise.json --scheduler slurm --scheduler_config /engshare/xiaodongma/iscanner_configs/all_reduce_pairwise.json
