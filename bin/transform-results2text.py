#!/usr/bin/env python

# results2text.py - format search results as a stream of plain text

# Eric Lease Morgan <emorgan@nd.edu>
# June 13, 2015 - first cut; based on HathiTrust work


# require
import sys

# sanity check
if sys.stdin.isatty() :
	print "Usage: ./bin/search.py <query> <name> | " + sys.argv[ 0 ] 
	quit()
	
# initialize
pointer = 0

# process each hit from standard input
for hit in sys.stdin:

	# increment
	pointer = pointer + 1

	# the input stream should have the following structure
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
	
	# parse the record into fields
	fields = hit.rstrip().split( '\t' )
	
	# output
	print( str( pointer ) + '. ' + fields[   1 ] )
	print( '      author: ' + str( fields[   2 ] ) )
	print( '        date: ' + str( fields[   3 ] ) )
	print( '    langauge: ' + str( fields[   4 ] ) )
	print( '  pagination: ' + str( fields[   5 ] ) )
	print( '       pages: ' + str( fields[   6 ] ) )
	print( '   publisher: ' + str( fields[   7 ] ) )
	print( '    subjects: ' + str( fields[   8 ] ) )
	print( '         tei: ' + str( fields[   9 ] ) )
	print( '        html: ' + str( fields[  10 ] ) )
	print( '  plain text: ' + str( fields[  11 ] ) )
	print( '       words: ' + str( fields[  12 ] ) )
	print( '      colors: ' + str( fields[  13 ] ) )
	print( '       names: ' + str( fields[  14 ] ) )
	print( '       ideas: ' + str( fields[  15 ] ) )
	print( '       count: ' + str( fields[  16 ] ) )
	print( '       tfidf: ' + str( fields[  17 ] ) )
	print( '          id: ' + str( fields[   0 ] ) )
	print

# done
quit()

