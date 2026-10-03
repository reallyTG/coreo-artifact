# Subject template

Copy, rename, fill in:

    cp -r subjects/_template subjects/mysubject
    python run.py mysubject --quick

Rename inside the copy: the `.fan` file, the `name` and `fan_filepath` in
`example.py`, and the `subjects._template.user_def_functions` import.

Directories starting with `_` are skipped by discovery, so this one never
appears in `python run.py --list`.

Full walkthrough: `docs/adding-a-subject.md`.
