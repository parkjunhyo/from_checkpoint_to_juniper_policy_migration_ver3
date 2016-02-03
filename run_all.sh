#! /usr/bin/env bash


# step1
./Match_zone_from_network.py 

# step2
./combine_match_all.py 

# step3
./combine_match_global_nat.py 

# step4
./upload_html.sh
