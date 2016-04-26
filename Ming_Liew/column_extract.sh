#!/bin/bash

eCollection=( $(cut -d ',' -f2 Consumer_Complaints.csv ) )
printf "%s\n" "${eCollection[0]}"
