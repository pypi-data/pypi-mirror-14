# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Lars Asplund lars.anders.asplund@gmail.com

"""
Module containing the CodecVHDLRecordType class.
"""
from string import Template
from vunit.vhdl_parser import VHDLRecordType
from vunit.com.codec_datatype_template import DatatypeStdCodecTemplate, DatatypeDebugCodecTemplate


class CodecVHDLRecordType(VHDLRecordType):
    """Class derived from VHDLRecordType to provide codec generator functionality for the record type."""
    def generate_codecs_and_support_functions(self, debug=False):
        """Generate codecs and communication support functions for the record type."""
        if not debug:
            template = RecordStdCodecTemplate()
        else:
            template = RecordDebugCodecTemplate()

        declarations = ''
        definitions = ''

        declarations += template.codec_declarations.substitute(type=self.identifier)
        declarations += template.to_string_declarations.substitute(type=self.identifier)
        element_encoding_list = []
        element_decoding_list = []
        num_of_elements = 0
        for element in self.elements:
            for i in element.identifier_list:
                element_encoding_list.append('encode(data.%s)' % i)
                if debug:
                    element_decoding_list.append('ret_val.%s := decode(elements.all(%d).all);' %
                                                 (i, num_of_elements))
                else:
                    element_decoding_list.append('decode(code, index, result.%s);' % i)

                num_of_elements += 1
        if debug:
            element_encodings = ', '.join(element_encoding_list)
        else:
            element_encodings = ' & '.join(element_encoding_list)

        element_decodings = '\n    '.join(element_decoding_list)
        definitions += template.record_codec_definition.substitute(type=self.identifier,
                                                                   element_encodings=element_encodings,
                                                                   num_of_elements=str(num_of_elements),
                                                                   element_decodings=element_decodings)
        definitions += template.record_to_string_definition.substitute(
            type=self.identifier,
            element_encoding_list=', '.join(element_encoding_list),
            num_of_elements=str(num_of_elements))

        return declarations, definitions


class RecordCodecTemplate(object):
    """This class contains record templates common to both standard and debug codecs."""

    record_to_string_definition = Template("""\
  function to_string (
    constant data : $type)
    return string is
  begin
    return create_group($num_of_elements, $element_encoding_list);
  end function to_string;
""")


class RecordStdCodecTemplate(DatatypeStdCodecTemplate, RecordCodecTemplate):
    """This class contains standard record templates."""

    record_codec_definition = Template("""\
  function encode (
    constant data : $type)
    return string is
  begin
    return $element_encodings;
  end function encode;

  procedure decode (
    constant code   : string;
    variable index : inout   positive;
    variable result : out $type) is
  begin
    $element_decodings
  end procedure decode;

  function decode (
    constant code : string)
    return $type is
    variable ret_val : $type;
    variable index : positive := code'left;
  begin
    decode(code, index, ret_val);

    return ret_val;
  end function decode;

""")


class RecordDebugCodecTemplate(DatatypeDebugCodecTemplate, RecordCodecTemplate):
    """This class contains debug record templates."""

    record_codec_definition = Template("""\
  function encode (
    constant data : $type)
    return string is
  begin
    return to_string(data);
  end function encode;

  function decode (
    constant code : string)
    return $type is
    variable ret_val : $type;
    variable elements : lines_t;
    variable length : natural;
  begin
    split_group(code, elements, $num_of_elements, length);
    $element_decodings
    deallocate_elements(elements);

    return ret_val;
  end function decode;

""")
