#!/usr/bin/env python

# about2html.py - transform an about.db file into an HTML stream

# Eric Lease Morgan <emorgan@nd.edu>
# June 11, 2015 - first investigations; based on work from HathiTrust
# June 13, 2015 - added links to tei, html, and re-configured plain text
# June 20, 2015 - made links to items of interest relative


# configure
ABOUT    = '/about.db'
CATALOG  = '/catalog.db'
SEARCH   = './search.cgi?q='
TEMPLATE = './etc/template-about.txt'
XML      = './xml/'
HTML     = './html/'
TEXT     = './text/'

# require
import sys
import re

# sanity check
if len( sys.argv ) != 2 :
	print "Usage: " + sys.argv[ 0 ] + ' <name>'
	quit()


# get input
corpus = sys.argv[ 1 ]

# read the database
metadata = {}
with open ( corpus + ABOUT ) as database :

		# process each record
		for record in database :
		
			# map each field to my metadata
			field = record.rstrip().split( '\t' )
			metadata[ field[ 0 ] ] = field[ 1 ]

# mark-up the frequently used words (not scalable)
frequent_links = ''
for word in metadata[ 'FREQUENTWORDS' ].rstrip( '|' ).split( '|' ) :

	fields = word.split( ' ' )
	item   = fields[ 0 ]
	count  = str( fields[ 1 ] )
	frequent_links  = frequent_links + '<a href="' + SEARCH + item + '">' + item + '</a> (' + count + ')&nbsp; '

# colors
color_links = ''
for color in metadata[ 'FREQUENTCOLORS' ].rstrip( '|' ).split( '|' ) :

	fields = color.split( ' ' )
	item   = fields[ 0 ]
	count  = str( fields[ 1 ] )
	color_links  = color_links + '<a href="' + SEARCH + item + '">' + item + '</a> (' + count + ')&nbsp; '

# names
names_links = ''
for name in metadata[ 'FREQUENTNAMES' ].rstrip( '|' ).split( '|' ) :

	fields = name.split( ' ' )
	item   = fields[ 0 ]
	count  = str( fields[ 1 ] )
	names_links  = names_links + '<a href="' + SEARCH + item + '">' + item + '</a> (' + count + ')&nbsp; '

# ideas
ideas_links = ''
for idea in metadata[ 'FREQUENTIDEAS' ].rstrip( '|' ).split( '|' ) :

	fields = idea.split( ' ' )
	item   = fields[ 0 ]
	count  = str( fields[ 1 ] )
	ideas_links  = ideas_links + '<a href="' + SEARCH + item + '">' + item + '</a> (' + count + ')&nbsp; '

# look up keys in catalog and get metadata
catalog = {}
with open ( corpus + CATALOG ) as database :

	index = 0
	for record in database :
	
		# increment and check; we don't need the catalog's header
		index = index + 1
		if index == 1 : continue
		
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
		
		# read a record
		fields = record.rstrip().split( '\t' )

		# get the key
		key = fields[ 0 ]
				
		catalog[ key ] = {}
		catalog[ key ][ 'title' ] = fields[  1 ]
		catalog[ key ][ 'tei' ]   = fields[  9 ]
		catalog[ key ][ 'html' ]  = fields[ 10 ]
		catalog[ key ][ 'text' ]  = fields[ 11 ]

