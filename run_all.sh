#! /usr/bin/env bash


# step1
./match_zone_from_renew.py

# step2
./combine_match_all.py 

# step3
./combine_match_global_nat.py 

# step4
./get_static_nat.py


# step source
./create_command_for_source_nat_juniper.py

# step5
./upload_html.sh
