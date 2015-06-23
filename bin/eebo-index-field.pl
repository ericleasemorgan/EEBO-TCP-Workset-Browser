#!/usr/bin/perl

# eebo-index.pl - tabulate input, sort, and output

# Eric Lease Morgan <emorgan@nd.edu>
# June 14, 2015 - first cut; interesting


# get input; needs error checking
my $field = $ARGV[ 0 ];

# initialize
my %index     = ();
my $stopwords = &stopwords();

# process each line of input
while ( <STDIN> ) {

	# parse
	chop;
	my ( $key, $values ) = split '\t';
	
	# can't index on non-existent value; next;
	next if ( ! $values );
	
	# initialize values to index
	my @values = ();
	
	# parse the given values, but we don't parse these
	if ( $field eq 'languages' | $field eq 'authors' | $field eq 'dates' ) { $values[ 0 ] = $values }
	
	# titles and publishers; we just want words
	elsif ( $field eq 'titles' | $field eq 'publishers' ) {
	
		$values = lc( $values );
		@words = split '\s', $values;
		foreach my $word ( split '\s', $values ) {
		
			# filter out the things we don't want
			next if ( $word =~ /\d|\W/ );
			next if ( ! $word );
			next if ( $$stopwords{ $word } );
			next if ( length( $word) < 3 );
			
			# update the list of indexable items
			push @values, $word;
			
		}
		
	}
	
	# subjects are delimited by vertical bars
	elsif ( $field eq 'subjects' ) { @values = split '\|', $values }
	
	# facets are split subjects
	elsif ( $field eq 'facets' ) {
	
		$values =~ s/\|/ -- /g;
		@values = split ' -- ', $values;
		
	}
	
	# error
	else { die "Unknown value for fields ($fields). Call Eric.\n" }
	
	# process each value
	foreach $value ( @values ) {
	
		# normalize inconsistent puncutation
		$value =~ s/\.$//;
		
		# read the existing list of ids, and add a value
		my $ids = $index{ $value };
		push @$ids, $key;
	
		# update the index
		$index{ $value } = $ids;
	
	}
	
}

# kewl sort and output
foreach my $key ( sort{ scalar @{ $index{ $b } } <=> scalar @{ $index{ $a } } } keys( %index ) ) {

	print "$key\t";
	my $ids = $index{ $key };
	print join( ',', @$ids ), "\n";
	
}

# done
exit 0;

sub stopwords {

	my %stopwords = ();
	while ( <DATA> ) {
	
		chop;
		$stopwords{ $_ }++;
		
	}

	return \%stopwords;
	
}


# hard coded stop words
__DATA__
a
about
above
after
again
against
all
am
an
and
any
are
as
at
be
because
been
before
being
below
between
both
but
by
can
did
do
does
doing
don
down
during
each
few
for
from
further
had
has
have
having
he
her
here
hers
herself
him
himself
his
how
i
if
in
into
is
it
its
itself
just
me
more
most
my
myself
no
nor
not
now
of
off
on
once
only
or
other
our
ours
ourselves
out
over
own
same
she
should
so
some
such
than
that
the
thee
their
theirs
them
themselves
then
there
these
they
this
those
thou
through
thy
to
too
under
until
up
very
was
we
were
what
when
where
which
while
who
whom
why
will
with
you
your
yours
yourself
yourselves

