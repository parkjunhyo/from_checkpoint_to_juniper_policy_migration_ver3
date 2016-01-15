#! /usr/bin/env bash


# step1
./gen_network_objects.py

# step2
./gen_network_services.py

# step3
./gen_security_objects.py

# step4
./renew_srcdst_policy.py

# step5
./renew_srv_policy.py

# step6
./confirm_renew_files.py

