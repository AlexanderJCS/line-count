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


def test_dir_no_recursive():
    summary_stats, specific_stats = lc.count_lines_dir("testfiles/test_dir")

    assert len(specific_stats) == 2
    assert summary_stats.lines == 10 * len(specific_stats)
    assert summary_stats.commented_lines == 2 * len(specific_stats)
    assert summary_stats.source_lines_of_code == 4 * len(specific_stats)
    assert summary_stats.blank_lines == 4 * len(specific_stats)


def test_dir_recursive():
    summary_stats, specific_stats = lc.count_lines_dir_recursive("testfiles/test_dir")

    assert len(specific_stats) == 3
    assert summary_stats.lines == 10 * len(specific_stats)
    assert summary_stats.commented_lines == 2 * len(specific_stats)
    assert summary_stats.source_lines_of_code == 4 * len(specific_stats)
    assert summary_stats.blank_lines == 4 * len(specific_stats)
