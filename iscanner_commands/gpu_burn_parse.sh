#!/bin/bash

clear && LOG_LEVEL=info iscanner --parser gpu_burn_parser --parser_config /engshare/xiaodongma/iscanner_configs/gpu_burn_config.json --summarizer gpu_burn_summarizer --summarizer_config /engshare/xiaodongma/iscanner_configs/gpu_burn_config.json
