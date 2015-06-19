#!/usr/bin/env python

# catalog2html.py - given the name of a corpus, output a human-readable version of the corpus's catalog

# Eric Lease Morgan <emorgan@nd.edu>
# June 11, 2015 - first investigations; based on HathiTrust work
# June 13, 2015 - added pages


# configure
CATALOG  = '/catalog.db'
HASH     = '''{ "id": "##ID##", "shortTitle": "##SHORTTITLE##", "title": "##TITLE##", "author": "##AUTHOR##", "date": "##DATE##", "language": "##LANGUAGE##", "pagination": "##PAGINATION##", "pages": "##PAGES##", "publisher": "##PUBLISHER##", "subjects": "##SUBJECTS##", "tei": "##TEI##", "html": "##HTML##", "text": "##TEXT##", "words": "##WORDS##", "colors": "##COLORS##", "names": "##NAMES##", "ideas": "##IDEAS##" }, '''
TEMPLATE = './etc/template-catalog.txt'
LENGTH   = 50

# require
import sys
import re

# sanity check
if len( sys.argv ) != 2 :
	print "Usage:", sys.argv[ 0 ], '<name>'
	quit()

# get input
name = sys.argv[ 1 ]

# open the database
data  = ''
with open( name + CATALOG ) as database :

	# initialize
	index = 0

	# process each record
	for record in database :

		# increment and re-initialize
		index += 1
		hash  =  HASH
		
		# read a record, and split it into fields
		fields = record.rstrip().split( '\t' )
		
		# check for header
		if index == 1 : continue
		
		# process the data
		else :
		
			# do the substitutions
			hash = re.sub( '##ID##',         fields[ 0 ],  hash )
			
			title = re.sub( '\"', '\\"',      fields[ 1 ] )
			hash  = re.sub( '##SHORTTITLE##', title[:LENGTH] + '...',  hash )
			hash  = re.sub( '##TITLE##',      title,        hash )
			
			hash  = re.sub( '##AUTHOR##',     fields[  2 ], hash )
			hash  = re.sub( '##DATE##',       fields[  3 ], hash )
			hash  = re.sub( '##LANGUAGE##',   fields[  4 ], hash )
			hash  = re.sub( '##PAGINATION##', fields[  5 ], hash )
			hash  = re.sub( '##PAGES##',      fields[  6 ], hash )
			hash  = re.sub( '##PUBLISHER##',  fields[  7 ], hash )
			hash  = re.sub( '##SUBJECTS##',   fields[  8 ], hash )
			hash  = re.sub( '##TEI##',        fields[  9 ], hash )
			hash  = re.sub( '##HTML##',       fields[ 10 ], hash )
			hash  = re.sub( '##TEXT##',       fields[ 11 ], hash )
			hash  = re.sub( '##WORDS##',      fields[ 12 ], hash )
			hash  = re.sub( '##COLORS##',     fields[ 13 ], hash )
			hash  = re.sub( '##NAMES##',      fields[ 14 ], hash )
			hash  = re.sub( '##IDEAS##',      fields[ 15 ], hash )
			
		# update the data
		data += hash
		
# create the html; do the substitutions
with open ( TEMPLATE ) as HTML : html = HTML.read()
html = re.sub( '##TITLE##', name, html )
html = re.sub( '##DATA##',  data, html )

# output and done
print html
quit()


