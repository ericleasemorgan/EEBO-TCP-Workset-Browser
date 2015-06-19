#!/bin/bash

# make-index.sh - create frequency files from the contents of a directory

# Eric Lease Morgan <emorgan@nd.edu>
# June 8, 2015 - first investigations; bases on HathiTrust work

# configure
XML2FREQUENCY=./bin/make-index.py

# get input
NAME=$1

# sanity check
if [ -z $NAME ]; then

    echo "Usage: $0 <name>"
    exit 1
    
fi

# process each json file in the given directory
echo "indexing and building text files"
for FILE in $NAME/xml/*.xml
do
    
    # parse out the KEY and echo
    KEY=$( basename $FILE .xml )
		
	# index
	if [ ! -f "$NAME/index/$KEY.db" ]; then
	
		echo "building $NAME/index/$KEY.db"
		cat $FILE | $XML2FREQUENCY -d > $NAME/index/$KEY.db
	
	fi
	
	# create "book"
	if [ ! -f "$NAME/text/$KEY.txt" ]; then
	
		echo "building $NAME/text/$KEY.txt"
		cat $FILE | $XML2FREQUENCY -b > $NAME/text/$KEY.txt
		
	fi
	
done
