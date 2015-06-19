#!/usr/bin/perl

# xml2tab.pl - extract the simplest of bibliographic data from xml files

# Eric Lease Morgan <emorgan@nd.edu>
# June 5, 2015 - first cut
# June 6, 2015 - added more thorough output; lonely 


# configure
use constant DEBUG => 0;

# require
use strict;
use XML::XPath;

# get input and sanity check
my $file = $ARGV[ 0 ];
if ( ! $file ) {

	print "Usage: $0 <file>\n";
	exit;
	
}

# initialize
binmode( STDOUT, ":utf8" );
my $parser = XML::XPath->new( filename => $file );

# do the work; easy things
my $id         = $parser->findvalue( '/TEI/teiHeader/fileDesc/publicationStmt/idno[@type="DLPS"]' );
my $author     = $parser->findvalue( '/TEI/teiHeader/fileDesc/titleStmt/author' );
my $title      = $parser->findvalue( '/TEI/teiHeader/fileDesc/titleStmt/title' );
my $date       = $parser->findvalue( '/TEI/teiHeader/fileDesc/editionStmt/edition/date' );
my $language   = $parser->findvalue( '/TEI/teiHeader/profileDesc/langUsage/language/@ident' );
my $pagination = $parser->findvalue( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/extent' );
my $publisher  = $parser->findvalue( '/TEI/teiHeader/fileDesc/sourceDesc/biblFull/publicationStmt' );
my $text       = $parser->findvalue( '/TEI/text' );
my $pages      = $parser->findvalue( 'count( //pb )' );


# build and beautify list of subjects
my $terms    = $parser->find( '//TEI/teiHeader/profileDesc/textClass/keywords/term' );
my $subjects = '';
foreach my $term ( $terms->get_nodelist ) { $subjects .= $term->string_value . '|' }
$subjects =~ s/\s+/ /g;

# beautify publisher
$publisher =~ s/\s+/ /g;
$publisher =~ s/^\s+//g;
$publisher =~ s/\s+$//g;

# beautify text
$text     =~ s/\s+/ /g;
$text     =~ s/^\s+//g;
$text     =~ s/\s+$//g;

# so they can be counted, create a list of all the words
my @words =  split ' ', $text;

# debug
if ( DEBUG ) {

	print "          id: $id\n";
	print "      author: $author\n";
	print "       title: $title\n";
	print "        date: $date\n";
	print "    subjects: $subjects\n";
	print "    language: $language\n";
	print "  pagination: $pagination\n";
	print "       pages: $pages\n";
	print "       words: $#words\n";
	print "   publisher: $publisher\n";
	print "\n";
	#print "$text\n";
	#print "\n\n";

}

else {

	# output
	print "$id\t$author\t$title\t$date\t$subjects\t$language\t$pagination\t$pages\t$#words\t$publisher\n";

}

# done
exit;
