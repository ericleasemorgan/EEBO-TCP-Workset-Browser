#!/bin/bash

# make-corpus.sh - given a list of identifiers and a keyword, cache EEBO content and make it browsable

# Eric Lease Morgan <emorgan@nd.edu>
# June  8, 2015 - first cut; based on HathiTrust efforts
# June 13, 2015 - migrated off everything but actual build to make-everything.sh
# June 14, 2015 - get files from GitHub instead of locally
# June 15, 2015 - migrated of the XSLT transform


# configure
XML='./xml'
CMD="wget --no-verbose -O $XML/##OUTPUT## --no-check-certificate https://raw.githubusercontent.com/textcreationpartnership/##KEY##/master/##KEY##.xml"

# get input
NAME=$1

# sanity check; needs additional error checking
if [ -z $NAME ]; then

    echo "Usage: cat <identifiers> | $0 <name>"
    exit 1
    
fi

# build the directory structure
echo "creating directory structure"
if [ ! -d "$NAME" ];        then mkdir $NAME;        fi
if [ ! -d "$NAME/xml" ];    then mkdir $NAME/xml;    fi
if [ ! -d "$NAME/index" ];  then mkdir $NAME/index;  fi
if [ ! -d "$NAME/text" ];   then mkdir $NAME/text;   fi
if [ ! -d "$NAME/html" ];   then mkdir $NAME/html;   fi
if [ ! -d "$NAME/graphs" ]; then mkdir $NAME/graphs; fi

# change into the newly created collection
cd $NAME

# get and transform all the requested files
echo "getting files"
while read RECORD; do
	
	# get the identifier
	IDENTIFIER=$( echo "$RECORD" | cut -f1 )
	
	# check to see if the file was already retrieved
	if [ ! -f "$XML/$IDENTIFIER.xml" ]; then
	
		WGET=$( echo $CMD | sed "s/##KEY##/$IDENTIFIER/g")
		WGET=$( echo $WGET | sed "s/##OUTPUT##/$IDENTIFIER.xml/g")
		$WGET
		
	fi
			
done

# finished
exit 0

