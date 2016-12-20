# ./marc2MARC.py
# -*- coding: utf-8 -*-

from __future__ import print_function
import MARC21relaxed
import pyxb


fieldMap={
    "001":{ " ":{"*":{"type":"cf","tag":"001"}}},
    "002":{ "b":{"a":{"type":"cf","tag":"002"}}},
    "003":{ " ":{"*":{"type":"cf","tag":"003"}}},
    "034":{ " ":{"*":{"type":"df","tag":"034","ind1":"1","ind2":"#"}}},
    "200":{ " ":{"k":{"type":"df","tag":"110","ind1":"2","ind2":"#","code":"a"}}}
    }

#print (datafieldMap["001"]["m21tag"])

xmlIN = open('samples/woldan_record_aseq.xml').read()
collection = MARC21relaxed.CreateFromDocument(xmlIN)

print ('<?xml version = "1.0" encoding = "UTF-8"?>')

print('''<collection xmlns="http://www.loc.gov/MARC21/slim"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">''')

for record in collection.record:

    print('''<record xmlns="http://www.loc.gov/MARC21/slim"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.loc.gov/MARC21/slim
    http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">''')
    leader=""
    controlfields={}
    datafields={}

    for ld in record.leader:
        leader=ld.value()

    print('<leader>%s</leader>'%leader)

    for cf in record.controlfield:
        #print(controlfield.tag,controlfield.value())
        controlfields[cf.tag]=cf.value()

    for df in record.datafield:
        #print(datafield.tag,datafield.ind1,datafield.ind2)

        for sf in df.subfield:
            fieldtype =""
            tag = df.tag
            ind1 = df.ind1
            ind2 = df.ind2
            code = sf.code
            value = sf.value()

            if tag in fieldMap:
                if ind1 in fieldMap[tag]:
                    if code in fieldMap[tag][ind1]:
                        lookupCode=code
                    else:
                        lookupCode='*'
                    try:
                        fieldtype=fieldMap[df.tag][df.ind1][lookupCode]["type"]
                        tag=fieldMap[df.tag][df.ind1][lookupCode]["tag"]
                        ind1=fieldMap[df.tag][df.ind1][lookupCode]["ind1"]
                        ind2=fieldMap[df.tag][df.ind1][lookupCode]["ind2"]
                        code=fieldMap[df.tag][df.ind1][lookupCode]["code"]
                    except KeyError:
                        pass

            if fieldtype == "cf":
                controlfields[tag]=value

            elif fieldtype == "df":
                if not tag in datafields:
                    datafields[tag]={}
                if not ind1 in datafields[tag]:
                    datafields[tag][ind1]={}
                if not ind2 in datafields[tag][ind1]:
                    datafields[tag][ind1][ind2]={}
                datafields[tag][ind1][ind2][code]=value

    for tag in sorted(controlfields.iterkeys()):
        print (u'<controlfield tag="%s">%s</controlfield>'%(tag,controlfields[tag]))

    for tag in sorted(datafields.iterkeys()):
        for ind1 in sorted(datafields[tag].iterkeys()):
            for ind2 in sorted(datafields[tag][ind1].iterkeys()):
                print (u'<datafield tag="%s" ind1="%s" ind2="%s">'%(tag,ind1,ind2))
                for code in sorted(datafields[tag][ind1][ind2].iterkeys()):
                    sfstr=u'<subfield code="%s">%s</subfield>'%(code,datafields[tag][ind1][ind2][code])
                    print (sfstr.encode('utf-8'))
                print(u'</datafield>')
    print (u'</record>')
print ('</collection>')

#print(controlfields)
