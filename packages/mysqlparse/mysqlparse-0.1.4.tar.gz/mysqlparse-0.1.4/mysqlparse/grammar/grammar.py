# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from pyparsing import Literal, CaselessLiteral, Word, Upcase, delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    OneOrMore, ZeroOrMore, restOfLine, Keyword, CharsNotIn, Suppress, Or, replaceWith, \
    QuotedString

import sys


parenthesis = Forward()
parenthesis <<= "(" + ZeroOrMore(CharsNotIn("()") | parenthesis) + ")"

identifier_def = Word(alphanums + '_$`')

alter_table_stmt = Forward()

add_column_def = CaselessKeyword("ADD") + Optional(CaselessKeyword("COLUMN")) + identifier_def.setName("table_name")

#
# DATA TYPES
# 

def define_basic_type(keyword, length_name=None):
    if not length_name:
        length_name = "length"
    return CaselessKeyword(keyword) + Optional(Suppress("(") + Word(nums).setName("integer") + Suppress(")")).setResultsName(length_name)

def define_decimal_type(keyword):
    return CaselessKeyword(keyword) + Optional(Suppress("(") + Word(nums).setName("integer").setResultsName("length") + "," + Word(nums).setName("integer").setResultsName("decimals") + Suppress(")")) + Optional("UNSIGNED") + Optional("ZEROFILL")

def extend_to_character_type(type_def, binary=True):
    if binary:
        type_def += Optional("BINARY")
    return type_def + Optional(CaselessKeyword("CHARACTER SET") + identifier_def.setName("character_set").setResultsName("collation_name")) + Optional(CaselessKeyword("COLLATE") + identifier_def.setName("collation_name").setResultsName("collation_name"))

data_type_def = (
    define_basic_type("BIT") |
    
    define_basic_type("TINYINT") + Optional(CaselessKeyword("UNSIGNED")) + Optional(CaselessKeyword("ZEROFILL")) | 
    define_basic_type("SMALLINT") + Optional(CaselessKeyword("UNSIGNED")) + Optional(CaselessKeyword("ZEROFILL")) | 
    define_basic_type("MEDIUMINT") + Optional(CaselessKeyword("UNSIGNED")) + Optional(CaselessKeyword("ZEROFILL")) | 
    define_basic_type("INT") + Optional(CaselessKeyword("UNSIGNED")) + Optional(CaselessKeyword("ZEROFILL")) | 
    define_basic_type("INTEGER") + Optional(CaselessKeyword("UNSIGNED")) + Optional(CaselessKeyword("ZEROFILL")) | 
    define_basic_type("BIGINT") + Optional(CaselessKeyword("UNSIGNED")) + Optional(CaselessKeyword("ZEROFILL")) | 

    define_decimal_type("REAL") |
    define_decimal_type("DOUBLE") |
    define_decimal_type("FLOAT") |
    define_decimal_type("DECIMAL") |
    define_decimal_type("NUMERIC") |
    
    CaselessKeyword("DATE") |

    define_basic_type("TIME", "fsm") |
    define_basic_type("TIMESTAMP", "fsm") |
    define_basic_type("DATETIME", "fsm") |

    CaselessKeyword("YEAR") |

    extend_to_character_type(define_basic_type("CHAR")) |
    extend_to_character_type(CaselessKeyword("VARCHAR") + Suppress("(") + Word(nums).setName("integer").setResultsName("length") + Suppress(")")) |

    define_basic_type("BINARY") |
    CaselessKeyword("VARBINARY") + Suppress("(") + Word(nums).setName("integer").setResultsName("length") + Suppress(")") |

    CaselessKeyword("TINYBLOB") |
    CaselessKeyword("BLOB") |
    CaselessKeyword("MEDIUMBLOB") |
    CaselessKeyword("LONGBLOB") |
    
    extend_to_character_type(CaselessKeyword("TINYTEXT")) |
    extend_to_character_type(CaselessKeyword("TEXT")) |
    extend_to_character_type(CaselessKeyword("MEDIUMTEXT")) |
    extend_to_character_type(CaselessKeyword("LONGTEXT")) |

    extend_to_character_type(CaselessKeyword("ENUM") + Suppress("(") + delimitedList(identifier_def).setName("enum_values").setResultsName("values") + Suppress(")"), binary=False) |
    extend_to_character_type(CaselessKeyword("SET") + Suppress("(") + delimitedList(identifier_def).setName("enum_values").setResultsName("values") + Suppress(")"), binary=False) 
).setResultsName("data_type")

column_def = Forward()
column_def <<= (
    data_type_def +
    Optional(CaselessKeyword("NOT NULL").setParseAction(replaceWith(False)) ^ CaselessKeyword("NULL").setParseAction(replaceWith(True))).setResultsName("is_null") +
    Optional(Suppress(CaselessKeyword("DEFAULT")) + Word(alphanums + "'\"").setName("string")).setResultsName("default") +
    Optional(CaselessKeyword("AUTO_INCREMENT")).setResultsName("auto_increment").setParseAction(replaceWith(True)) +
    Optional(Or([(CaselessKeyword("UNIQUE") + Optional(CaselessKeyword("KEY"))).setParseAction(replaceWith("unique_key")), (Optional(CaselessKeyword("PRIMARY")) + CaselessKeyword("KEY")).setParseAction(replaceWith("primary_key"))]).setResultsName("index_type")) +
    Optional(CaselessKeyword("COMMENT") + Or([QuotedString("'"), QuotedString('"')]).setResultsName("comment"))
)



table_options_def = (
    CaselessKeyword("ENGINE") + Optional("=") + identifier_def.setName("table_engine") |
    CaselessKeyword("AUTOINCREMENT") + Optional("=") + Word(nums).setName("table_autoincrement") |
    CaselessKeyword("AVG_ROW_LENGTH") + Optional("=") + Word(nums).setName("table_avg_row_length") |
    Optional("DEFAULT") + CaselessKeyword("CHARACTER") + CaselessKeyword("SET") + Optional("=") + identifier_def.setName("table_charset")
)

def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv)
