#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
import json
import logging
import unittest

from lxml import etree


logger = logging.getLogger('weblyzard_api.xml_content.parsers')


class XMLParser(object):
    VERSION = None
    SUPPORTED_NAMESPACE = None
    DOCUMENT_NAMESPACES = None
    ATTR_MAPPING = None
    SENTENCE_MAPPING = None
    ANNOTATION_MAPPING = None
    DEFAULT_NAMESPACE = 'wl'

    @classmethod
    def encode_value(cls, value):
        if isinstance(value, basestring):
            return value
        else:
            try:
                return json.dumps(value)
            except Exception, e:
                logger.error('could not encode %s: %s' % (value, e))
                return

    @classmethod
    def decode_value(cls, value):
        try:
            decoded = json.loads(value)
            if decoded in (float('inf'), float('-inf'), float('nan')):
                raise ValueError('deserializing of invalid json values')
            else:
                return decoded
        except ValueError as err:
            return value

    @classmethod
    def is_supported(cls, xml_content):
        return 'xmlns:wl="%s"' % cls.SUPPORTED_NAMESPACE in xml_content

        # if xml_content:
        # return any([ns in xml_content for ns in cls.get_supported_namespaces()])

    @classmethod
    def parse(cls, xml_content, remove_duplicates=True):
        ''' '''
        parser = etree.XMLParser(recover=True, strip_cdata=False)
        root = etree.fromstring(xml_content.replace('encoding="UTF-8"', ''),
                                parser=parser)
        attributes = cls.load_attributes(root.attrib,
                                         mapping=cls.ATTR_MAPPING)

        sentences = cls.load_sentences(root, page_attributes=attributes,
                                       remove_duplicates=remove_duplicates)
        title_sentence_ids = [sentence['md5sum'] for sentence in sentences \
                              if 'is_title' in sentence and sentence['is_title']]
        
        title_annotations = []
        body_annotations = []
        for annotation in cls.load_annotations(root):
            if 'md5sum' in annotation and annotation['md5sum'] in title_sentence_ids:
                title_annotations.append(annotation)
            else:
                body_annotations.append(annotation)
                
        return attributes, sentences, title_annotations, body_annotations

    @classmethod
    def load_attributes(cls, attributes, mapping):
        new_attributes = {}

        for key, value in attributes.iteritems():
            if mapping:
                key = mapping.get(key, key)

            value = cls.decode_value(value)

            if not value == 'None':
                new_attributes[key] = value

        return new_attributes

    @classmethod
    def load_annotations(cls, root):
        ''' '''
        annotations = []
        for annotation_element in root.iterfind('{%s}annotation' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):

            annotation_attrs = cls.load_attributes(annotation_element.attrib,
                                                  mapping=cls.ANNOTATION_MAPPING)
#             annotation_attrs['value'] = annotation_element.text.strip()

