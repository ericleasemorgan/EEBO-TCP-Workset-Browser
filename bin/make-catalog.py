#!/usr/bin/env python

# make-catalog.py - create a "catalog" from the selected EEBO XML files

# Eric Lease Morgan <emorgan@nd.edu>
# June 10, 2015 - first cut; based on work from HathiTrust
# June 13, 2015 - added count of pages 
# June 15, 2015 - changed dates so they: 1) exist, and 2) are not ranges


# configure
DEBUG     = 0
HTML      = '/html/'
PLAINTEXT = '/text/'
ROOT      = 'http://dh.crc.nd.edu/sandbox/eebo-tcp/'
XML       = '/xml/'

# require
import glob
import sys
import re
import libxml2
import ntpath

# sanity check
if len( sys.argv ) != 2 :
	print "Usage:", sys.argv[ 0 ], '<name>'
	quit()

# get input
name = sys.argv[ 1 ]

# process each xml file in the given directory
for filename in glob.glob( name + XML + '*.xml' ):

	# open and create a parser against the file
	sys.stderr.write( filename + '\n' )
	tei = libxml2.parseFile( filename )
	tei = tei.xpathNewContext()
	tei.xpathRegisterNs( 't', 'http://www.tei-c.org/ns/1.0' )

	# parse out the easy stuff; stupid and verbose xpath
	id         = str( tei.xpathEval( '//t:TEI/t:teiHeader/t:fileDesc/t:publicationStmt/t:idno[@type="DLPS"]' )[ 0 ].content )
	title      = str( tei.xpathEval(  '/t:TEI/t:teiHeader/t:fileDesc/t:titleStmt/t:title/text()' )[ 0 ] )
	language   = str( tei.xpathEval(  '/t:TEI/t:teiHeader/t:profileDesc/t:langUsage/t:language/@ident' )[ 0 ].content )
	pagination = str( tei.xpathEval(  '/t:TEI/t:teiHeader/t:fileDesc/t:sourceDesc/t:biblFull/t:extent/text()' )[ 0 ] )
	pages      = int( tei.xpathEval(  'count( //t:pb )' ) )
	
	# date; it doesn't always exist; and sorry, but I can only use the first four characters
	date = '9999'
	if tei.xpathEval( '/t:TEI/t:teiHeader/t:fileDesc/t:editionStmt/t:edition/t:date/text()' ) : date = str( tei.xpathEval( '/t:TEI/t:teiHeader/t:fileDesc/t:editionStmt/t:edition/t:date/text()' )[ 0 ] )
	date = date[:4]
	
	# author; it doesn't always exist?
	author = ''
	if tei.xpathEval( '/t:TEI/t:teiHeader/t:fileDesc/t:titleStmt/t:author/text()' ) : author = str( tei.xpathEval( '/t:TEI/t:teiHeader/t:fileDesc/t:titleStmt/t:author/text()' )[ 0 ] )

	# publisher
	publisher = str( tei.xpathEval( '/t:TEI/t:teiHeader/t:fileDesc/t:sourceDesc/t:biblFull/t:publicationStmt' )[ 0 ].content )
	publisher = re.sub( '\s+', ' ', publisher )
	publisher = re.sub( '^\s+', '', publisher )
	
	# subjects
	subjects = ''
	terms    = tei.xpathEval( '//t:TEI/t:teiHeader/t:profileDesc/t:textClass/t:keywords/t:term/text()' );
	for term in terms: subjects = subjects + str( term ) + '|'
	subjects = re.sub( ' +', ' ', subjects )
	
	# define the location of the raw tei
	tei = ROOT + name + XML + ntpath.basename( filename )
	
	# location of the plain text
	plaintext = ROOT + name + PLAINTEXT + ntpath.basename( filename )
	plaintext = re.sub( 'xml$', 'txt', plaintext )
	
	# html
	html = ROOT + name + HTML + ntpath.basename( filename )
	html = re.sub( 'xml$', 'html', html )
	
	# debug
	if DEBUG :
	
		# echo
		print '          id:', id
		print '       title:', title
		print '      author:', author
		print '        date:', date
		print '   lannguage:', language
		print '  pagination:', pagination
		print '       pages:', pages
		print '   publisher:', publisher
		print '  subject(s):', subjects
		print '         TEI:', tei
		print '        HTML:', html
		print '  plain text:', plaintext
		print
	
	# or not; output
	else : print( '\t'.join( map( str, [ id, title, author, date, language, pagination, pages, publisher, subjects, tei, html, plaintext ] ) ) )
	
# done
quit()

