from collections import namedtuple

import os.path
import re

import exceptions

LineStats = namedtuple(
    "LineStats",
    ["filepath", "lines", "source_lines_of_code", "commented_lines", "blank_lines"]
)


def _inline_comment_status(line: str, in_comment: bool) -> bool | None:
    """
    Checks if the line entered, exited, or did not enter or exit an inline comment.

    :param line: The line to verify
    :param in_comment If we are currently in a commment
    :return: True if the line entered an inline comment, false if the line exited an inline comment, None if it did not
             enter or exit an inline comment
    """

    if in_comment is False:
        # Check if we are in an inline comment, but exclude the inline comment start/stop from inside a string
        # The (?<\)" regex finds " characters, but NOT \" characters.
        split_by_quote = re.split(r'(?<!\\)"', line)

        # Remove odd indices to remove items inside strings
        for i in range(len(split_by_quote) - 1, -1, -1):
            if i % 2 != 0:
                split_by_quote.pop(i)

        # Convert the list to a string to be easily-searchable
        no_quote_content = "".join([split_by_quote[i] for i in range(0, len(split_by_quote), 2)])

    else:
        no_quote_content = line

    # If the last closing inline comment is after the last opening inline comment
    # AND it is after the opening inline comment, if it exists
    if no_quote_content[::-1].find("*/") > no_quote_content[::-1].find("/*"):
        return False

    if "/*" in no_quote_content:
        return True

    return None


def count_lines_file(filepath: str):
    """
    :param filepath: The filepath of the file to count the lines of
    :return: A tuple of four values: (total lines, num commented lines, num blank lines, source lines of code)
    :raises LineCountError, when there is an issue decoding a file
    """

    lines = 0
    commented_lines = 0
    blank_lines = 0

    with open(filepath, "r") as f:
        in_comment: bool = False

        try:
            for line in f:
                lines += 1

                status = _inline_comment_status(line, in_comment)
                if status is not None:
                    in_comment = status

                if in_comment:
                    commented_lines += 1
                    continue

                if line.isspace():
                    blank_lines += 1
                    continue

                # Check if the line only has a comment in it
                split_by_slash_comment = line.split("//")
                split_by_hash_comment = line.split("#")
                split_by_inline_comment = line.split("/*")

                if split_by_slash_comment[0].isspace() or split_by_hash_comment[0].isspace() or split_by_inline_comment[0].isspace():
                    commented_lines += 1


        except UnicodeDecodeError as e:
            raise exceptions.LineCountError(f"Could not decode the file {filepath}. Is it a plaintext file?") from e

    return LineStats(
        filepath=filepath,
        lines=lines,
        source_lines_of_code=lines - blank_lines - commented_lines,
        commented_lines=commented_lines,
        blank_lines=blank_lines
    )


def count_lines_dir(dir_path: str) -> tuple[LineStats, list[LineStats]]:
    """
    Counts the lines of all files within a directory. Not recursive.

    :param dir_path: The path to the directory to count the lines of all the files inside.
    :return: A tuple of two values: a LineStats object that adds up the lines across all files, and a list of LineStats
             objects for individual files.
    """

    total_lines = 0
    total_commented_lines = 0
    total_blank_lines = 0
    total_sloc = 0  # total source lines of code

    individual_stats: list[LineStats] = []

    for file in os.listdir(dir_path):
        if not os.path.isfile(os.path.join(dir_path, file)):
            continue

        try:
            line_stats = count_lines_file(os.path.join(dir_path, file))
            individual_stats.append(line_stats)

        except exceptions.LineCountError:
            pass

        else:
            total_lines += line_stats.lines
            total_commented_lines += line_stats.commented_lines
            total_blank_lines += line_stats.blank_lines
            total_sloc += line_stats.source_lines_of_code

    return (
            LineStats(
                filepath=dir_path,
                lines=total_lines,
                source_lines_of_code=total_sloc,
                commented_lines=total_commented_lines,
                blank_lines=total_blank_lines
            ),

            individual_stats
    )


def count_lines_dir_recursive(dir_path: str) -> tuple[LineStats, list[LineStats]]:
    """
    Recursively counts the lines of all files within a directory.

    :param dir_path: The path to the directory to count the lines of all the files inside.
    :return: A tuple of two values: a LineStats object that adds up the lines across all files, and a list of LineStats
             objects for individual files.
    """

    total_lines = 0
    total_commented_lines = 0
    total_blank_lines = 0
    total_sloc = 0  # total source lines of code

    individual_stats: list[LineStats] = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            try:
                line_stats = count_lines_file(os.path.join(root, file))
                individual_stats.append(line_stats)

            except exceptions.LineCountError:
                pass

            else:
                total_lines += line_stats.lines
                total_commented_lines += line_stats.commented_lines
                total_blank_lines += line_stats.blank_lines
                total_sloc += line_stats.source_lines_of_code

    return (
        LineStats(
            filepath=dir_path,
            lines=total_lines,
            source_lines_of_code=total_sloc,
            commented_lines=total_commented_lines,
            blank_lines=total_blank_lines
        ),

        individual_stats
    )
