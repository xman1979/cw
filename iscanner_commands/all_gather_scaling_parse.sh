#!/bin/bash

clear && LOG_LEVEL=info iscanner --parser nccl_tests_parser --parser_config /engshare/xiaodongma/iscanner_configs/all_gather_scaling.json --summarizer nccl_tests_summarizer --summarizer_config /engshare/xiaodongma/iscanner_configs/all_gather_scaling.json
