#!/bin/bash

## Run all_gather single node

clear && LOG_LEVEL=info iscanner --runner nccl_tests_runner --runner_config /engshare/xiaodongma/iscanner_configs/single_node_all_gather.json --scheduler slurm --scheduler_config /engshare/xiaodongma/iscanner_configs/single_node_all_gather.json
