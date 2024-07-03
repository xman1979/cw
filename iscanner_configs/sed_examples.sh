1) sed -i 's/"additional_script_options":.*/"additional_script_options": "export PATH=$PATH:\/opt\/hpcx\/ompi\/bin\/\\nexport NCCL_ALGO=Ring\\nexport LD_LIBRARY_PATH=\/engshare\/akokolis\/custom_nccl_tests\/nccl\/build\/lib\/:LD_LIBRARY_PATH"/g' all_reduce_pairwise.json



2) sed -i 's/"nodelist":.*"/"nodelist": "h100-192-[009]"/g' *.json 

3)  tr '\n' ',' < hostlist.txt >  output.txt ## replace a change of line with a comma to get the list of nodes as a single line.
                                             ## Then run scontrol show hostlist to create the compressed nodelist
