#!/bin/bash

# make-catalog.sh - given a name, create a "database" from the previously gathered information

# Eric Lease Morgan <emorgan@nd.edu>
# May  23, 2015 - first cut
# May  30, 2015 - added human-readable version to output
# June  2, 2015 - added sanity checking; removed json configuration
# June 13, 2015 - added pages


# get input
NAME=$1

# sanity check
if [ -z $NAME ]; then

    echo "Usage: $0 <name>"
    exit 1
    
fi

# initialize the database with the content from the json files
echo "making base catalog"
./bin/make-catalog.py $NAME | sort > $NAME/catalog.db

# append: sizes, colors, names, ideas
echo "adding sizes to catalog"
./bin/calculate-size.sh   $NAME                      | sort | cut -f2 | paste $NAME/catalog.db - > $NAME/catalog.tmp; mv $NAME/catalog.tmp $NAME/catalog.db

echo "adding color themes to catalog"
./bin/calculate-themes.sh $NAME etc/theme-colors.txt | sort | cut -f2 | paste $NAME/catalog.db - > $NAME/catalog.tmp; mv $NAME/catalog.tmp $NAME/catalog.db

echo "adding names to catalog"
./bin/calculate-themes.sh $NAME etc/theme-names.txt  | sort | cut -f2 | paste $NAME/catalog.db - > $NAME/catalog.tmp; mv $NAME/catalog.tmp $NAME/catalog.db

echo "adding ideas to catalog"
./bin/calculate-themes.sh $NAME etc/theme-ideas.txt  | sort | cut -f2 | paste $NAME/catalog.db - > $NAME/catalog.tmp; mv $NAME/catalog.tmp $NAME/catalog.db

# add the human-readable header
echo "adding header to catalog"
printf "ids\ttitles\tauthors\tdates\tlanguages\tpagination\tpages\tpublishers\tsubjects\ttei\thtml\ttext\twords\tcolors\tnames\tideas\n" | cat - $NAME/catalog.db > $NAME/catalog.tmp; mv $NAME/catalog.tmp $NAME/catalog.db

# make the human-readable version
echo "transforming catalog.db into catalog.html"
./bin/transform-catalog2html.py $NAME > $NAME/catalog.html

# make the search engine, as it may be, available
echo "adding search interface"
cp ./etc/search.cgi $NAME
chmod +x $NAME/search.cgi

# done
echo "done making catalog"
exit 0


