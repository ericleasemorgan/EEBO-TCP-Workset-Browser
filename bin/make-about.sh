#!/bin/bash

# make-about.sh - create a set of name/value pairs describing a corpus

# Eric Lease Morgan <emorgan@nd.edu>
# June 11, 2015 - first cut; based on HathiTrust work


# get input
CORPUSNAME=$1

# sanity check
if [ -z $CORPUSNAME ]; then

    echo "Usage: $0 <name>"
    exit 1
    
fi

# size of corpus
CORPUSSIZE=$( ls -1 $CORPUSNAME/xml/*.xml | wc -l )

# slurp up the catalog and remove its header
CATALOG=$( sed '1d' $CORPUSNAME/catalog.db )

# remember, the fields in the (default) catalog
#   1 - ids
#   2 - titles
#   3 - authors
#   4 - dates
#   5 - languages
#   6 - pagination
#   7 - pages
#   8 - publishers
#   9 - subjects
#  10 - tei
#  11 - html
#  12 - text
#  13 - words
#  14 - colors
#  15 - names
#  16 - ideas

# date range
DATEEARLIEST=$( echo "$CATALOG" | sort -t $'\t' -k4 -g    | cut -f4 | head -1 )
DATELATEST=$(   echo "$CATALOG" | sort -t $'\t' -k4 -g -r | cut -f4 | head -1 )

# size in page
PAGESSHORTEST=$(echo "$CATALOG" | sort -t $'\t' -k7 -g    | cut -f7 | head -1 )
PAGESLONGEST=$( echo "$CATALOG" | sort -t $'\t' -k7 -g -r | cut -f7 | head -1 )
PAGESTOTAL=$(   echo "$CATALOG" | cut  -f7 | paste -sd+ - | bc )

# size in words
WORDSSHORTEST=$(echo "$CATALOG" | sort -t $'\t' -k13 -n    | cut -f13 | head -1 )
WORDSLONGEST=$( echo "$CATALOG" | sort -t $'\t' -k13 -n -r | cut -f13 | head -1 )
WORDSTOTAL=$(   echo "$CATALOG" | cut -f13 | paste -sd+ - | bc )
WORDSUNIQUE=$(    wc -l < $CORPUSNAME/unique.db | tr -d ' ' )

# most frequent words
FREQUENTWORDS=$( cat $CORPUSNAME/dictionary.db        | head -25 | awk '{print $1" "$2}' | tr '\n' '|' )
FREQUENTIDEAS=$( cat $CORPUSNAME/dictionary-ideas.db  | head -25 | awk '{print $1" "$2}' | tr '\n' '|' )
FREQUENTNAMES=$( cat $CORPUSNAME/dictionary-names.db  | head -25 | awk '{print $1" "$2}' | tr '\n' '|' )
FREQUENTCOLORS=$(cat $CORPUSNAME/dictionary-colors.db | head -10 | awk '{print $1" "$2}' | tr '\n' '|' )

# items of interest
WORKSHORTEST=$( echo "$CATALOG" | sort -t $'\t' -k13 -g     | head -1 | cut -f1 )
WORKLONGEST=$(  echo "$CATALOG" | sort -t $'\t' -k13 -g -r  | head -1 | cut -f1 )
WORKOLDEST=$(   echo "$CATALOG" | sort -t $'\t' -k4  -g     | head -1 | cut -f1 )
WORKNEWEST=$(   echo "$CATALOG" | sort -t $'\t' -k4  -g -r  | head -1 | cut -f1 )
COLORSMOST=$(   echo "$CATALOG" | sort -t $'\t' -k14 -g -r  | head -1 | cut -f1 )
COLORSLEAST=$(  echo "$CATALOG" | sort -t $'\t' -k14 -g     | head -1 | cut -f1 )
NAMESMOST=$(    echo "$CATALOG" | sort -t $'\t' -k15 -g -r  | head -1 | cut -f1 )
NAMESLEAST=$(   echo "$CATALOG" | sort -t $'\t' -k15 -g     | head -1 | cut -f1 )
IDEASMOST=$(    echo "$CATALOG" | sort -t $'\t' -k16 -g -r  | head -1 | cut -f1 )
IDEASLEAST=$(   echo "$CATALOG" | sort -t $'\t' -k16 -g     | head -1 | cut -f1 )

# output
printf "CORPUSNAME\t$CORPUSNAME\n"
printf "CORPUSSIZE\t$CORPUSSIZE\n"
printf "DATEEARLIEST\t$DATEEARLIEST\n"
printf "DATELATEST\t$DATELATEST\n"
printf "PAGESSHORTEST\t$PAGESSHORTEST\n"
printf "PAGESLONGEST\t$PAGESLONGEST\n"
printf "PAGESTOTAL\t$PAGESTOTAL\n"
printf "WORDSSHORTEST\t$WORDSSHORTEST\n"
printf "WORDSLONGEST\t$WORDSLONGEST\n"
printf "WORDSTOTAL\t$WORDSTOTAL\n"
printf "WORDSUNIQUE\t$WORDSUNIQUE\n"
printf "FREQUENTWORDS\t$FREQUENTWORDS\n"
printf "FREQUENTIDEAS\t$FREQUENTIDEAS\n"
printf "FREQUENTNAMES\t$FREQUENTNAMES\n"
printf "FREQUENTCOLORS\t$FREQUENTCOLORS\n"
printf "WORKSHORTEST\t$WORKSHORTEST\n"
printf "WORKLONGEST\t$WORKLONGEST\n"
printf "WORKOLDEST\t$WORKOLDEST\n"
printf "WORKNEWEST\t$WORKNEWEST\n"
printf "IDEASMOST\t$IDEASMOST\n"
printf "IDEASLEAST\t$IDEASLEAST\n"
printf "NAMESMOST\t$NAMESMOST\n"
printf "NAMESLEAST\t$NAMESLEAST\n"
printf "COLORSMOST\t$COLORSMOST\n"
printf "COLORSLEAST\t$COLORSLEAST\n"

# done
exit


