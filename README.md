# pyMARC
Python Tools to handle MARC21 XML and ASEQ data

python marc2aseq.py  | tee  samples/woldan_record_marc.xml

zorba -i -f -q ../aseq2marcxml/markxml2bibframe.xqy -e marcxmluri:="./samples/woldan_record_marc.xml" -e writelog:="true" -e logdir:="./log/" -e baseuri:="http://permalink.obvsg.at/" | tee samples/woldan_marc_record.rdf

python marc2aseq.py  | tee  samples/woldan_marc.xml

zorba -i -f -q ../aseq2marcxml/markxml2bibframe.xqy -e marcxmluri:="./samples/woldan_record_marc.xml" -e writelog:="true" -e logdir:="./log/" -e baseuri:="http://permalink.obvsg.at/" | tee samples/woldan_marc_record.rdf

 xmllint --noout --schema ./xsd/MARC21relaxed.xsd samples/woldan_record_aseq.xml

 marc2bf samples/woldan_record_marc.xml --rdfttl samples/woldan_record_marc.ttl
