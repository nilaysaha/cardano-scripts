#!/bin/sh

curl -s localhost:12798/metrics | grep cardano_node_metrics_blocksForgedNum_int
