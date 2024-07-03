#!/bin/bash

## Run reduce_scatter single node

clear && LOG_LEVEL=info iscanner --runner nccl_tests_runner --runner_config /engshare/xiaodongma/iscanner_configs/single_node_reduce_scatter.json --scheduler slurm --scheduler_config /engshare/xiaodongma/iscanner_configs/single_node_reduce_scatter.json
