#!/bin/bash

## Run reduce_scatter scaling node

clear && LOG_LEVEL=info iscanner --runner nccl_tests_runner --runner_config /engshare/xiaodongma/iscanner_configs/reduce_scatter_scaling.json --scheduler slurm --scheduler_config /engshare/xiaodongma/iscanner_configs/reduce_scatter_scaling.json
