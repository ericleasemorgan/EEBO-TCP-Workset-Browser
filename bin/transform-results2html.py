#!/usr/bin/env python

# results2html.py - given standard input, output an HTML table of search results

# Eric Lease Morgan <emorgan@nd.edu>
# June 13, 2015 - first cut; based on HathiTrust work


# configure
HASH     = '''{ "id": "##ID##", "shortTitle": "##SHORTTITLE##", "title": "##TITLE##", "author": "##AUTHOR##", "date": "##DATE##", "language": "##LANGUAGE##", "pagination": "##PAGINATION##", "pages": "##PAGES##", "publisher": "##PUBLISHER##", "subjects": "##SUBJECTS##", "tei": "##TEI##", "html": "##HTML##", "text": "##TEXT##", "words": "##WORDS##", "colors": "##COLORS##", "names": "##NAMES##", "ideas": "##IDEAS##", "count": "##COUNT##", "tfidf": "##TFIDF##" }, '''
TEMPLATE = './etc/template-search-results.txt'

# require
import sys
import re

# sanity check
if ( len( sys.argv ) != 2 ) | ( sys.stdin.isatty() ) :
	print "Usage: ./bin/search.py <query> <name> | " + sys.argv[ 0 ] + ' <name>'
	quit()

# get input
name = sys.argv[ 1 ]

# initialize
data = ''

# process each record
for hit in sys.stdin:

	# re-initialize
	hash = HASH
	
	# parse the record into fields; the stream should have the following structure
	#   0 - ids
	#   1 - titles
	#   2 - authors
	#   3 - dates
	#   4 - languages
	#   5 - pagination
	#   6 - pages
	#   7 - publishers
	#   8 - subjects
	#   9 - tei
	#  10 - html
	#  11 - plaintext
	#  12 - words
	#  13 - colors
	#  14 - names
	#  15 - ideas
	#  16 - count
	#  17 - tfidf
	fields = hit.rstrip().split( '\t' )
		
	# do the substitutions
	hash = re.sub( '##ID##',         fields[  0 ],  hash )
	
	title = re.sub( '\"', '\\"',     fields[  1 ] )
	hash = re.sub( '##SHORTTITLE##', title[:50] + '...',  hash )
	hash = re.sub( '##TITLE##',      title,  hash )
	
	hash = re.sub( '##AUTHOR##',     fields[  2 ],  hash )
	hash = re.sub( '##DATE##',       fields[  3 ],  hash )
	hash = re.sub( '##LANGUAGE##',   fields[  4 ],  hash )
	hash = re.sub( '##PAGINATION##', fields[  5 ],  hash )
	hash = re.sub( '##PAGES##',      fields[  6 ],  hash )
	hash = re.sub( '##PUBLISHER##',  fields[  7 ],  hash )
	hash = re.sub( '##SUBJECTS##',   fields[  8 ],  hash )
	hash = re.sub( '##TEI##',        fields[  9 ],  hash )
	hash = re.sub( '##HTML##',       fields[ 10 ],  hash )
	hash = re.sub( '##TEXT##',       fields[ 11 ],  hash )
	hash = re.sub( '##WORDS##',      fields[ 12 ],  hash )
	hash = re.sub( '##COLORS##',     fields[ 13 ],  hash )
	hash = re.sub( '##NAMES##',      fields[ 14 ],  hash )
	hash = re.sub( '##IDEAS##',      fields[ 15 ],  hash )
	hash = re.sub( '##COUNT##',      fields[ 16 ],  hash )
	hash = re.sub( '##TFIDF##',      fields[ 17 ],  hash )
		
	# update the data
	data += hash

# create the html; do the substitutions
with open ( TEMPLATE ) as HTML : html = HTML.read()
html = re.sub( '##TITLE##', name, html )
html = re.sub( '##DATA##',  data, html )

# output and done
print html
quit()


