#! /usr/bin/env bash


cp ../service.renew .
cp ../static_nat_address.txt .
cp ../text_type_result.txt .
cp ../destination.match_zone .
cp ../source.match_zone .
cp ../text_type_global_nat_result.txt .


# create object
./create_source_destination_object.py  

# create application object
./create_service_object.py          

# create policy
./create_juniper_policy_command.py  

# create static nat
./create_static_nat_from_publiczone.py  

# create source nat
./create_source_nat.py                 




