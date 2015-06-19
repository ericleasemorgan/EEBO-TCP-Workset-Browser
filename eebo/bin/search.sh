#!/bin/bash

# eebo-search.sh - query the locally created EEBO catalog

# Eric Lease Morgan
# June 14, 2015 - first cut
# June 16, 2015 - moved indicies to etc


# configure
ETC='./etc'
CATALOG='./catalog.db'

# initialize
QUERY=$1
INDEX=$2

# parse the input into query and index parameters
#while true; do
#
#	# re-initialize
#	i=$1
#	shift
#
#	# check for end of input
#	if [ -z $i ]; then break
#
#	# check for index parameter
#	elif [ $i = "-i" ]; then
#
#		# denote INDEX
#		INDEX=$1
#		shift
#
#	# build the query
#	else QUERY="$QUERY $i"
#
#	fi
#	
#done

# check for specific index
if [ -z $INDEX ]; then
	
	# search the catalog; free text search
	grep -i "$QUERY" $CATALOG | sort
	
else

	# search a specific index
	grep -i "$QUERY" $ETC/index-$INDEX.idx | cut -f2 | sed s/,/"\n"/g | sort | uniq -u | while read R; do grep $R $CATALOG; done

fi

# done
exit 0
