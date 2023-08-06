# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

import xml.etree.ElementTree as etree
from xml.etree.ElementTree import SubElement

from superdesk.publish.formatters import Formatter
import superdesk
from superdesk.errors import FormatterError
from superdesk.metadata.item import ITEM_TYPE, CONTENT_TYPE, EMBARGO
from apps.archive.common import get_utc_schedule


class NITFFormatter(Formatter):
    """
    NITF Formatter
    """
    XML_ROOT = '<?xml version="1.0"?>'

    _message_attrib = {'version': "-//IPTC//DTD NITF 3.6//EN"}

    _schema_uri = 'http://www.iptc.org/std/NITF/3.6/specification'
    _schema_ref = 'http://www.iptc.org/std/NITF/3.6/specification/nitf-3-6.xsd'
    _debug_message_extra = {
        'schemaLocation': '{} {}'.format(_schema_uri, _schema_ref)}

    def format(self, article, subscriber):
        try:
            pub_seq_num = superdesk.get_resource_service('subscribers').generate_sequence_number(subscriber)

            nitf = self.get_nitf(article, subscriber, pub_seq_num)
            return [(pub_seq_num, self.XML_ROOT + etree.tostring(nitf).decode('utf-8'))]
        except Exception as ex:
            raise FormatterError.nitfFormatterError(ex, subscriber)

    def get_nitf(self, article, destination, pub_seq_num):
        self._message_attrib.update(self._debug_message_extra)
        nitf = etree.Element("nitf", attrib=self._message_attrib)
        head = SubElement(nitf, "head")
        body = SubElement(nitf, "body")
        body_head = SubElement(body, "body.head")
        body_content = SubElement(body, "body.content")

        self.map_html_to_xml(body_content, self.append_body_footer(article))

        body_end = SubElement(body, "body.end")

        self.__append_meta(article, head, destination, pub_seq_num)
        self.__format_head(article, head)
        self.__format_body_head(article, body_head)
        self.__format_body_end(article, body_end)
        return nitf

    def __format_head(self, article, head):
        title = SubElement(head, 'title')
        title.text = article.get('headline', '')

        tobject = SubElement(head, 'tobject', {'tobject.type': 'news'})
        if 'genre' in article and len(article['genre']) > 0:
            SubElement(tobject, 'tobject.property', {'tobject.property.type': article['genre'][0]['name']})
        self.__format_subjects(article, tobject)

        if article.get(EMBARGO):
            docdata = SubElement(head, 'docdata', {'management-status': 'embargoed'})
            SubElement(docdata, 'date.expire',
                       {'norm': str(get_utc_schedule(article, EMBARGO).isoformat())})
        else:
            docdata = SubElement(head, 'docdata', {'management-status': article.get('pubstatus', '')})
            SubElement(docdata, 'date.expire', {'norm': str(article.get('expiry', ''))})

        SubElement(docdata, 'urgency', {'ed-urg': str(article.get('urgency', ''))})
        SubElement(docdata, 'date.issue', {'norm': str(article.get('firstcreated', ''))})
        SubElement(docdata, 'doc-id', attrib={'id-string': article.get('guid', '')})

        if article.get('ednote'):
            SubElement(docdata, 'ed-msg', {'info': article.get('ednote', '')})

        self.__format_keywords(article, head)

    def __format_subjects(self, article, tobject):
        for subject in article.get('subject', []):
            SubElement(tobject, 'tobject.subject',
                       {'tobject.subject.refnum': subject.get('qcode', '')})

    def __format_keywords(self, article, head):
        if article.get('keywords'):
            keylist = SubElement(head, 'key-list')
            for keyword in article['keywords']:
                SubElement(keylist, 'keyword', {'key': keyword})

    def __format_body_head(self, article, body_head):
        hedline = SubElement(body_head, 'hedline')
        hl1 = SubElement(hedline, 'hl1')
        hl1.text = article.get('headline', '')

        if article.get('byline'):
            byline = SubElement(body_head, 'byline')
            byline.text = "By " + article['byline']

        if article.get('dateline', {}).get('text'):
            dateline = SubElement(body_head, 'dateline')
            dateline.text = article['dateline']['text']

        if article.get('abstract'):
            abstract = SubElement(body_head, 'abstract')
            self.map_html_to_xml(abstract, article.get('abstract'))

        for company in article.get('company_codes', []):
            org = SubElement(body_head, 'org', attrib={'idsrc': company.get('security_exchange', ''),
                                                       'value': company.get('qcode', '')})
            org.text = company.get('name', '')

    def __format_body_end(self, article, body_end):
        if article.get('ednote'):
            tagline = SubElement(body_end, 'tagline')
            tagline.text = article['ednote']

    def can_format(self, format_type, article):
        return format_type == 'nitf' and \
            article[ITEM_TYPE] in (CONTENT_TYPE.TEXT, CONTENT_TYPE.PREFORMATTED, CONTENT_TYPE.COMPOSITE)

    def __append_meta(self, article, head, destination, pub_seq_num):
        """
        Appends <meta> elements to <head>
        """

        SubElement(head, 'meta', {'name': 'anpa-sequence', 'content': str(pub_seq_num)})
        SubElement(head, 'meta', {'name': 'anpa-keyword', 'content': self.append_legal(article)})
        SubElement(head, 'meta', {'name': 'anpa-takekey', 'content': article.get('anpa_take_key', '')})
        if 'anpa_category' in article and article['anpa_category'] is not None and len(
                article.get('anpa_category')) > 0:
            SubElement(head, 'meta',
                       {'name': 'anpa-category', 'content': article.get('anpa_category')[0].get('qcode', '')})

        if 'priority' in article:
            SubElement(head, 'meta', {'name': 'aap-priority', 'content': str(article.get('priority', '3'))})
        original_creator = superdesk.get_resource_service('users').find_one(req=None,
                                                                            _id=article.get('original_creator', ''))
        if original_creator:
            SubElement(head, 'meta', {'name': 'aap-original-creator', 'content': original_creator.get('username')})
        version_creator = superdesk.get_resource_service('users').find_one(req=None,
                                                                           _id=article.get('version_creator', ''))
        if version_creator:
            SubElement(head, 'meta', {'name': 'aap-version-creator', 'content': version_creator.get('username')})

        if article.get('task', {}).get('desk') is not None:
            desk = superdesk.get_resource_service('desks').find_one(_id=article.get('task', {}).get('desk'), req=None)
            SubElement(head, 'meta', {'name': 'aap-desk', 'content': desk.get('name', '')})
        if article.get('task', {}).get('stage') is not None:
            stage = superdesk.get_resource_service('stages').find_one(_id=article.get('task', {}).get('stage'),
                                                                      req=None)
            if stage is not None:
                SubElement(head, 'meta', {'name': 'aap-stage', 'content': stage.get('name', '')})

        SubElement(head, 'meta', {'name': 'aap-source', 'content': article.get('source', '')})
        SubElement(head, 'meta', {'name': 'aap-original-source', 'content': article.get('original_source', '')})

        if 'place' in article and article['place'] is not None and len(article.get('place', [])) > 0:
            SubElement(head, 'meta', {'name': 'aap-place', 'content': article.get('place')[0]['qcode']})
