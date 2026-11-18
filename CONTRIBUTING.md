# Contributing to this PeakRDL-regblock fork
This project is a fork of [SystemRDL/PeakRDL-regblock](https://github.com/SystemRDL/PeakRDL-regblock). Custom changes are applied on top of the upstream HEAD as a series of logical self-contained commits. By keeping a small set of coherent commits, we ensure that updating the fork whenever a new upstream release is published remains a simple and linear task.

## Bug or feature contribution
1. Open an [issue](https://github.com/HEP-SoC/PeakRDL-regblock/issues)
2. Create a development branch and open a pull request when ready
3. Make sure the commit history stays linear and consistent:
    - Group changes corresponding to the same file, same topic or bug fix in the same commit. If your bug fix is fixing a change made in a previous commit, edit that commit. 
    - Move commits around to keep a consistent history where changes are applied in order of topic. Commits should have a prefix indicating the scope of the change. Commits that are core to the functionality of the fork should come first, followed by commits that solve bugs or compatibility issues and that will potentially be removed when those issues are resolved here or upstream. The latter should contain the issue number as a prefix. Example:
        ```
        9b6f9bf [Issue #13] Remove problematic assertion
        02a6971 Update pyproject.toml
        52fe420 Add Verilator lint_off for MULTIDRIVEN
        841cad4 [Issue #6] Comment out APB4 pprot signal
        d8b5c1d [TMRG] Ignore/copy
        c315862 [TMRG] Add tmrError support
        2652da8 [Voting] Add voting to cpuif signals if retime_read_response
        9600213 [Voting] Add voting to module_tmpl
        3d4c99e [Voting] Add voting to addr_decode
        30620a6 [Voting] Add get_voted_storage_identifier
        9d15c90 [Voting] Add voting to apb4_tmpl
        e2020bc [Voting] Add voting to apb3_tmpl
        ```
    - `git rebase -i`  is your friend here and should be heavily used to ensure the points above.
4. Pull requests should be merged with a linear history without merge commits. Given that every pull request will re-write the history and will pollute the diff, consider using the following to ease the reviewer's job:
    - Use `git range-diff` to show the patch stack diff per commit:
        ```
        git range-diff <previous tagged version>...<your development branch>
        ```
    This will show which commits where added, changed or dropped and a per-commit diff.
    - Use this snippet to generate a flat diff for the whole patch stack compared to the previous one:
        ```sh
        OLD_BASE=<old upstream base commit>
        NEW_BASE=<new upstream base commit>
        OLD_TIP=<previous fork tagged version>
        NEW_TIP=<your development branch>

        git worktree add --detach ../old-on-new $NEW_BASE
        git -C ../old-on-new checkout -q --detach $NEW_BASE

        # old modifications as one combined patch, 3-way applied onto the new upstream
        git diff $OLD_BASE $OLD_TIP | git -C ../old-on-new apply --3way --index
        git -C ../old-on-new add -A          # keeps any conflict markers, like merge-tree would
        TREE=$(git -C ../old-on-new write-tree)

        git diff --stat $TREE $NEW_TIP
        git diff $TREE $NEW_TIP

        git worktree remove --force ../old-on-new
        ```
    This will generate a flat diff that can be copy-pasted on GitHub's pull request description to show changes at a glance.
5. Afte the pull request is complete, create a tag following this convention:
    ```
    <upstream version>-socrates<incremental number>
    ```

## Updating the fork after an upstream release
The same approach should be followed with a rebase of the fork on the upstream and conflict resolution. Special care should be taken to review the changes introduced upstream, to ensure they don't break functionality and that no new changes must be introduced in the fork.
