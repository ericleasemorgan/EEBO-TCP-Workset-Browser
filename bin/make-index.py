#!/usr/bin/env python

# make-index.py - read EEBO TEI files and output word frequencies as well as a "book"

# Eric Lease Morgan <emorgan@nd.edu>
# June 8, 2015 - first investigations; bases on HathiTrust work


# configure
STOPWORDS = './etc/stopwords-en.txt'

# require
import operator
import re
import sys
import libxml2

# sanity check
if ( len( sys.argv ) != 2 ) | ( sys.stdin.isatty() ) :
	print "Usage: cat <xml> |", sys.argv[ 0 ], '<-b|-d>'
	quit()

# get input; sanity check
flag = sys.argv[ 1 ]

# build a book?
if   flag == '-b' : build_book = 1
elif flag == '-d' : build_book = 0
else :
	print "Usage: cat <xml> |", sys.argv[ 0 ], '<-b|-d>'
	quit()

# create an xpath parser with an xml file
xml     = sys.stdin.read()
tei     = libxml2.parseMemory( xml, len( xml ) )
context = tei.xpathNewContext()
context.xpathRegisterNs( 't', 'http://www.tei-c.org/ns/1.0' )

# parse
title = context.xpathEval( '/t:TEI/t:teiHeader/t:fileDesc/t:titleStmt/t:title/text()' )[ 0 ]
text  = context.xpathEval( '/t:TEI/t:text' )[ 0 ].content

# normalize the text
text = re.sub( '\s+', ' ', text )
text = text.lower()
text = text.split()

# initialize output
words = {}
book  = str( title ) + '\n'

# create a list of (English) stopwords
stopwords = {}
with open ( STOPWORDS ) as DATABASE :
	for record in DATABASE : stopwords[ record.rstrip() ] = 1

# process each word in the text
for word in text :
		
	# normalize some more; probably not 100% accurate
	word = word.rstrip( '?:!.,;)' )
	word = word.lstrip( '?:!.,;(' )
	
	# filter out unwanted words
	if len( word ) < 2           : continue
	if re.match( '\d|\W', word ) : continue
	if word in stopwords         : continue
	
	# build text file
	if build_book : book = book + word + ' ' 
		
	# or update the dictionary
	else : words[ word ] = words.get( word, 0 ) + 1
	
# output book, or
if build_book : print book

# output the dictionary
else :
	for tuple in sorted( words.items(), key=operator.itemgetter( 1 ), reverse=True ) :
		print( tuple[ 0 ] + '\t' + str( tuple[ 1 ] ) )

# done
quit()