#             if 'md5sum' in annotation_attrs:
#                 sent_id = annotation_attrs['md5sum']
#             else:
#                 sent_id = annotation_attrs['id']
#                 annotation_attrs['md5sum'] = sent_id
#                 del annotation_attrs['id']

            annotations.append(annotation_attrs)

        return annotations
    
    @classmethod
    def load_sentences(cls, root, page_attributes=None, remove_duplicates=True):
        ''' '''
        sentences = []
        seen_sentences = []

        for sent_element in root.iterfind('{%s}sentence' % cls.get_default_ns(),
                                          namespaces=cls.DOCUMENT_NAMESPACES):

            sent_attributes = cls.load_attributes(sent_element.attrib,
                                                  mapping=cls.SENTENCE_MAPPING)
            sent_attributes['value'] = sent_element.text.strip()

            if 'md5sum' in sent_attributes:
                sent_id = sent_attributes['md5sum']
            else:
                sent_id = sent_attributes['id']
                sent_attributes['md5sum'] = sent_id
                del sent_attributes['id']

            if not sent_id in seen_sentences:
                sentences.append(sent_attributes)

                if remove_duplicates:
                    seen_sentences.append(sent_id)

        return sentences

    @classmethod
    def dump_xml_attributes(cls, attributes, mapping, keep_none_values=False):
        new_attributes = {}

        for key, value in attributes.iteritems():

            if mapping and key in mapping:
                key = mapping[key]

            if value and value not in ('None', 'null', '0.0'):
                new_attributes[key] = cls.encode_value(value)

        return new_attributes

    @classmethod
    def dump_xml(cls, titles, attributes, sentences, annotations=None):
        ''' returns attribute / sentence /annotations as a webLyzard XML document '''

        attributes, sentences = cls.pre_xml_dump(titles=titles,
                                                 attributes=attributes,
                                                 sentences=sentences)

        if attributes:
            assert isinstance(attributes, dict), 'dict required'

        if cls.ATTR_MAPPING:
            invert_mapping = dict(zip(cls.ATTR_MAPPING.values(),
                cls.ATTR_MAPPING.keys()))
        else:
            invert_mapping = None

        attributes = cls.dump_xml_attributes(attributes,
                                             mapping=invert_mapping)
        root = etree.Element('{%s}page' % cls.get_default_ns(),
                             attrib=attributes,
                             nsmap=cls.DOCUMENT_NAMESPACES)

        if cls.SENTENCE_MAPPING:
            sent_mapping = dict(zip(cls.SENTENCE_MAPPING.values(),
                cls.SENTENCE_MAPPING.keys()))
        else:
            sent_mapping = None

        for sent in sentences:
            sent = sent.as_dict()
            assert isinstance(sent, dict), 'dict required'
            value = sent['value']
            del sent['value']

            if not value:
                continue

            sent_attributes = cls.dump_xml_attributes(sent,
                                                      mapping=sent_mapping)
            sent_elem = etree.SubElement(root,
                                         '{%s}sentence' % cls.get_default_ns(),
                                         attrib=sent_attributes,
                                         nsmap=cls.DOCUMENT_NAMESPACES)
            if isinstance(value, int):
                value = str(value)
            sent_elem.text = etree.CDATA(value)
           
        if cls.ANNOTATION_MAPPING:
            annotation_mapping = dict(zip(cls.ANNOTATION_MAPPING.values(),
                                    cls.ANNOTATION_MAPPING.keys()))
        else:
            annotation_mapping = None
        if annotations:
            # add all annotations as body annotations
            for a_type, annotations in annotations.iteritems():
                for annotation in annotations:       
                    assert isinstance(annotation, dict), 'dict required'
                    if 'entities' in annotation:
                        for entity in annotation['entities']:
                            entity['annotation_type'] = a_type
                            entity['key'] = annotation['key']
                            annotation_attributes = cls.dump_xml_attributes(entity,
                                                                            mapping=annotation_mapping)
                            annotation_elem = etree.SubElement(root,
                                                               '{%s}annotation' % cls.get_default_ns(),
                                                               attrib=annotation_attributes,
                                                               nsmap=cls.DOCUMENT_NAMESPACES)
#                             if isinstance(value, int):
#                                 value = str(value)
#                             annotation_elem.text = etree.CDATA(value)

        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):
        ''' overriding this functions allows to perform custom cleanup tasks'''
        return attributes, sentences

    @classmethod
    def get_supported_namespaces(cls):
        if not isinstance(cls.SUPPORTED_NAMESPACES, list):
            return [cls.SUPPORTED_NAMESPACES]
        return cls.SUPPORTED_NAMESPACES

    @classmethod
    def get_default_ns(cls):
        return cls.SUPPORTED_NAMESPACE


class TestParser(unittest.TestCase):

    def test_scientific_notation_bug(self):
        '''
        make sure that a decoding bug for strings in scientific notation yielding infinity doesn't occur
        '''
        import hashlib

        m = hashlib.md5()
        m.update(
            "\"That triumph for more military spending was an anomaly in the budget blueprint, which would cut spending $5.5 trillion over the next decade.")
        md5sum = m.hexdigest()
        expected = '3120900866903065837e521458088467'
        self.assertEqual(md5sum, expected)
        self.assertEqual(XMLParser.decode_value(md5sum), expected)


if __name__ == '__main__':
    unittest.main()
