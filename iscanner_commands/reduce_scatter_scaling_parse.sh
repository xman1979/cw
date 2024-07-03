#!/bin/bash

clear && LOG_LEVEL=info iscanner --parser nccl_tests_parser --parser_config /engshare/xiaodongma/iscanner_configs/reduce_scatter_scaling.json --summarizer nccl_tests_summarizer --summarizer_config /engshare/xiaodongma/iscanner_configs/reduce_scatter_scaling.json
