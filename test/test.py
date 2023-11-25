import src.linecount.line_counting as lc


def test_line_count():
    assert lc.count_lines_file("testfiles/test_lines.txt").lines == 10


def test_comment_count_simple():
    # Testing of "simple" inline comments
    assert lc.count_lines_file("testfiles/test_comments_simple.txt").commented_lines == 8


def test_comment_count_advanced():
    # Test excluding comments inside quotes, since strings do not contain comments
    assert lc.count_lines_file("testfiles/test_comments_advanced.txt").commented_lines == 1


def test_source_lines_of_code():
    assert lc.count_lines_file("testfiles/test_sloc.txt").source_lines_of_code == 5
