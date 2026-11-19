---
name: identify-bug
description: Find and explain bugs in code without changing any files. Use when the user asks to identify, find, locate, diagnose or explain a bug, error, crash or unexpected behaviour, or runs /identify-bug with a file, folder, error message or symptom. Read-only - the developer applies the fix.
argument-hint: "[file | folder | error message | symptom]"
allowed-tools: Read, Grep, Glob, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git show:*), Bash(git blame:*)
---

# Identify Bug (read-only)

Find the bug, explain it, and suggest a fix. **Do not modify anything.** The developer is responsible for updating the files.

## Hard rules

- **Never** use Edit, Write, NotebookEdit, or any shell command that changes files (`sed -i`, `>`, `>>`, `mv`, `rm`, `git checkout`, `git restore`, `git stash`, `git commit`, formatters, `--fix` flags, package installs, etc.).
- Do not create scratch, test or patch files inside the repository.
- If the user asks you to apply the fix while this skill is active, remind them the skill is read-only and that they should apply the suggested change themselves (or ask outside this skill).
- Suggested fixes appear **only as code blocks in your reply**, never written to disk.

## Target

`$ARGUMENTS` describes what to investigate. It may be:

- a file or folder path - review that code;
- an error message or stack trace - trace it back to the cause;
- a description of wrong behaviour - find the code responsible;
- empty - inspect the uncommitted changes (`git status`, `git diff`), and if there are none, ask the user what to look at.

## Process

1. **Understand the symptom.** Restate in one line what goes wrong (or what you are checking).
2. **Locate the code.** Use Glob/Grep to find entry points, the functions named in a stack trace, and their callers. Read the relevant files fully, not just the matching line.
3. **Trace the data flow.** Follow inputs through the code: types, `None`/empty values, async/await, exceptions, config and environment variables, file paths, ports, imports, Dockerfile / docker-compose / pyproject settings where relevant.
4. **Check common bug classes:** wrong logic or conditions, off-by-one errors, unhandled exceptions, missing `await`, mutable default arguments, wrong imports or module paths, type mismatches, missing/misnamed env vars, mismatched ports or hostnames between services, resource leaks, race conditions, security issues (secrets in code, injection).
5. **Confirm before reporting.** For each suspected bug, check it against the actual code - make sure it really happens on a concrete input or state. Drop anything you can't back up, or mark it clearly as *possible*.

## Report format

For each bug, most severe first:

### Bug N: <short title>
- **Location:** [file.py:42](relative/path/file.py#L42)
- **Severity:** Critical / High / Medium / Low
- **Confidence:** Confirmed / Likely / Possible
- **What's wrong:** one or two sentences.
- **How it fails:** concrete input or state, and the result (wrong output, exception, crash).
- **Suggested fix:** a minimal code snippet showing the change (before/after), for the developer to apply.

End with a one-line summary (e.g. "2 bugs found: 1 high, 1 low - no files were modified."). If no bugs are found, say so plainly and list what you checked.
