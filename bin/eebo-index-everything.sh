#!/bin/bash

# eebo-index-everything.sh - process each index

# Eric Lease Morgan <emorgan@nd.edu>
# June 14, 2015 - first investigations


# configure
SCRIPT='./bin/eebo-index-field.sh'
CATALOG='./eebo.db'
INDEXES=(authors titles dates subjects facets languages publishers)

# process each index
for INDEX in ${INDEXES[@]}; do

	echo "indexing $INDEX"
	cat $CATALOG | $SCRIPT $INDEX
	
done

# quit
exit 0
