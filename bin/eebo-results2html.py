#!/usr/bin/env python

# results2html.py - given standard input, output an HTML table of search results

# Eric Lease Morgan <emorgan@nd.edu>
# June  7, 2015 - first cut for EEBO
# June 16, 2015 - pointed to xml on GitHub; removed pointer to local html; hmmm...
# June 22, 2015 - moved to the root of the distribution


# configure
HASH     = '''{ "id": "##ID##", "shortTitle": "##SHORTTITLE##", "title": "##TITLE##", "author": "##AUTHOR##", "date": "##DATE##", "subjects": "##SUBJECTS##", "language": "##LANGUAGE##", "pages": "##PAGES##", "publisher": "##PUBLISHER##", "words": "##WORDS##", "xml": "##XML##" }, '''
TEMPLATE = './etc/eebo-template-search-results.txt'
XMLROOT  = 'https://github.com/textcreationpartnership/'

# require
import sys
import re

# sanity check
if ( len( sys.argv ) != 2 ) | ( sys.stdin.isatty() ) :
	print "cat <results> | " + sys.argv[ 0 ] + ' <query>'
	quit()

# get input
name = sys.argv[ 1 ]

# initialize
data = ''

# process each record
for hit in sys.stdin:

	# re-initialize
	hash = HASH
	
	# read a record with the following strucxture:
	#   0 - id
	#   1 - author
	#   2 - title
	#   3 - date
	#   4 - subjects
	#   5 - language
	#   6 - pagination
	#   7 - pages
	#   8 - words
	#   9 - publisher
	fields = hit.rstrip().split( '\t' )
		
	# do the substitutions
	hash = re.sub( '##ID##',         fields[ 0 ],  hash )
	title = re.sub( '\"', '\\"',     fields[ 2 ] )
	hash = re.sub( '##SHORTTITLE##', title[:50] + '...',  hash )
	hash = re.sub( '##TITLE##',      title,  hash )
	hash = re.sub( '##AUTHOR##',     fields[ 1 ],  hash )
	hash = re.sub( '##DATE##',       fields[ 3 ],  hash )
	hash = re.sub( '##PAGINATION##', fields[ 6 ],  hash )
	hash = re.sub( '##PAGES##',      fields[ 7 ],  hash )
	hash = re.sub( '##WORDS##',      fields[ 8 ],  hash )
	hash = re.sub( '##LANGUAGE##',   fields[ 5 ],  hash )
	hash = re.sub( '##SUBJECTS##',   fields[ 4 ],  hash )
	hash = re.sub( '##PUBLISHER##',  fields[ 9 ],  hash )

	# calculate xml filename, and then do the substitution
	hash = re.sub( '##XML##',  XMLROOT + fields[ 0 ],  hash )

	# update the data
	data += hash

# create the html; do the substitutions
with open ( TEMPLATE ) as HTML : html = HTML.read()
html = re.sub( '##TITLE##', name, html )
html = re.sub( '##DATA##',  data, html )

# output and done
print html
quit()


