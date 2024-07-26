import unittest
from unittest.mock import patch, MagicMock
import hopenai
import snippets
import sys; sys.path.append("/data")
import helpers.hunit_test as hunit_test

# ##############################################################################


class Test_remove_comments1(hunit_test.TestCase):

    def test1(self) -> None:
        # Prepare inputs.
        func = snippets.get_functions("code_snippets1")[0]
        # Test.
        act = snippets.remove_comments(func)
        # Check.
        exp = '''
def test(
    dir_name: str,
) -> str:
    """
    Test.

    :param dir_name: path to the directory where to look for files
    """
    _ = dir_name, pattern
    return "test"
'''
        self.assert_equal(act, exp, fuzzy_match=True)


class Test_remove_docstring1(hunit_test.TestCase):

    def test1(self) -> None:
        # Prepare inputs.
        func = snippets.get_functions("code_snippets1")[0]
        # Test.
        act = snippets.remove_docstring(func)
        # Check.
        exp = '''
def test(
    dir_name: str,
) -> str:
    _ = dir_name, pattern
    # Hello.
    return "test"
'''
        self.assert_equal(act, exp, fuzzy_match=True)


class Test_get_in_out_functions1(hunit_test.TestCase):

    def test1(self) -> None:
        in_outs = snippets.get_in_out_functions("code_snippets1",
                                                "remove_docstring")
        # Test.
        act = str(in_outs[0])
        # Check.
        exp = r'''
Input:
'
def test(
    dir_name: str,
) -> str:
    _ = dir_name, pattern
    # Hello.
    return "test"
'
Output:
'
def test(
    dir_name: str,
) -> str:
    """
Test.

:param dir_name: path to the directory where to look for files
    """
    _ = dir_name, pattern
    # Hello.
    return "test"
'
        '''
        self.assert_equal(act, exp, fuzzy_match=True)


class Test_get_in_out_functions1(hunit_test.TestCase):

    def test1(self) -> None:
        function_tag = "code_snippets1"
        transform_tag = "remove_docstring"
        prompt_tag = "docstring"
        act = snippets.eval_prompt(function_tag, transform_tag, prompt_tag,
                             save_to_file=False)
        print(act)
        assert 0
        # Check.
        exp = r'''
        '''
        self.assert_equal(act, exp, fuzzy_match=True)
