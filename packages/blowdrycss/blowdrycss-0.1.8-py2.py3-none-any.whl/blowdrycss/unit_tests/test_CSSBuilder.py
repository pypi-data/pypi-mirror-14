# python 2
# from lib2to3.fixes import fix_set_literal  http://python-future.org/futurize.html?highlight=set
# builtins
import sys
from unittest import TestCase, main

# custom
from blowdrycss.utilities import change_settings_for_testing
from blowdrycss.classpropertyparser import ClassPropertyParser
from blowdrycss.cssbuilder import CSSBuilder

__author__ = 'chad nelson'
__project__ = 'blowdrycss'

# required for pycharm unittest feature to work under both python 2.7 and python 3.x
if sys.hexversion < 0x03000000:
    import blowdrycss.blowdrycss_settings as settings
else:
    import blowdrycss_settings as settings

change_settings_for_testing()


class TestCSSStyleBuilder(TestCase):
    def test_get_css_text_sets(self):
        # TODO: Check back at bitbucket cssutils to see if a resolution is available.
        # 'rem' units are raise an error in cssutils.css.CSSStyleRule.
        # https://bitbucket.org/cthedot/cssutils/issues/60/using-units-of-rem-produces-an-invalid
        class_set = {
            'cue-x5_0p', 'margin-top-10', 'bgc-h000', 'hide', 'margin-20', 'padding-top-10', 'height-200', 'padding-10',
            'valign-middle', 'b', 'width-150', 'width-50', 'font-size-48', 'c-blue', 'margin-top-50px',
            'text-align-center', 'height-50px', 'height-150px', 'bold', 'color-hfff', 'padding-b1 a5 c1% e5',
            'margin-1a% 10x% 3q% 1mp3', 'font-size-1_23rem'
        }
        expected_clean_set = {
            'margin-top-10', 'margin-20', 'padding-top-10', 'height-200', 'padding-10', 'width-150', 'width-50',
            'font-size-48',
            'c-blue', 'height-150px', 'bgc-h000', 'bold', 'color-hfff', 'height-50px', 'text-align-center',
            'margin-top-50px', 'valign-middle', 'font-size-1_23rem'
        }
        expected_removed_set = {
            'cue-x5_0p (cssutils invalid property value: x5.0%)',
            'hide (property_name not found in property_alias_dict.)',
            'padding-b1 a5 c1% e5 (Only a-z, 0-9, "_", and "-" are allowed in class name.)',
            'b (property_name not found in property_alias_dict.)',
            'margin-1a% 10x% 3q% 1mp3 (Only a-z, 0-9, "_", and "-" are allowed in class name.)'
        }
        property_parser = ClassPropertyParser(class_set=class_set)
        style_builder = CSSBuilder(property_parser=property_parser)
        self.assertTrue(style_builder.property_parser.class_set == expected_clean_set,
                        msg=style_builder.property_parser.class_set)
        self.assertTrue(style_builder.property_parser.removed_class_set == expected_removed_set,
                        msg=style_builder.property_parser.removed_class_set)

    def test_get_css_text_output_convert_to_em(self):
        class_set = {
            'margin-top-10', 'bgc-h000', 'hide', 'margin-20', 'padding-top-10', 'height-200', 'padding-10',
            'valign-middle', 'b', 'width-150', 'width-50', 'font-size-48', 'c-blue', 'margin-top-50px',
            'text-align-center', 'height-50px', 'height-150px', 'bold', 'color-hfff'
        }
        expected_properties = [
            'background-color: #000', 'vertical-align: middle', 'color: blue', 'margin-top: 3.125em',
            'text-align: center', 'height: 3.125em', 'height: 9.375em', 'font-weight: bold', 'color: #fff'
        ]
        property_parser = ClassPropertyParser(class_set=class_set)
        css_builder = CSSBuilder(property_parser=property_parser)
        css_text = css_builder.get_css_text().decode('utf-8')

        for expected in expected_properties:
            self.assertTrue(expected in css_text, msg=expected + ' and ' + css_text)
            if expected in css_text:
                css_text = css_text.replace(expected, '')

    def test_get_css_text_output_no_conversion(self):
        class_set = {
            'margin-top-10', 'bgc-h000', 'hide', 'margin-20', 'padding-top-10', 'height-200', 'padding-10',
            'valign-middle', 'b', 'width-150', 'width-50', 'font-size-48', 'c-blue', 'margin-top-50px',
            'text-align-center', 'height-50px', 'height-150px', 'bold', 'color-hfff',
        }
        expected_properties = [
            'background-color: #000', 'vertical-align: middle', 'color: blue', 'margin-top: 50px',
            'text-align: center', 'height: 50px', 'height: 150px', 'font-weight: bold', 'color: #fff',
        ]
        settings.use_em = False
        property_parser = ClassPropertyParser(class_set=class_set)
        css_builder = CSSBuilder(property_parser=property_parser)
        css_text = css_builder.get_css_text().decode('utf-8')

        for expected in expected_properties:
            self.assertTrue(expected in css_text, msg=expected + ' and ' + css_text)
            if expected in css_text:
                css_text = css_text.replace(expected, '')

        settings.use_em = True

if __name__ == '__main__':
    main()
