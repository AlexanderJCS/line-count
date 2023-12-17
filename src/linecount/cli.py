import argparse
import os.path

from . import line_counting as lc


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="LineCount",
        description="Counts the number of lines in a file, all files in a directory, "
                    "or all files in the directory and subdirectories"
    )

    parser.add_argument(
        "file_or_dir",
        help="The file or directory to count the lines of. If you want to include all "
             "files in this directory, use a \".\""
    )

    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="If the program should search subdirectories"
    )

    parser.add_argument(
        "-ef", "--excludefiles",
        help="Excludes any files containing the comma separated values given. e.g., \".txt,.cpp\" will "
             "exclude_files any text files containing .txt or .cpp in their name."
    )

    parser.add_argument(
        "-if", "--includefiles",
        help="When this argument is not blank, it will only include files that contain the string pattern."
             "e.g., \".py,.cpp\" will make this program only count the lines of files that have .py or .cpp "
             "in their name."
    )

    parser.add_argument(
        "-ed", "--excludedirs",
        help="Excludes any directories containing the comma separated values given. e.g., \".git,images\" will "
             "exclude_files any directories containing .git or images in their name."
    )

    return parser.parse_args()


def _get_average(summary_stats: lc.LineStats, num_files: int) -> lc.LineStats:
    """
    Gets the average of a list of line stats objects.

    :param summary_stats: A LineStats object that contains the data from all other LineStats objects summed up
    :param num_files: The number of LineStats objects that summary_stats contains data of
    :return: A LineCount object containing the average data from the line stats list
    """

    return lc.LineStats(
        filepath="AVERAGE",
        lines=round(summary_stats.lines / num_files) if num_files != 0 else 0,
        source_lines_of_code=round(summary_stats.source_lines_of_code / num_files) if num_files != 0 else 0,
        commented_lines=round(summary_stats.commented_lines / num_files) if num_files != 0 else 0,
        blank_lines=round(summary_stats.blank_lines / num_files) if num_files != 0 else 0
    )


def _print_row(stat: lc.LineStats, filepath_col_width: int, num_col_width) -> None:
    """
    Prints a row of LineStats data. Used for the print_table function.

    :param stat: The line stats object to display data of
    :param filepath_col_width: The width of the filepath column
    :param num_col_width: The width of numerical columns, or columns containing numbers
    """
    print(
        f"{stat.filepath:<{filepath_col_width}}|"
        f"{stat.lines:^{num_col_width}}|"
        f"{stat.source_lines_of_code:^{num_col_width}}|"
        f"{stat.commented_lines:^{num_col_width}}|"
        f"{stat.blank_lines:^{num_col_width}}"
    )


def print_table(summary_stats: lc.LineStats, individual_stats: list[lc.LineStats]) -> None:
    """
    Prints a table with the provided data.
    :param summary_stats: All the items from invidual_stats added up.
    :param individual_stats:
    :return:
    """

    num_col_width = 10  # numerical column width, the width for columns containing numbers

    filepath_col_width = len("FILEPATH")
    for stat in individual_stats:
        if len(stat.filepath) > filepath_col_width:
            filepath_col_width = len(stat.filepath)

    filepath_col_width += 1

    print(
        f"{'FILEPATH':^{filepath_col_width}}|"
        f"{'LINES':^{num_col_width}}|"
        f"{'SLOC':^{num_col_width}}|"
        f"{'COMMENT':^{num_col_width}}|"
        f"{'BLANK':^{num_col_width}}"
    )

    print("-" * (filepath_col_width + num_col_width * 4 + 4))

    for stat in individual_stats:
        _print_row(stat, filepath_col_width, num_col_width)

    # No need to print summary stats for one item
    if len(individual_stats) == 1:
        return

    # Avoid printing 2 lines in a row
    if len(individual_stats) != 0:
        print("-" * (filepath_col_width + num_col_width * 4 + 4))

    summary_stats = summary_stats._replace(filepath="TOTAL")
    average_stats = _get_average(summary_stats, len(individual_stats))

    _print_row(average_stats, filepath_col_width, num_col_width)
    _print_row(summary_stats, filepath_col_width, num_col_width)


def cli():
    args = get_args()

    # Replace * for a . since otherwise it won't work properly
    if args.file_or_dir == "*":
        args.file_or_dir = ""

    args.excludefiles = [] if args.excludefiles is None else args.excludefiles.split(",")
    args.includefiles = [] if args.includefiles is None else args.includefiles.split(",")
    args.excludedirs = [] if args.excludedirs is None else args.excludedirs.split(",")

    if not os.path.exists(args.file_or_dir):
        print(f"The path {args.file_or_dir} does not exist!")
        return

    if os.path.isfile(args.file_or_dir):
        try:
            stats = lc.count_lines_file(args.file_or_dir)

        except PermissionError:
            print("You do not have permission to read that file!")

        else:
            print_table(stats, [stats])

    elif args.recursive is True:
        summary_stats, indivdual_stats = lc.count_lines_dir_recursive(
            args.file_or_dir,
            exclude_files=args.excludefiles,
            include_files=args.includefiles,
            exclude_dirs=args.excludedirs
        )

        print_table(summary_stats, indivdual_stats)

    else:
        summary_stats, individual_stats = lc.count_lines_dir(
            args.file_or_dir,
            exclude_files=args.excludefiles,
            include_files=args.includefiles
        )

        print_table(summary_stats, individual_stats)


if __name__ == "__main__":
    cli()
