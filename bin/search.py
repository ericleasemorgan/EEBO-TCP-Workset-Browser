#!/usr/bin/env python

# search.py - given a word and an index, return a list of relevancy ranked identifiers whose document contains the word

# Eric Lease Morgan <emorgan@nd.edu>
# June 13, 2015 - first cut; based on HathiTrust work


# configure
DEBUG   = 0
CATALOG = '/catalog.db'

# require
import glob
import math
import ntpath
import re
import sys
import operator

# sanity check
if len( sys.argv ) != 3 :
	print "Usage" + sys.argv[ 0 ] + ' <query> <name>'
	quit()

# get input; sanity check
query     = sys.argv[ 1 ].lower()
directory = sys.argv[ 2 ]

# initialize
total_documents = 0;
hits            = {};

# process each (database) file in the given directory
for filename in glob.glob( directory + '/index/*.db' ) :
	
	# increment
	total_documents += 1

	# re-initialize
	found      = 0
	size       = 0
	statistics = {}
	statistics = { 'count' : 0, 'size' : size, 'tfidf' : 0 }
	
	# process each "database"
	with open( filename ) as DATABASE :
	
		# create a key for the dictionary of hits
		id = ntpath.basename( filename )
		id = re.sub( '\.db$', '', id )

		# process each record
		for record in DATABASE :
			
			# parse
			fields = record.rstrip().split( '\t' )
			word   = fields[ 0 ]
			count  = int( fields[ 1 ] )

			# check for hit
			if word == query :
		
				# update statistics and hits
				statistics[ 'count' ] = count
				hits[ id ]            = statistics
					
				# update found
				found = 1;
			
			# increment size of document
			size += count
	
		# update statistics
		if found : hits[ id ][ 'size' ] = size 
	
		# debug
		if DEBUG :
			sys.stdout.write( 'documents: ' + str( total_documents ) + '\thits: ' + str( len( hits ) ) + '\r' )
			sys.stdout.flush()

# debug
if DEBUG : print( 'documents: ' + str( total_documents ) + '\thits: ' + str( len( hits ) ) )

# score all the hits
d = total_documents
h = len( hits )
for id in sorted( hits ) :

	# re-initialize
	n     = hits[ id ][ 'count' ]
	t     = hits[ id ][ 'size' ]
	tfidf = 0
	
	# calculate tfidf = ( n / t ) * log( d / h ) where:
	#     n = number of times a word appears in a document
	#     t = total number of words
	#     d = total number of documents
	#     h = number of documents that contain the word	
	if d == h : tfidf = float( n ) / t
	else : tfidf = ( float( n ) / t ) * math.log( float( d ) / h )
	
	# debug
	if DEBUG :

		# echo
		print '     id: ' + id
		print '  count: ' + str( n )
		print '   size: ' + str( t )
		print '  tfidf: ' + str( tfidf )
		print 

	# update
	hits[ id ][ 'tfidf' ] = tfidf

# update the list of keys in the hits with its metadata
with open( directory + CATALOG ) as DATABASE :

		# initialize the pointer
		pointer = 0
		
		# process each record in the catalog
		for record in DATABASE :

			# increment; we don't want the field headers
			pointer = pointer + 1
			if pointer == 1 : continue
			
			# read the record
			fields = record.rstrip().split( '\t' )
			
			# get the identifier
			id = fields[ 0 ]
							
			# search for the key in the list hits - "needle in a haystack"
			if id in hits :
				
				# remember, the fields in the (default) catalog
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
				#  11 - text
				#  12 - words
				#  13 - colors
				#  14 - names
				#  15 - ideas

				# update the hit list
				hits[ id ][ 'title' ]      = fields[   1 ]
				hits[ id ][ 'author' ]     = fields[   2 ]
				hits[ id ][ 'date' ]       = fields[   3 ]
				hits[ id ][ 'language' ]   = fields[   4 ]
				hits[ id ][ 'pagination' ] = fields[   5 ]
				hits[ id ][ 'pages' ]      = fields[   6 ]
				hits[ id ][ 'publisher' ]  = fields[   7 ]
				hits[ id ][ 'subjects' ]   = fields[   8 ]
				hits[ id ][ 'tei' ]        = fields[   9 ]
				hits[ id ][ 'html' ]       = fields[  10 ]
				hits[ id ][ 'plaintext' ]  = fields[  11 ]
				hits[ id ][ 'words' ]      = fields[  12 ]
				hits[ id ][ 'colors' ]     = fields[  13 ]
				hits[ id ][ 'names' ]      = fields[  14 ]
				hits[ id ][ 'ideas' ]      = fields[  15 ]

# output; I wish I could sort by tfidf!
for id in sorted( hits ) :
	
	# parse
	title      = hits[ id ][ 'title' ]
	author     = hits[ id ][ 'author' ]
	date       = hits[ id ][ 'date' ]
	language   = hits[ id ][ 'language' ]
	pagination = hits[ id ][ 'pagination' ]
	pages      = hits[ id ][ 'pages' ]
	publisher  = hits[ id ][ 'publisher' ]
	subjects   = hits[ id ][ 'subjects' ]
	tei        = hits[ id ][ 'tei' ]
	html       = hits[ id ][ 'html' ]
	plaintext  = hits[ id ][ 'plaintext' ]
	words      = hits[ id ][ 'words' ]
	colors     = hits[ id ][ 'colors' ]
	names      = hits[ id ][ 'names' ]
	ideas      = hits[ id ][ 'ideas' ]
	count      = hits[ id ][ 'count' ]
	tfidf      = hits[ id ][ 'tfidf' ]
		
	# output
	print( '\t'.join( map( str, [ id, title, author, date, language, pagination, pages, publisher, subjects, tei, html, plaintext, words, colors, names, ideas, count, tfidf ] ) ) )

# done
quit()
