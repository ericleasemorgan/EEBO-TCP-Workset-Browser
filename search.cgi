#!/bin/bash

# eebo-search.cgi - rudimentary query interface to the eebo corpus

# Eric Lease Morgan <emorgan@nd.edu>
# June 16, 2015 - first cut; based on HathiTrust work
# June 17, 2015 - added options for output


# configure
TEMPLATE='./etc/eebo-template-search.txt'
SEARCH='./bin/eebo-search.sh'
RESULTS='./bin/eebo-results2html.py'

# check for no input; display input form
if [ -z "$QUERY_STRING" ]; then
	
		# print the magic lines
		echo "Content-type: text/html"
		echo

		# output the search form
		cat $TEMPLATE
		
# process the query
else
	
	# get the input; do error checking here!!!
	QUERY=$(  echo "$QUERY_STRING" | sed -n 's/^.*q=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" )
	INDEX=$(  echo "$QUERY_STRING" | sed -n 's/^.*i=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" )
	OUTPUT=$( echo "$QUERY_STRING" | sed -n 's/^.*o=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" )
		
	# html output
	if [ $OUTPUT = 'h' ]; then
	
		# print the magic lines
		echo "Content-type: text/html"
		echo

		# do the work
		$SEARCH $QUERY $INDEX | $RESULTS $QUERY
		
	# only identifiers
	elif [ $OUTPUT = 'i' ]; then
	
		# print the magic lines
		echo "Content-type: text/plain"
		echo
		
		# do the work		
		$SEARCH $QUERY $INDEX | cut -f1

	# error; unknown input
	else
	
		# print the magic lines
		echo "Content-type: text/plain"
		echo

		# do the work
		echo "Unknown value for output ($OUTPUT). Call Eric."

	fi

fi

# done
exit 0
