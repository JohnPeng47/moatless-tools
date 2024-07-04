import re
from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel, validator, Field, root_validator
from typing_extensions import deprecated

from moatless.codeblocks.parser.comment import get_comment_symbol
from moatless.utils.colors import Colors

BlockPath = List[str]


class SpanMarker(Enum):
    TAG = 1
    COMMENT = 2


class CodeBlockTypeGroup(str, Enum):
    STRUCTURE = "Structures"
    IMPLEMENTATION = "Implementation"
    IMPORT = "Imports"

    BLOCK_DELIMITER = "BlockDelimiter"
    SPACE = "Space"

    COMMENT = "Comment"

    ERROR = "Error"


class CodeBlockType(Enum):

    MODULE = (
        "Module",
        CodeBlockTypeGroup.STRUCTURE,
    )  # TODO: Module shouldn't be a STRUCTURE
    CLASS = ("Class", CodeBlockTypeGroup.STRUCTURE)
    FUNCTION = ("Function", CodeBlockTypeGroup.STRUCTURE)

    # TODO: Remove and add sub types to functions and classes
    CONSTRUCTOR = ("Constructor", CodeBlockTypeGroup.STRUCTURE)
    TEST_SUITE = ("TestSuite", CodeBlockTypeGroup.STRUCTURE)
    TEST_CASE = ("TestCase", CodeBlockTypeGroup.STRUCTURE)

    IMPORT = ("Import", CodeBlockTypeGroup.IMPORT)

    EXPORT = ("Export", CodeBlockTypeGroup.IMPLEMENTATION)
    COMPOUND = ("Compound", CodeBlockTypeGroup.IMPLEMENTATION)
    # Dependent clauses are clauses that are dependent on another compound statement and can't be shown on their own
    DEPENDENT_CLAUSE = ("DependentClause", CodeBlockTypeGroup.IMPLEMENTATION)
    ASSIGNMENT = ("Assignment", CodeBlockTypeGroup.IMPLEMENTATION)
    CALL = ("Call", CodeBlockTypeGroup.IMPLEMENTATION)
    STATEMENT = ("Statement", CodeBlockTypeGroup.IMPLEMENTATION)

    CODE = ("Code", CodeBlockTypeGroup.IMPLEMENTATION)

    # TODO: Incorporate in code block?
    BLOCK_DELIMITER = ("BlockDelimiter", CodeBlockTypeGroup.BLOCK_DELIMITER)

    # TODO: Remove as it's just to fill upp spaces at the end of the file?
    SPACE = ("Space", CodeBlockTypeGroup.SPACE)

    COMMENT = ("Comment", CodeBlockTypeGroup.COMMENT)
    COMMENTED_OUT_CODE = (
        "Placeholder",
        CodeBlockTypeGroup.COMMENT,
    )  # TODO: Replace to PlaceholderComment

    ERROR = ("Error", CodeBlockTypeGroup.ERROR)

    def __init__(self, value: str, group: CodeBlockTypeGroup):
        self._value_ = value
        self.group = group

    @classmethod
    def from_string(cls, tag: str) -> Optional["CodeBlockType"]:
        if not tag.startswith("definition"):
            return None

        tag_to_block_type = {
            "definition.assignment": cls.ASSIGNMENT,
            "definition.block_delimiter": cls.BLOCK_DELIMITER,
            "definition.call": cls.CALL,
            "definition.class": cls.CLASS,
            "definition.code": cls.CODE,
            "definition.comment": cls.COMMENT,
            "definition.compound": cls.COMPOUND,
            "definition.constructor": cls.CONSTRUCTOR,
            "definition.dependent_clause": cls.DEPENDENT_CLAUSE,
            "definition.error": cls.ERROR,
            "definition.export": cls.EXPORT,
            "definition.function": cls.FUNCTION,
            "definition.import": cls.IMPORT,
            "definition.module": cls.MODULE,
            "definition.statement": cls.STATEMENT,
            "definition.test_suite": cls.TEST_SUITE,
            "definition.test_case": cls.TEST_CASE,
        }
        return tag_to_block_type.get(tag)
