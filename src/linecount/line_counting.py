from collections import namedtuple

import os.path
import re

import exceptions

LineStats = namedtuple(
    "LineStats",
    ["filepath", "lines", "source_lines_of_code", "commented_lines", "blank_lines"]
)


def _add_line_stats(line_stats_1: LineStats, line_stats_2: LineStats):
    """
    Add the values of two line stats objects. Keeps the filepath of the first line stats object.

    :param line_stats_1: The first line stat to add
    :param line_stats_2: The second line stat to add
    :return: A new LineStats object with the added values
    """

    return LineStats(
        filepath=line_stats_1,
        lines=line_stats_1.lines + line_stats_2.lines,
        source_lines_of_code=line_stats_1.source_lines_of_code + line_stats_2.source_lines_of_code,
        commented_lines=line_stats_1.commented_lines + line_stats_2.commented_lines,
        blank_lines=line_stats_1.blank_lines + line_stats_2.blank_lines
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
        # Check if we are in an inline comment, but exclude_files the inline comment start/stop from inside a string
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
    # Since no_quote_content is reversed, to find the last occurence, the findstr also needs to be reversed
    if no_quote_content[::-1].find("*/"[::-1]) > no_quote_content[::-1].find("/*"[::-1]):
        return False

    if "/*" in no_quote_content:
        return True

    return None


def count_lines_file(filepath: str):
    """
    :param filepath: The filepath of the file to count the lines of
    :return: A tuple of four values: (total lines, num commented lines, num blank lines, source lines of code)
    :raises LineCountError, when there is an issue decoding a file.
            PermissionError, if you do not have permission to read the file
    """

    lines = 0
    commented_lines = 0
    blank_lines = 0

    with (open(filepath, "r") as f):
        in_comment: bool = False

        try:
            for line in f:
                lines += 1

                status = _inline_comment_status(line, in_comment)
                if status is not None:
                    in_comment = status

                    # Do this since closing multi-line comments will otherwise not be counted
                    commented_lines += 1
                    continue

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

                # Use .strip() instead of .isspace() since "".isspace() returns False
                if not split_by_slash_comment[0].strip() or \
                        not split_by_hash_comment[0].strip() or \
                        not split_by_inline_comment[0].strip():

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


def _is_excluded(file_or_dir_name: str, exclude: list[str]) -> bool:
    for exclude_item in exclude:
        if exclude_item in file_or_dir_name:
            return True

    return False


def count_lines_dir(dir_path: str, exclude_files: list[str] | None = None) -> tuple[LineStats, list[LineStats]]:
    """
    Counts the lines of all files within a directory. Not recursive.

    :param dir_path: The path to the directory to count the lines of all the files inside.
    :param exclude_files: Excludes any files containing any of the string patterns in the name

    :return: A tuple of two values: a LineStats object that adds up the lines across all files, and a list of LineStats
             objects for individual files.
    """

    if exclude_files is None:
        exclude_files = []

    summary_stats = LineStats(dir_path, 0, 0, 0, 0)

    individual_stats: list[LineStats] = []

    for file in os.listdir(dir_path):
        if not os.path.isfile(os.path.join(dir_path, file)):
            continue

        # Skip excluded files
        if _is_excluded(file, exclude_files):
            continue

        # Add the line stats if the file is not excluded
        try:
            line_stats = count_lines_file(os.path.join(dir_path, file))
            individual_stats.append(line_stats)

        except (exceptions.LineCountError, PermissionError):
            pass

        else:
            summary_stats = _add_line_stats(summary_stats, line_stats)

    return summary_stats, individual_stats


def count_lines_dir_recursive(
        dir_path: str,
        exclude_files: list[str] | None = None,
        exclude_dirs: list[str] | None = None
) -> tuple[LineStats, list[LineStats]]:
    """
    Recursively counts the lines of all files within a directory.

    :param dir_path: The path to the directory to count the lines of all the files inside.
    :param exclude_files: Excludes any files containing any of the string patterns in the name
    :param exclude_dirs: Excludes any directories containing any of the string patterns in the name
    :return: A tuple of two values: a LineStats object that adds up the lines across all files, and a list of LineStats
             objects for individual files.
    """

    if exclude_files is None:
        exclude_files = []

    if exclude_dirs is None:
        exclude_dirs = []

    summary_stats = LineStats(dir_path, 0, 0, 0, 0)

    individual_stats: list[LineStats] = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Skip excluded files
            if _is_excluded(file, exclude_files):
                continue

            # Skip excluded directories
            if _is_excluded(root[len(dir_path):], exclude_dirs):
                continue

            try:
                line_stats = count_lines_file(os.path.join(root, file))
                individual_stats.append(line_stats)

            except (exceptions.LineCountError, PermissionError):
                pass

            else:
                summary_stats = _add_line_stats(summary_stats, line_stats)

    return summary_stats, individual_stats
