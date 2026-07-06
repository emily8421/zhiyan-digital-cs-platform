# TEMPLATE-UPGRADE: Derived Sync PowerShell Fallback Robustness

> Type: template improvement proposal found during derived-project post-sync closure.
> Status: pending template-repo review.
> Related: `scripts/check-derived-sync.ps1`, `scripts/check-derived-sync.sh`, `ai/commands/sync-methodology.md`, `template-docs/derived-sync-report-template.md`.

## 1. Background and Problem

On Windows PowerShell 5.1, derived-project sync may rely on the PowerShell fallback path when Git Bash cannot start. After syncing to `v1.30.3` and merging the sync PR, post-sync closure exposed two reusable issues:

1. Running `scripts/check-derived-sync.ps1` on `main` after a PR merge checks `HEAD`. If `HEAD` is a merge commit, the script can report a false failure because `diff-tree -r HEAD` has no direct file changes and the merge subject is not `sync template vX.Y.Z from ai-project-template`.
2. Passing an explicit sync commit, for example `scripts/check-derived-sync.ps1 <sync-commit>`, still appeared to check `HEAD` on the PowerShell fallback path. This suggests a parameter forwarding or parsing compatibility issue.

This is not project-specific business logic. It may affect any Windows user who merges template sync branches via PR merge commits and then runs the derived sync boundary check through the PowerShell fallback path.

## 2. Suggested Changes

- Avoid using names that can be confused with PowerShell automatic variables or invocation semantics for fallback helper parameters, such as `$Args`.
- Add a Windows PowerShell 5.1 regression check for `check-derived-sync.ps1 <commit>` to ensure the explicit commit reaches the fallback implementation.
- Add one merge-commit handling strategy:
  - detect PR merge commits at `HEAD` and tell the user to pass the actual sync commit; or
  - automatically find the most recent `sync template vX.Y.Z from ai-project-template` commit in the first-parent range; or
  - add an explicit mode such as `--latest-sync` / `--from-pr`.
- Update `sync-methodology` or the derived sync report template to clarify that post-merge boundary checks should validate the sync commit, not the PR merge commit.
- Add fallback regression coverage for: no arguments, explicit commit, merge commit guidance, empty stderr, and Git Bash unavailable.

## 3. Version Impact

- Suitable for a patch release.
- No change to document lifecycle semantics or the sync file list.
- Impact is limited to Windows / PowerShell fallback reliability and derived-project sync validation UX.

## 4. Acceptance Suggestions

- On Windows PowerShell 5.1, run `scripts/check-derived-sync.ps1 <sync-commit>` and confirm the target commit is the explicit commit.
- Run the checker with a merge commit as `HEAD` and confirm it does not mislead users into treating the merge commit as the template sync commit.
- Confirm the fallback path still gives clear output when Git Bash is unavailable or stderr is empty.
