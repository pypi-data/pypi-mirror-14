# This file is part of python-escpos-xml.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.
import base64
import warnings
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from io import BytesIO


BLOCKS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'hr'}
LISTS = {'ul', 'ol'}
OPERATIONS = {'cut', 'partialcut', 'cashdraw'}
DEFAULT_STYLE = {
    'bold': False, 'underline': None, 'size': 'normal', 'font': 'a',
    'align': 'left', 'inverted': False, 'color': 1}
DEFAULT_STYLES = {
    'h1': {'bold': True, 'size': '2x'},
    'h2': {'size': '2x'},
    'h3': {'bold': True, 'size': '2h'},
    'h4': {'size': '2h'},
    'h5': {'bold': True},
    'bold': {'bold': True},
    'b': {'bold': True},
    }


class Parser(object):

    def __init__(self, printer):
        self.printer = printer
        self.styles = []

    def parse(self, xml):
        tree = ET.parse(xml)
        root = tree.getroot()
        assert root.tag == 'receipt'
        assert not self.styles
        self.width = int(root.attrib.get('width', 0))

        for child in root:
            if child.tag in BLOCKS:
                self.parse_block(child)
            elif child.tag in LISTS:
                self.parse_list(child)
            elif child.tag in OPERATIONS:
                self.parse_operation(child)
            else:
                getattr(self, 'parse_%s' % child.tag)(child)

    def parse_block(self, element):
        style = self.get_element_style(element)
        with self.new_style(**style):
            if element.tag == 'hr':
                self.print_('-' * self.width)
            else:
                if element.text:
                    self.print_(self.strip(element.text))
                for child in element:
                    self.parse_inline(child)
            self.print_('\n')

    def parse_list(self, element, deep=0):
        count = int(element.attrib.get('start', 1))
        tabwidth = int(element.attrib.get('tabwidth', 1))
        style = self.get_element_style(element)
        with self.new_style(**style):
            for item in element:
                assert item.tag == 'li'
                style = self.get_element_style(item)
                with self.new_style(**style):
                    self.print_('{:<{}}{} '.format(
                            '', deep * tabwidth, self.bullet(element, count)))
                    if item.text:
                        self.print_(self.strip(item.text))
                    child = None
                    for child in item:
                        if child.tag in LISTS:
                            self.print_('\n')
                            self.parse_list(child, deep + 1)
                        else:
                            self.parse_inline(child)
                    if child is None or child.tag not in LISTS:
                        self.print_('\n')
                count += 1

    def bullet(self, element, count):
        default_type = {'ul': 'circle', 'ol': '1'}[element.tag]
        type_ = element.attrib.get('type', default_type)
        if type_ == 'circle':
            return '*'
        elif type_ == '1':
            return str(count)
        else:
            # TODO
            warnings.warn('list type "%s" not supported' % type_, UserWarning)
            return '*'

    def parse_inline(self, element):
        style = self.get_element_style(element)
        with self.new_style(**style):
            head, tail = self.compute_width(element)
            if head:
                self.print_(head)
            if element.text:
                self.print_(self.strip(element.text))
            for child in element:
                self.parse_inline(child)
            if tail:
                self.print_(tail)
        if element.tail:
            self.print_(self.strip(element.tail))

    def strip(self, text):
        return ''.join(filter(lambda l: l.strip(), text.splitlines()))

    def print_(self, text):
        if text:
            self.printer.text(text.encode('utf-8'))

    def compute_width(self, element):
        if element.tag != 'span' or 'width' not in element.attrib:
            return None, None
        width = int(element.attrib['width'])
        align = element.attrib.get('align', 'left')

        def all_text(element):
            text = ''
            if element.text:
                text = self.strip(element.text)
            for child in element:
                text += all_text(child)
            if element.tail:
                text += self.strip(element.tail)
            return text

        text = all_text(element)

        fmt = {
            'left': u'{:<{}}',
            'right': u'{:>{}}',
            'center': u'{:^{}}',
            }[align]
        result = fmt.format(text, width)

        head = ' ' * (
            len(result) - len(result.lstrip())
            - (len(text) - len(text.lstrip())))
        tail = ' ' * (
            len(result) - len(result.rstrip())
            - (len(text) - len(text.rstrip())))
        return head, tail

    def parse_operation(self, element):
        if element.tag == 'cashdraw':
            self.printer.cashdraw(int(element.attrib['pin']))
        else:
            self.print_('\n')
            getattr(self.printer, element.tag)()

    def parse_barcode(self, element):
        self.printer.barcode(
            element.text.strip(), element.attrib['encoding'],
            int(element.attrib.get('width', 255)),
            int(element.attrib.get('height', 2)),
            element.attrib.get('position', 'below'),
            element.attrib.get('font', 'a'))

    def parse_img(self, element):
        _, data = element.attrib['src'].split(',')
        image = BytesIO(base64.b64decode(data))
        self.printer.image(image)

    def get_element_style(self, element):
        style = DEFAULT_STYLES.get(element.tag, {}).copy()
        for name in ['bold', 'inverted']:
            if name in element.attrib:
                style[name] = bool(int(element.attrib[name]))
        for name in ['underline', 'color']:
            if name in element.attrib:
                style[name] = int(element.attrib[name])
                if name == 'underline' and not style[name]:
                    style[name] = None
        for name in ['size', 'font', 'align']:
            if name in element.attrib:
                style[name] = element.attrib[name]
        if element.tag == 'span' and 'align' in style:
            del style['align']
        return style

    @property
    def current_style(self):
        if not self.styles:
            return DEFAULT_STYLE
        return self.styles[-1]

    @contextmanager
    def new_style(self, **style):
        # TODO optimize set call with only changed style
        new_style = self.current_style.copy()
        new_style.update(style)
        self.styles.append(new_style)
        self.printer.set(**new_style)
        yield
        self.styles.pop()
        self.printer.set(**self.current_style)


def parse(printer, xml):
    Parser(printer).parse(xml)


def _main():
    # TODO
    pass
