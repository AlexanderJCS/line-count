# Line Count
A library that counts the lines within a file, directory, or directory tree.

It can be run through the command line, or functions can be imported to be used in your own Python projects.

Some benefits of `linecount` include:
- See the number of source lines of code (SLOC), commented lines, and blank lines
- Exclude files or directories whose names contain certain characters. This is useful for excluding files with certain file extensions, or certain directories like `venv` or `.git`.
- Only include files whose names contain certain characters. This is useful for counting lines of files with certain file extensions.

You can view the PyPi page [here](https://pypi.org/project/linecount/)

## Installing

You can install the project from pypi:
```shell
$ pip install linecount
```

## Command Line Usage

### Help
You can get help on commands by performing:

```shell
$ linecount -h
$ linecount --help  # alternative way to write it
```

### Counting Lines of a File

```shell
$ linecount file_to_count.txt
```

### Counting Lines in a Directory
```shell
$ linecount . # count all files in this directory
$ linecount /path/to/dir  # or specify a directory this way
```

### Recursive
You can also count the lines of all files within a directory and all of its subdirectories. This command may take a while if you are counting the lines of a lot of files.
```shell
$ linecount . -r  # count all files in this directory + all subdirectories, recursively
$ linecount /path/to/dir -r  # another way to specify the directory
```

### Include Files
If you only want to count the lines of files containing a string in the filename, such as `.py` or `hello`, you can do:
```shell
$ linecount /path/to/dir -r --includefiles ".py,hello"
$ linecount /path/to/dir -r -if ".py,hello"  # alternative way to write it
```
This will only include files whose names contain `.py` or `hello`.  For example, the below files will be included:
```
hello.py
hello.txt
a.hello
cache.pyc
```

### Exclude Files
If you want to exclude files containing a certain string in their name, for example, `.txt`, we can do:
```shell
$ linecount /path/to/dir -r --excludefiles ".txt"
$ linecount /path/to/dir -r -ef ".txt"  # alternative way to write it
```

For example, this will exclude the following files:
```
myfile.txt
a.txt.py
```

### Exclude Dirs
You can also exclude directories that have a specific string in their name. For example, if you want to exclude the `venv` directory:
```shell
$ linecount /path/to/dir -r --excludedirs "venv"
$ linecount /path/to/dir -r -ed "venv"  # alternative way to write it
```

### Combining Include Files and Exclude Files
If you want to include files that have the string `.py`, but not `.pyc`, you can include `.py` and exclude `.pyc`:
```shell
$ linecount /path/to/dir -if ".py" -ef ".pyc"
```

## Python Usage

### Importing

You can import linecount by performing:
```py
import linecount as lc
```

### The LineStats Tuple

The `LineStats` tuple is a common return value from line counting functions. It is a named tuple with five variables:
- `filepath`: the path to the file the object is describing
- `lines`: the total number of lines in the file
- `souce_lines_of_code`: the number of source lines of code (SLOC) in the file
- `commented_lines`: the number of commented lines in the file
- `blank_lines`: the number of empty lines in the file

### Count the lines of a file

You can count the lines of a file with the `lc.count_lines_file(filepath: str)` function. It returns a `LineStats` named tuple.

```py
line_stats: lc.LineStats = lc.count_lines_file("path/to/file.txt")
```

### Counting the lines of a directory

The `lc.count_lines_dir(dir_path: str)` function counts the lines of all files within a directory. It takes one required argument, `dir_path`.

It returns a tuple of two values:
- The first value is a `LineStats` object, and contains data on all the files in the directory summed up.
- The second value is a `list[LineStats]`, and contains one entry per file that was counted.

It also takes in two optional arguments:
- `exclude_files: list[str]`: excludes any files with filenames containing any of the strings listed. For example, if `exclude_files` contains `[".py", ".txt"]`, all files containing `.py` or `.txt` in their name will be excluded.
- `include_files: list[str]`: only filenames that contain one or more of the strings in the list will be included.

Usage example:
```py
summary_stats, specific_stats = lc.count_lines_dir("path/to/dir", exclude_files=[".pyc"], include_files=[".py"])
```

### Counting lines of files within a directory recursively

To recursively count the number of lines of files within a directory, the `lc.count_lines_dir_recursive(dir_path: str)` function can be used.  It takes one required argument, `dir_path`.

It returns a tuple of two values:
- The first value is a `LineStats` object, and contains data on all the files in the directory and subdirectories summed up.
- The second value is a `list[LineStats]` data structure, and contains one entry per file that was counted.

It contains three optional arguments:
- `exclude_files: list[str]`: excludes any files with filenames containing any of the strings listed. For example, if `exclude_files` contains `[".py", ".txt"]`, all files containing `.py` or `.txt` in their name will be excluded.
- `include_files: list[str]`: only filenames that contain one or more of the strings in the list will be included.
- `exclude_dirs: list[str]`: directory names that contain one or more of the strings in the list  will be excluded.

Example usage:
```py
summary_stats, specific_stats = lc.count_lines_dir_recursive("path/to/dir", exclude_files=[".pyc"], include_files=[".py"], exclude_dirs=["venv"])
```