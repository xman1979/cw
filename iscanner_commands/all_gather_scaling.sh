#!/bin/bash

## Run all_gather scaling node

clear && LOG_LEVEL=info iscanner --runner nccl_tests_runner --runner_config /engshare/xiaodongma/iscanner_configs/all_gather_scaling.json --scheduler slurm --scheduler_config /engshare/xiaodongma/iscanner_configs/all_gather_scaling.json
