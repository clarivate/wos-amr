# Web of Science Links Article Match Retrieval Service (AMR)

This client allows users to send batch requests to [AMR](http://ipscience-help.thomsonreuters.com/LAMRService/WebServicesOverviewGroup/overview.html) to match local metadata to the Web of Science and retrieve details about individual documents from the Web of Science.

For more information about web services for the Web of Science, please review this [data integration](http://ip-science.interest.thomsonreuters.com/data-integration) website.

## Getting started

### Requirements
* Python 2.7
* Access to the [AMR](http://ipscience-help.thomsonreuters.com/LAMRService/WebServicesOverviewGroup/overview.html) service

### Install

* Download or clone this repository by clicking on the "Clone or download" button in the top right corner
* Set two environment variables with your AMR credentials.
 * WOS_USER
 * WOS_PASSWORD

#### Setting environment variables

On a Mac or Linux system:

~~~
$ export WOS_USER="myuser"
$ export WOS_PASSWORD="mypassword"
~~~

On Windows, open a command window:

~~~
set WOS_USER="myuser"
set WOS_PASSWORD="mypassword"
~~~

#### Running a script

Run the script with the incoming csv data as the first parameter and output file as the second parameter. For example:

~~~
$ python lookup_ids.py myfile.csv output.csv
~~~

#### Disclaimer

These scripts are provided to allow Web of Science users to perform common operations with the AMR web service. The scripts and uses cases may change over time. No direct support is provided. Please contact [technical support](http://ip-science.thomsonreuters.com/techsupport/) with questions regarding API access.

## Use Cases

### Match a set of DOIs or PMIDs to the Web of Science

With a CSV file with the following information, retrieve the Web of Science identifier (UT), DOI, current times cited count, and a link to the Web of Science.

Script name: [`lookup_ids.py`](./lookup_ids.py)

#### incoming data
|PMID|DOI|
|----|---|
19883697|10.1016/j.bbr.2009.10.030
22011016|10.1080/09602011.2011.621275
2223077|10.1016/j.neuropsychologia.2011.12.011

#### matched data

|id|ut|doi|pmid|times cited|source|
|---|---|---|---|----|---|
1|WOS:000276621200002|10.1016/j.bbr.2009.10.030|19883697|95|...
2|WOS:000299789100009|10.1080/09602011.2011.621275|22011016|33|....
3|WOS:000300816600006|10.1016/j.neuropsychologia.2011.12.011|22223077|22|...


### Get JCR URLs for a set of ISSNs

Script name: [`issns_to_jcr.py`](./issns_to_jcr.py)

An incoming csv file with a column with an ID and a ISSN can be match to the Web of Science and a link to the Journal Citation Reports URL for that journal can be returned. 

More use cases will be added .....
