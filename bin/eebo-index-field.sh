#!/bin/bash

# eebo-index-field.sh - parse out a field from the local catalog of EEBO metadata, and have it indexed

# Eric Lease Morgan <emorgan@nd.edu>
# June 14, 2015 - first investigations


# configure
SCRIPT='./bin/eebo-index-field.pl'
ETC='./etc'
ROOT='eebo-index'

# remember, the structure of the "catalog" is:
#  1 - id
#  2 - author
#  3 - title
#  4 - date
#  5 - subjects
#  6 - language
#  7 - pagination
#  8 - pages
#  9 - words
# 10 - publisher

# map the input to a column in the catalog
if   [ $1 = 'authors' ];    then FIELD=2
elif [ $1 = 'titles' ];     then FIELD=3
elif [ $1 = 'dates' ];      then FIELD=4
elif [ $1 = 'subjects' ];   then FIELD=5
elif [ $1 = 'facets' ];     then FIELD=5
elif [ $1 = 'languages' ];  then FIELD=6
elif [ $1 = 'publishers' ]; then FIELD=10
else echo "Usage: cat <eebo.db> | $0 <authors|titles|dates|subjects|facets|languages|publishers>"; exit 1
fi

# parse out the requested data and do the work
cat /dev/stdin | sed '1d' - | cut -f1,$FIELD | $SCRIPT $1 > "$ETC/$ROOT-$1.idx"

# done
exit 0
