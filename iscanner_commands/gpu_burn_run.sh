#!/bin/bash

## Run gpu burn

clear && LOG_LEVEL=info iscanner --runner gpu_burn_runner --runner_config /engshare/xiaodongma/iscanner_configs/gpu_burn_config.json --scheduler slurm --scheduler_config /engshare/xiaodongma/iscanner_configs/gpu_burn_config.json
