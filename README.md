Test git repo annotations for KDE and GNOME projects.

Annotation files created with
[git-test-annotate](https://github.com/afrantzis/git-test-annotate).

The process.py tool can process one or more test annotation files:

```python3 process.py [--list] [DIR|FILE]...```

Annotation files must end with ```.ta``` or ```.stats```.

Example:

```python3 process.py annotations/kde annotations/gnome```
