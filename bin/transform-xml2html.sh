#!/bin/bash

# transform-xml2html.sh - make TEI files (more) human readable

# Eric Lease Morgan <emorgan@nd.edu>
# June 15, 2015 - first investigations; forked off from make-corpus.sh


# configure
HTML='html'
JAR='./etc/saxon9he.jar'
XML='xml'
XSL='./etc/xsl/html5/html5.xsl'

# get input
NAME=$1

# sanity check
if [ -z $NAME ]; then

    echo "Usage: $0 <name>"
    exit 1
    
fi

# process each json file in the given directory
echo "transforming TEI into HTML"
for SOURCE in $NAME/$XML/*.xml
do
        
    # build name of the HTML output file
    KEY=$( basename "$SOURCE" .xml )
	INPUT="$NAME/$XML/$KEY.xml"
	OUTPUT="$NAME/$HTML/$KEY.html"
		
	# check to make sure the work has not already been done
	if [ ! -f "$OUTPUT" ]; then
	
		# do the work
		echo "Transforming $INPUT to $OUTPUT"
		java -cp $JAR net.sf.saxon.Transform -s:$SOURCE -xsl:$XSL -o:$OUTPUT
	
	fi
		
done

# quit
exit 0
