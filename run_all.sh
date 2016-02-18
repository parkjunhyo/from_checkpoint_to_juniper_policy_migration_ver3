#! /usr/bin/env bash


# step1
./Match_zone_from_network.py 

# step2
./combine_match_all.py 

# step3
./combine_match_global_nat.py 

# step4
./get_static_nat.py

# step command
./create_command_for_juniper_policy.py

# step nat
./create_command_for_static_nat_juniper.py

# step5
./upload_html.sh
