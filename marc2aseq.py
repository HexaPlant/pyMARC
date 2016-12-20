# ./marc2MARC.py
# -*- coding: utf-8 -*-

from __future__ import print_function
import MARC21relaxed
import pyxb


fieldMap={
    "001":{ " ":{"":{"tag":"001"}}},
    "002":{ "b":{"a":{"tag":"002"}}},
    "003":{ " ":{"":{"tag":"003"}}},
    "010":{ " ":{"a":{"tag":"773","ind1":"9","ind2":"#","code":"w"}}},
    "034":{ " ":{"":{"tag":"034","ind1":"1","ind2":"#"}}},
    "200":{ " ":{"k":{"tag":"110","ind1":"2","ind2":"#","code":"a"}}},
    "089":{ " ":{"n":{"tag":"245","ind1":"0","ind2":"0","code":"n"}}},
    "036":{ "a":{"a":{"tag":"044","ind1":"#","ind2":"#","code":"c"}}},
    "037":{ "b":{"a":{"tag":"041","ind1":"#","ind2":"7","code":"a"}}},
    "064":{ "a":{"a":{"tag":"655","ind1":"#","ind2":"7","code":"a"}},
            "9":{"":{"tag":"655","ind1":"#","ind2":"7","code":"0"}}},
    "089":{ " ":{"":{"tag":"245","ind1":"0","ind2":"0"}}},
    "090":{ " ":{"":{"tag":"773","ind1":"0","ind2":"#","code":"q"}}},
    "100":{ " ":{"p":{"tag":"100","ind1":"1","ind2":"#","code":"a"}}},
    "200":{ " ":{"k":{"tag":"110","ind1":"2","ind2":"#","code":"a"}},
            " ":{"b":{"tag":"110","ind1":"2","ind2":"#","code":"b"}},
            " ":{"h":{"tag":"110","ind1":"2","ind2":"#","code":"g"}},
            " ":{"9":{"tag":"110","ind1":"2","ind2":"#","code":"0"}},
            "b":{"k":{"tag":"110","ind1":"2","ind2":"#","code":"a"}},
            "b":{"h":{"tag":"110","ind1":"2","ind2":"#","code":"g"}},
            "b":{"9":{"tag":"110","ind1":"2","ind2":"#","code":"0"}}},
    "331":{ " ":{"":{"tag":"245","ind1":"0","ind2":"0"}},
            "_":{"a":{"tag":"765","ind1":"0","ind2":"#","code":"t"}}},
    "370":{ "a":{"":{"tag":"246","ind1":"0","ind2":"3"}}},
    "403":{ " ":{"":{"tag":"250","ind1":"#","ind2":"#"}}},
    "407":{ " ":{"":{"tag":"255","ind1":"#","ind2":"#"}}},
    "419":{ " ":{"":{"tag":"264","ind1":"#","ind2":"1"}},
            "c":{"":{"tag":"264","ind1":"#","ind2":"3"}}},
    "433":{ " ":{"":{"tag":"300","ind1":"#","ind2":"#"}}},
    "590":{ " ":{"a":{"tag":"773","ind1":"#","ind2":"#","code":"t"}}},
    "594":{ " ":{"a":{"tag":"773","ind1":"#","ind2":"#","code":"d"}}},
    "595":{ " ":{"a":{"tag":"773","ind1":"#","ind2":"#","code":"d"}}},
    "596":{ "a":{"a":{"tag":"773","ind1":"#","ind2":"#","code":"g"}}},
    "599":{ " ":{"a":{"tag":"773","ind1":"#","ind2":"#","code":"w"}}},
    "676":{ " ":{"g":{"tag":"751","ind1":"#","ind2":"#","code":"a"}},
            " ":{"9":{"tag":"751","ind1":"#","ind2":"#","code":"0"}},
            " ":{" ":{"tag":"751","ind1":"#","ind2":"#","code":"2"}}},
    "677":{ " ":{"p":{"tag":"700","ind1":"1","ind2":"#","code":"a"}},
            " ":{"9":{"tag":"700","ind1":"1","ind2":"#","code":"0"}},
            " ":{"4":{"tag":"700","ind1":"1","ind2":"#","code":"4"}},
            " ":{"k":{"tag":"700","ind1":"1","ind2":"#","code":"a"}},
            " ":{"9":{"tag":"700","ind1":"1","ind2":"#","code":"0"}},
            " ":{"4":{"tag":"700","ind1":"1","ind2":"#","code":"4"}}},
    }

#print (datafieldMap["001"]["m21tag"])

xmlIN = open('samples/woldan_aseq.xml').read()
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
                        lookupCode=''

                    tagNew=""
                    ind1New=""
                    ind2New=""
                    codeNew=""

                    try:
                        #fieldtype=fieldMap[df.tag][df.ind1][lookupCode]["type"]
                        tagNew=fieldMap[tag][ind1][lookupCode]["tag"]
                        ind1New=fieldMap[tag][ind1][lookupCode]["ind1"]
                        ind2New=fieldMap[tag][ind1][lookupCode]["ind2"]
                        codeNew=fieldMap[tag][ind1][lookupCode]["code"]
                    except KeyError:
                        pass

                    if tagNew:
                        tag=tagNew
                    if ind1New:
                        ind1=ind1New
                    if ind2New:
                        ind2=ind2New
                    if codeNew:
                        code=codeNew

            if tagNew and not ind1New and not ind2New:
                controlfields[tag]=value

            else:
            #elif tagNew and ind1New and ind2New :
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
                    print (sfstr.replace(u'&','&amp;').encode('utf-8'))
                print(u'</datafield>')
    print (u'</record>')
print (u'</collection>')

#print(controlfields)
