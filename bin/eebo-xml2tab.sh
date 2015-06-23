#!/bin/bash

# xml2tab.sh - find all .xml files and pull out rudimentary metadata

# Eric Lease Morgan <emorgan@nd.edu>
# June 5, 2015 - first cut


# configure
XML2TAB='./bin/eebo-xml2tab.pl'
ROOT='xml'

# start the output
printf "id\tauthor\ttitle\tdate\tsubjects\tlanguage\tpagination\tpages\twords\tpublisher\n"

# find all xml files and do the work
find ./$ROOT -name '*.xml' -exec $XML2TAB {} \; 

# done
exit 0

