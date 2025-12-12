# Cursor Prompt Templates

This folder contains reusable prompt templates. Reference them with `@filename` to trigger the workflow automatically.

## Available Prompts

### @issue-workflow.md
**What it does:** Creates an issue-specific branch and starts working on the issue
**Usage:** `@issue-workflow.md` or just reference it when you want to start working on an issue
**Result:** 
- Creates branch `issue-<number>-<description>`
- Adds branch creation as first todo (marked completed)
- Creates plan with todos
- Starts implementation

### @commit-and-close.md
**What it does:** Commits all changes with proper format and closes the issue
**Usage:** `@commit-and-close.md` when you're done with an issue
**Result:**
- Formats commit message with "Closes #<number>"
- Lists all completed tasks
- Commits and closes the GitHub issue

### @merge-and-cleanup.md
**What it does:** Merges issue branch to main, pushes, and cleans up branches
**Usage:** `@merge-and-cleanup.md` after committing
**Result:**
- Checks out main branch
- Merges issue branch
- Pushes to remote
- Deletes local and remote issue branches

## How to Use

Simply reference the file in your message:
- "I want to work on issue #5. @issue-workflow.md"
- "@commit-and-close.md"
- "@merge-and-cleanup.md"

Or just mention the file and the workflow will execute automatically.

