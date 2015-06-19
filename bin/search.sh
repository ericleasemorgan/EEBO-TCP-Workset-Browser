#!/bin/bash

# search.sh - given a one-word query and a "database", do a search and return it in plain text

# Eric Lease Morgan <emorgan@nd.edu>
# June 13, 2015 - first cut; based on HathiTrust work, but doesn't seem to sort correctly


# get input
QUERY=$1
NAME=$2

# sanity check
if [ -z $QUERY ] || [ -z $NAME ]; then

    echo "Usage: $0 <query> <name>"
    exit 1
    
fi

# do the work
./bin/search.py $QUERY $NAME | sort -t $'\t' -k17 -g -r | ./bin/transform-results2text.py

# done
exit
