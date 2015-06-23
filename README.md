# EEBO TCP Workset Browser

The EEBO-TCP Workset Browser is a suite of software designed to support "distant reading" against the corpus called the Early English Books Online - Text Creation Partnership corpus. [1] Using the Browser it is possible to: 1) search a "catalog" of the corpus's metadata, 2) create a list of identifiers representing a subset of content for study, 3) feed the identifiers to a set of files which will mirror the content locally, index it, and do some rudimentary analysis outputting as set of HTML files, structured data, and graphs. The reader is then expected to examine the output more "closely" (all puns intended) using their favorite Web browser, text editor, spreadsheet, database, or statistical application. The purpose and functionality of this suite is very similar to the purpose and functionality of HathiTrust Research Center Workset Browser. [2]

## Requirements

The Browser is designed to work on Linux and Macintosh computers with Python and the Bash Shell installed. At the very least, the Browser also requires wget as well as a Python library called libxml2. [3, 4] The dependency on wget can (and probably will) be removed. Installing libxml2 can be a real pain. I know. I'm sorry. This too can (and probably will) be removed.

## Quick start

Here's a set of quick start instructions. Download the software and uncompress it, if necessary. Second, open your terminal and change directories to the distribution. Third, create a collection with the following command:

>`cat ./etc/catalog-lute.txt | ./bin/make-everything.sh lute`

If Bash, Python, wget, and libxml2 are installed, then the command will create a directory named lute, mirror bunches o' XML/TEI files, index them, create a "catalog" of them, do the rudimentary analysis, and generate data for further analysis. Of special interest is the file named `lute/catalog.db`. Import this file into your favorite spreadsheet or database program to search, sort, and browse characteristics of the collection. The next report of special interest is `lute/about.html`. It provides an overall narrative describing the collection.

If you saved the Browser to a file system accessible via HTTP, then edit `./bin/make-catalog.py` changing the value of ROOT found near the top of the file to the root URL where the Browser software can be found. Then recreate the catalog's db and html files:

>`./bin/make-catalog.sh lute`

If you have Java installed, then you can transform the mirrored XML/TEI into pretty HTML. To do so, you need to get a copy of Saxon (HE). [5] Download Saxon, uncompress the archive, and then edit `./bin/transform-xml2html.sh`. Specifically, change the value of JAR found near the top of the file to point to the Saxon (HE)'s .jar file. You can now do the transformations with the following command, and the results will be found in `lute/html/`:

>`./bin/transform-xml2html.sh lute`

If you have R installed, then you can create quite a number of graphs literally illustrating characteristics of the collection, but you will also need a few R libraries, specifically: NLP, tm, RColorBrewer, and wordcloud. Once these libraries are installed, generate the graphs with the following command, and the results will be saved in `lute/graphs/`:

>`./bin/make-graphs.sh lute`


## Extra credit

If you have gotten this far, then create a collection of Shakespeare's works with the following commands:

>`cat etc/catalog-shakespeare.txt | ./bin/make-everything.sh shakespeare`

>`./bin/make-graphs.sh shakespeare`

>`./bin/transform-xml2html.sh shakespeare &>/dev/null &`

You are now ready for extra credit. Edit `./bin/make-everything.sh` and uncomment the following lines found towards the beginning and end of the file:

	     #echo "transforming TEI to HTML"
	     #./bin/transform-xml2html.sh $NAME 

	     #echo "making graphs"
	     #./bin/make-graphs.sh $NAME

You can now create a collection with a single command:

>`cat etc/catalog-mather.txt | ./bin/make-everything.sh mather`

## Creating your own collections

Creating your own collections is a matter of creating a set of EEBO-TCP identifiers and feeding them to `./bin/make-everything.sh`. As of this writing, there is a complete collection of EEBO-TCP identifiers and their associated pieces of metadata found in the the file named `eebo.db`. For example, try some of the following commands to get feel for how the word lute is used in the entire corpus's metadata:

>`./bin/eebo-search.sh lute`

>`./bin/eebo-search.sh lute facets`

>`./bin/eebo-search.sh lute facets | less`

> `./bin/eebo-search.sh lute facets | ./bin/eebo-results2text.py`

> `./bin/eebo-search.sh lute facets | ./bin/eebo-results2text.py | less`

> `./bin/eebo-search.sh lute facets | ./bin/eebo-results2html.py lute | less`

> `./bin/eebo-search.sh lute facets | ./bin/eebo-results2html.py lute > lute.html`

> `./bin/eebo-search.sh lute facets | ./bin/make-everything.sh new-lute`

Please be forewarned because `./bin/eebo-search.sh` can only search for single words. Phrase searching is not supported.

Power-readers will want to peruse the indexes found in `./etc/eebo-index-*.idx`. Search, sort, and browse these files using your favorite spreadsheet, database, or text editor application. Power-readers will also want to import `eebo.db` into the same applications. Believe me, the results will be eye-opening!

## Links

1. EEBO-TCP - [http://www.textcreationpartnership.org/tcp-eebo/](http://www.textcreationpartnership.org/tcp-eebo/)
2. HTRC Workset Browser - [https://github.com/ericleasemorgan/HTRC-Workset-Browser](https://github.com/ericleasemorgan/HTRC-Workset-Browser)
3. wget - [http://www.gnu.org/software/wget/](http://www.gnu.org/software/wget/)
4. libxml2 - [http://www.xmlsoft.org/python.html](http://www.xmlsoft.org/python.html)
5. Saxon (HE) - [http://saxon.sourceforge.net](http://saxon.sourceforge.net)

## Author
Eric Lease Morgan <[emorgan@nd.edu](emorgan@nd.edu)>

June 23, 2015




