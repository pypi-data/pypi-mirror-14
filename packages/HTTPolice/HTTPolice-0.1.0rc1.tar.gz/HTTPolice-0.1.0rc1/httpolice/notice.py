# -*- coding: utf-8; -*-

import copy
import six

import lxml.etree
import pkg_resources

from httpolice import citation, structure


ERROR = 'error'
COMMENT = 'comment'
DEBUG = 'debug'


known_map = {
    'auth': structure.AuthScheme,
    'cache': structure.CacheDirective,
    'cc': structure.ContentCoding,
    'h': structure.FieldName,
    'hsts': structure.HSTSDirective,
    'm': structure.Method,
    'media': structure.MediaType,
    'st': structure.StatusCode,
    'tc': structure.TransferCoding,
    'warn': structure.WarnCode,
}


class Notice(lxml.etree.ElementBase):

    id = property(lambda self: int(self.get('id')))
    severity = property(lambda self: self.tag)
    severity_short = property(lambda self: self.severity[0].upper())
    title = property(lambda self: self.find('title').content)

    @property
    def explanation(self):
        for child in self:
            if isinstance(child, Title) or child.tag is lxml.etree.Comment:
                continue
            elif isinstance(child, (Paragraph, ExceptionDetails, Ref)):
                yield child
            else:
                # Assume that a wrapping ``<explain/>`` was omitted.
                para = _parser.makeelement('explain')
                para.append(copy.deepcopy(child))
                yield para


class Content(lxml.etree.ElementBase):

    @property
    def content(self):
        r = [self.text]
        for child in self:
            r.append(child)
            r.append(child.tail)
        r = [piece for piece in r if piece is not None and piece != u'']

        # Strip spaces from the first and last text children.
        # Useful for quotes.
        if r:
            if isinstance(r[0], (six.text_type, bytes)):
                r[0] = r[0].lstrip()
            if isinstance(r[-1], (six.text_type, bytes)):
                r[-1] = r[-1].rstrip()

        return r


class Paragraph(Content):

    pass


class Title(Content):

    pass


class Ref(lxml.etree.ElementBase):

    reference = property(lambda self: self.get('to').split('.'))


class Var(Ref):

    reference = property(lambda self: self.get('ref').split('.'))


class ExceptionDetails(lxml.etree.ElementBase):

    pass


class Cite(Content):

    @property
    def info(self):
        return citation.Citation(self.get('title'), self.get('url'))


class CiteRFC(Cite):

    @property
    def info(self):
        num = int(self.get('num'))
        if self.get('sect'):
            sect = tuple(int(n) for n in self.get('sect').split('.'))
        else:
            sect = None
        errata = int(self.get('errata')) if self.get('errata') else None
        return citation.RFC(num, section=sect, errata=errata)


class Known(lxml.etree.ElementBase):

    content = property(lambda self: known_map[self.tag](self.text))


def _load_notices():
    lookup = lxml.etree.ElementNamespaceClassLookup()
    parser = lxml.etree.XMLParser()
    parser.set_element_class_lookup(lookup)
    ns = lookup.get_namespace(None)
    for tag in [ERROR, COMMENT, DEBUG]:
        ns[tag] = Notice
    ns['title'] = Title
    ns['explain'] = Paragraph
    ns['exception'] = ExceptionDetails
    ns['var'] = Var
    ns['ref'] = Ref
    ns['cite'] = Cite
    ns['rfc'] = CiteRFC
    for tag in known_map:
        ns[tag] = Known
    notices_xml = pkg_resources.resource_stream('httpolice', 'notices.xml')
    tree = lxml.etree.parse(notices_xml, parser)
    r = {}
    for elem in tree.getroot():
        if isinstance(elem, Notice):
            assert elem.id not in r
            r[elem.id] = elem
    return r, parser

(notices, _parser) = _load_notices()
