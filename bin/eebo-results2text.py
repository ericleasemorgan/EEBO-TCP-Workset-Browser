#!/usr/bin/env python

# results2text.py - format search results as a stream of plain text

# Eric Lease Morgan <emorgan@nd.edu>
# May  27, 2015 - first cut
# June  2, 2015 - added sanity checking
# June 15, 2015 - tweaked for eebo


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
	
	# output
	print( str( pointer ) + '. ' + fields[  2 ] )
	print( '      author: ' + str( fields[  1 ] ) )
	print( '        date: ' + str( fields[  3 ] ) )
	print( '  pagination: ' + str( fields[  6 ] ) )
	print( '       pages: ' + str( fields[  7 ] ) )
	print( '       words: ' + str( fields[  8 ] ) )
	print( '    langauge: ' +      fields[  5 ] )
	print( '  subject(s): ' +      fields[  4 ] )
	print( '   publisher: ' +      fields[  9 ] )
	print( '          id: ' +      fields[  0 ] )
	print

# done
quit()

