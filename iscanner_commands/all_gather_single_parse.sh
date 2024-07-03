#!/bin/bash

clear && LOG_LEVEL=info iscanner --parser nccl_tests_parser --parser_config /engshare/xiaodongma/iscanner_configs/single_node_all_gather.json --summarizer nccl_tests_summarizer --summarizer_config /engshare/xiaodongma/iscanner_configs/single_node_all_gather.json
