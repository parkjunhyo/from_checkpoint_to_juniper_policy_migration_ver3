#! /usr/bin/env bash


# step1
./gen_network_objects.py

# step2
./gen_network_services.py

# step3
./gen_security_objects.py

# step4 : nat source
./gen_global_nat_source.py

# step5 : nat address
./gen_global_nat_address.py  

# step6
./renew_srcdst_policy.py

# step7
./renew_srv_policy.py

# step8
./confirm_renew_files.py

