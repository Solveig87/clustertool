#!/bin/bash

if [ ! -d "clustered_data" ]; then
    mkdir clustered_data
fi
if [ ! -d "streamcharts" ]; then
    mkdir streamcharts
fi
if [ ! -d "motioncharts" ]; then
    mkdir motioncharts
fi

bash create_clusters.sh
bash create_graphs.sh