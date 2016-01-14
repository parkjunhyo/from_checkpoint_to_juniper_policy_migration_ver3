ip_calc.sh

searching_network_objects.sh  

Data : this is orign file directory
       network_objects.data -> network object table
       destination.data     -> destination policy 
       service.data         -> service policy
       source.data          -> souce policy

Step 1. generate the completed netowrk object
        run "gen_network_objects.py" file to create "network_objects.gen"

Step 2. generate the completed policy rule
        run "gen_security_objects.py" file to create "source.gen", "destination.gen" and "service.gen"

Step 3. re-arrange full policy file
        run "renew_security_objects.py"
        

             