# create the links of interest; shortest
title        = catalog[ metadata[ 'WORKSHORTEST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'WORKSHORTEST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'WORKSHORTEST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'WORKSHORTEST' ] + '.txt">plain text</a>'
workshortest = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# longest
title        = catalog[ metadata[ 'WORKLONGEST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'WORKLONGEST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'WORKLONGEST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'WORKLONGEST' ] + '.txt">plain text</a>'
worklongest = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# oldest
title        = catalog[ metadata[ 'WORKOLDEST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'WORKOLDEST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'WORKOLDEST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'WORKOLDEST' ] + '.txt">plain text</a>'
workoldest = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# newest
title        = catalog[ metadata[ 'WORKNEWEST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'WORKNEWEST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'WORKNEWEST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'WORKNEWEST' ] + '.txt">plain text</a>'
worknewest = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# most ideas
title        = catalog[ metadata[ 'IDEASMOST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'IDEASMOST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'IDEASMOST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'IDEASMOST' ] + '.txt">plain text</a>'
ideasmost = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# least ideas
title        = catalog[ metadata[ 'IDEASLEAST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'IDEASLEAST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'IDEASLEAST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'IDEASLEAST' ] + '.txt">plain text</a>'
ideasleast = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# most names
title        = catalog[ metadata[ 'NAMESMOST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'NAMESMOST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'NAMESMOST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'NAMESMOST' ] + '.txt">plain text</a>'
namesmost = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# least names
title        = catalog[ metadata[ 'NAMESLEAST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'NAMESLEAST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'NAMESLEAST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'NAMESLEAST' ] + '.txt">plain text</a>'
namesleast = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# most colors
title        = catalog[ metadata[ 'COLORSMOST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'COLORSMOST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'COLORSMOST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'COLORSMOST' ] + '.txt">plain text</a>'
colorsmost = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# least colors
title        = catalog[ metadata[ 'COLORSLEAST' ] ][ 'title' ]
tei          = '<a href="' + XML  + metadata[ 'COLORSLEAST' ] + '.xml">TEI</a>'
html         = '<a href="' + HTML + metadata[ 'COLORSLEAST' ] + '.html">HTML</a>'
plaintext    = '<a href="' + TEXT + metadata[ 'COLORSLEAST' ] + '.txt">plain text</a>'
colorsleast = title + ' (' + tei + ' : ' + html + ' : ' + plaintext + ')'

# do some math; add more "kewl" calculations here
pagesaverage = str( int( metadata[ 'PAGESTOTAL' ] ) / int( metadata[ 'CORPUSSIZE' ] ) )
wordsaverage = str( int( metadata[ 'WORDSTOTAL' ] ) / int( metadata[ 'CORPUSSIZE' ] ) )

# slurp up the template; find & replace the tokesn
with open ( TEMPLATE ) as HTML : html = HTML.read()
html = re.sub( '##CORPUSNAME##',     metadata[ 'CORPUSNAME' ],    html )
html = re.sub( '##CORPUSSIZE##',     metadata[ 'CORPUSSIZE' ],    html )
html = re.sub( '##DATEEARLIEST##',   metadata[ 'DATEEARLIEST' ],  html )
html = re.sub( '##DATELATEST##',     metadata[ 'DATELATEST' ],    html )
html = re.sub( '##PAGESSHORTEST##',  metadata[ 'PAGESSHORTEST' ], html )
html = re.sub( '##PAGESLONGEST##',   metadata[ 'PAGESLONGEST' ],  html )
html = re.sub( '##PAGESTOTAL##',     metadata[ 'PAGESTOTAL' ],    html )
html = re.sub( '##PAGESAVERAGE##',   pagesaverage,                html )
html = re.sub( '##WORDSSHORTEST##',  metadata[ 'WORDSSHORTEST' ], html )
html = re.sub( '##WORDSLONGEST##',   metadata[ 'WORDSLONGEST' ],  html )
html = re.sub( '##WORDSTOTAL##',     metadata[ 'WORDSTOTAL' ],    html )
html = re.sub( '##WORDSAVERAGE##',   wordsaverage,                html )
html = re.sub( '##WORDSUNIQUE##',    metadata[ 'WORDSUNIQUE' ],   html )
html = re.sub( '##FREQUENTWORDS##',  frequent_links,              html )
html = re.sub( '##FREQUENTIDEAS##',  ideas_links,                 html )
html = re.sub( '##FREQUENTNAMES##',  names_links,                 html )
html = re.sub( '##FREQUENTCOLORS##', color_links,                 html )
html = re.sub( '##WORKSHORTEST##',   workshortest,                html )
html = re.sub( '##WORKLONGEST##',    worklongest,                 html )
html = re.sub( '##WORKOLDEST##',     workoldest,                  html )
html = re.sub( '##WORKNEWEST##',     worknewest,                  html )
html = re.sub( '##IDEASMOST##',      ideasmost,                   html )
html = re.sub( '##IDEASLEAST##',     ideasleast,                  html )
html = re.sub( '##NAMESMOST##',      namesmost,                   html )
html = re.sub( '##NAMESLEAST##',     namesleast,                  html )
html = re.sub( '##COLORSMOST##',     colorsmost,                  html )
html = re.sub( '##COLORSLEAST##',    colorsleast,                 html )

# output and done
print html
quit()


