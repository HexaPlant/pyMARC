# ./marc2aseq.py
# -*- coding: utf-8 -*-

from __future__ import print_function
import MARC21relaxed

xml = open('samples/woldan_record_aseq.xml').read()
aseq = MARC21relaxed.CreateFromDocument(xml)
print (dir (aseq))
