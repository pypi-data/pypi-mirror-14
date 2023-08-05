# This file is part of python-escpos-xml.  The COPYRIGHT file at the top level
# of this repository contains the full copyright notices and license terms.
import os
import xml.etree.ElementTree as ET
from unittest import TestCase
from io import BytesIO, open

from mock import Mock, ANY, call
from escpos.escpos import Image

from escpos_xml import Parser, parse
from escpos_xml.parser import DEFAULT_STYLE

here = os.path.dirname(__file__)


class ESCPOSTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.printer = Mock()
        self.parser = Parser(self.printer)

    def test_parse(self):
        parse(self.printer, BytesIO('<receipt></receipt>'))

    def test_receipt(self):
        self.parser.parse(BytesIO('<receipt></receipt>'))

    def test_block(self):
        self.parser.parse(BytesIO(
                '<receipt>'
                '<p></p>'
                '</receipt>'))
        self.printer.text.assert_called_once_with('\n')

    def test_hr(self):
        self.parser.parse(BytesIO(
                '<receipt width="48">'
                '<hr/>'
                '</receipt>'))
        calls = [call('-' * 48), call('\n')]
        self.printer.text.assert_has_calls(calls)

    def test_list(self):
        self.parser.parse(BytesIO(
                '<receipt>'
                '<ol>'
                '<li>foo</li>'
                '<li>bar</li>'
                '</ol>'
                '</receipt>'))
        calls = [
            call('1 '), call('foo'), call('\n'),
            call('2 '), call('bar'), call('\n')]
        self.printer.text.assert_has_calls(calls)

    def test_nested_list(self):
        self.parser.parse(BytesIO(
                '<receipt>'
                '<ol>'
                '<li>foo'
                '<ol>'
                '<li>test</li>'
                '<li>baz</li>'
                '</ol>'
                '</li>'
                '<li>bar</li>'
                '</ol>'
                '</receipt>'))
        calls = [
            call('1 '), call('foo'), call('\n'),
            call(' 1 '), call('test'), call('\n'),
            call(' 2 '), call('baz'), call('\n'),
            call('2 '), call('bar'), call('\n')]
        self.printer.text.assert_has_calls(calls)

    def test_inline(self):
        self.parser.parse(BytesIO(
                '<receipt>'
                '<p>Test <b>Foo</b> Bar</p>'
                '</receipt>'))
        calls = [call('Test '), call('Foo'), call(' Bar'), call('\n')]
        self.printer.text.assert_has_calls(calls)

    def test_compute_width(self):
        for xml, result in [
                ('<span align="center" width="9">foo</span>',
                    (' ' * 3, ' ' * 3)),
                ('<span width="9">foo</span>', ('', ' ' * 6)),
                ('<span width="9" align="right">foo</span>',
                    (' ' * 6, '')),
                ('<span width="9">foo <b>bar</b></span>',
                    ('', ' ' * 2)),
                ('<span width="2">foo</span>', ('', '')),
                ]:
            element = ET.fromstring(xml)
            self.assertEqual(
                self.parser.compute_width(element), result, msg=xml)

    def test_inline_with_width(self):
        self.parser.parse(BytesIO(
                '<receipt><p>'
                '<span align="left" width="10">foo</span>'
                '<span align="right" width="10">bar</span>'
                '</p></receipt>'))
        calls = [
            call('foo'), call('       '), call('       '), call('bar'),
            call('\n')]
        self.printer.text.assert_has_calls(calls)

    def test_operation(self):
        self.parser.parse(BytesIO(
                '<receipt>'
                '<cut/>'
                '<partialcut/>'
                '<cashdraw pin="2"/>'
                '</receipt>'))
        self.printer.cut.assert_called_once_with()
        self.printer.partialcut.assert_called_once_with()
        self.printer.text.assert_has_calls([call('\n'), call('\n')])
        self.printer.cashdraw.assert_called_once_with(2)

    def test_barcode(self):
        self.parser.parse(BytesIO(
                '<receipt>'
                '<barcode encoding="EAN13">5449000000996</barcode>'
                '</receipt>'))
        self.printer.barcode.assert_called_once_with(
            '5449000000996', 'EAN13', 255, 2, 'below', 'a')

        self.printer.reset_mock()

        self.parser.parse(BytesIO(
                '<receipt>'
                '<barcode encoding="EAN13" width="100" height="4" '
                'position="above" font="b">5449000000996</barcode>'
                '</receipt>'))
        self.printer.barcode.assert_called_once_with(
            '5449000000996', 'EAN13', 100, 4, 'above', 'b')

    def test_img(self):
        with open(os.path.join(here, 'image.xml'), 'rb') as f:
            self.parser.parse(f)
        self.printer.image.assert_called_once_with(ANY)
        image, = self.printer.image.call_args[0]
        Image.open(image)

    def test_element_style(self):
        element = Mock()
        element.tag = 'p'
        element.attrib = {
            'bold': '1', 'underline': '0', 'color': '1', 'size': '2h'}
        self.assertEqual(
            self.parser.get_element_style(element),
            {'bold': True, 'underline': None, 'color': 1, 'size': '2h'})

        element.tag = 'h1'
        element.attrib = {}
        self.assertEqual(
            self.parser.get_element_style(element),
            {'bold': True, 'size': '2x'})

        element.tag = 'span'
        element.attrib = {'align': 'left'}
        self.assertEqual(
            self.parser.get_element_style(element),
            {})

    def test_new_style(self):
        self.assertEqual(self.parser.current_style, DEFAULT_STYLE)
        with self.parser.new_style(key='test'):
            new_style = DEFAULT_STYLE.copy()
            new_style.update({'key': 'test'})
            self.assertEqual(self.parser.current_style, new_style)
            self.printer.set.assert_called_once_with(**new_style)
            self.printer.reset_mock()
        self.assertEqual(self.parser.current_style, DEFAULT_STYLE)
        self.printer.set.assert_called_once_with(**DEFAULT_STYLE)
