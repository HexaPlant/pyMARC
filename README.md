# pyMARC
Python Tools to handle MARC21 XML and ASEQ data


python marc2aseq.py  | tee  samples/woldan_record_marc.xml


zorba -i -f -q ../aseq2marcxml/markxml2bibframe.xqy -e marcxmluri:="./samples/woldan_record_marc.xml" -e writelog:="true" -e logdir:="./log/" -e baseuri:="http://permalink.obvsg.at/" | tee samples/woldan_marc_record.rdf
