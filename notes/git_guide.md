# Git Guide for Pragmatists

A practical, no-nonsense guide to using Git for everyday development work.

## Table of Contents
1. [Initial Setup](#initial-setup)
   - [Git Aliases (Shortcuts)](#git-aliases-shortcuts)
2. [Starting a Project](#starting-a-project)
3. [Daily Workflow](#daily-workflow)
4. [Branching Strategy](#branching-strategy)
5. [Collaboration](#collaboration)
6. [Fixing Mistakes](#fixing-mistakes)
7. [Advanced Operations](#advanced-operations)
8. [Quick Reference](#quick-reference)
9. [Hands-On Tutorial](#hands-on-tutorial)

---

## Initial Setup

### First Time Git Configuration

```bash
# Set your identity (required)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Optional but recommended settings
git config --global init.defaultBranch main  # Use 'main' as default branch name
git config --global core.editor "code --wait"  # Set VS Code as editor
git config --global pull.rebase false  # Use merge strategy for pulls

# View all configurations
git config --list
```

### SSH Key Setup (for GitHub/GitLab)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard (macOS)
pbcopy < ~/.ssh/id_ed25519.pub

# Then paste this key into GitHub Settings > SSH Keys
```

### Git Aliases (Shortcuts)

Aliases let you create shortcuts for frequently used Git commands. These save typing and make your workflow faster.

#### Setting Up Aliases

```bash
# Basic shortcuts
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# Unstage files
git config --global alias.unstage 'reset HEAD --'

# View last commit
git config --global alias.last 'log -1 HEAD'

# Visual log graph
git config --global alias.visual 'log --graph --oneline --all'
```

#### Recommended Additional Aliases

```bash
# Short status with branch info
git config --global alias.s 'status -sb'

# Compact log (last 20 commits)
git config --global alias.l 'log --oneline -20'

# Amend last commit without editing message
git config --global alias.amend 'commit --amend --no-edit'

# Undo last commit (keep changes)
git config --global alias.undo 'reset HEAD~1'

# View all branches (local and remote)
git config --global alias.branches 'branch -a'

# View all remotes
git config --global alias.remotes 'remote -v'

# List all your aliases
git config --global alias.aliases 'config --get-regexp alias'

# Show changes in last commit
git config --global alias.show-last 'show --stat'

# Pretty log with dates and authors
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# Find branches containing commit
git config --global alias.find-branch 'branch -a --contains'

# Delete merged branches
git config --global alias.cleanup "!git branch --merged | grep -v '\\*\\|main\\|master' | xargs -n 1 git branch -d"
```

#### Using Aliases

```bash
# Instead of: git status
git st

# Instead of: git checkout main
git co main

# Instead of: git log --graph --oneline --all
git visual

# Instead of: git reset HEAD -- file.py
git unstage file.py

# View all your configured aliases
git aliases
```

#### Avoid Anti-Pattern Aliases

**Don't create aliases that skip review steps:**

```bash
# ❌ BAD - Auto-commits without review
git config --global alias.fpush '!git pull && git add . && git commit -m && git push'
# Problems:
# - git commit -m requires a message (this will fail)
# - Stages ALL files without review
# - No chance to check git diff before committing
# - Violates "review before committing" best practice
```

**If you need quick commits, use this safer version:**

```bash
# ✓ BETTER - But still use sparingly!
git config --global alias.quicksave '!f() { git add . && git commit -m "${1:-WIP: quick save}" && git push; }; f'

# Usage:
git quicksave "my commit message"
# Or just: git quicksave  (uses "WIP: quick save")
```

**However, even this is discouraged because:**
- Skips `git diff` review
- Encourages lazy commit messages
- Can accidentally commit unwanted files

**Best practice**: Always review changes before committing:
```bash
git status           # See what changed
git diff            # Review changes
git add file.py     # Stage specific files
git commit -m "..."  # Thoughtful message
git push
```

---

## Starting a Project

### Option 1: Create a New Repository

```bash
# Create project directory
mkdir my-project
cd my-project

# Initialize Git repository
git init

# Create initial files
echo "# My Project" > README.md
echo "*.pyc" > .gitignore
echo "__pycache__/" >> .gitignore

# Make first commit
git add .
git commit -m "Initial commit"

# Connect to remote repository (create empty repo on GitHub first)
git remote add origin git@github.com:username/my-project.git
git push -u origin main
```

### Option 2: Clone an Existing Repository

```bash
# Clone a repository
git clone git@github.com:username/repository.git

# Clone into a specific directory
git clone git@github.com:username/repository.git my-folder

# Clone a specific branch
git clone -b branch-name git@github.com:username/repository.git
```

---

## Daily Workflow

### Basic Cycle: Status → Add → Commit → Push

```bash
# 1. Check what's changed
git status

# 2. View detailed changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes

# 3. Stage changes for commit
git add file.py            # Add specific file
git add src/              # Add entire directory
git add .                 # Add all changes in current directory
git add -p                # Interactive staging (review each change)

# 4. Commit changes
git commit -m "Add feature X"
git commit -m "Fix bug in calculation" -m "Detailed description here"

# 5. Push to remote
git push
git push origin main      # Explicit branch name
```

### Example Workflow

```bash
# Morning: Get latest changes
git pull

# Work on your code...
# Edit files: calculator.py, tests.py

# Check what changed
git status
# Output:
#   modified:   calculator.py
#   modified:   tests.py
#   untracked:  notes.txt

# Review changes
git diff calculator.py

# Stage specific files (don't commit notes.txt)
git add calculator.py tests.py

# Commit with descriptive message
git commit -m "Add multiplication function with tests"

# Push to remote
git push

# Continue working...
```

### Commit Message Best Practices

```bash
# Good commits:
git commit -m "Fix division by zero error in calculator"
git commit -m "Add user authentication module"
git commit -m "Update README with installation instructions"

# Bad commits (too vague):
git commit -m "fix"
git commit -m "changes"
git commit -m "wip"

# Multi-line commit message
git commit -m "Add portfolio optimization module" -m "- Implements mean-variance optimization
- Uses CVXPY for convex optimization
- Includes tests for edge cases"
```

---

## Branching Strategy

### Why Use Branches?

Branches let you work on features, fixes, or experiments without affecting the main codebase.

### Basic Branch Operations

```bash
# List all branches
git branch                # Local branches
git branch -r            # Remote branches
git branch -a            # All branches

# Create a new branch
git branch feature-x

# Switch to a branch
git checkout feature-x

# Create and switch in one command
git checkout -b feature-x

# Modern alternative (Git 2.23+)
git switch feature-x
git switch -c feature-x  # Create and switch
```

### Feature Branch Workflow

```bash
# Starting point: You're on main branch, up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature-user-auth

# Work on your feature...
# Edit files, make commits
git add .
git commit -m "Add login functionality"
git commit -m "Add logout functionality"
git commit -m "Add password reset"

# Push feature branch to remote
git push -u origin feature-user-auth
# Note: -u sets upstream, so future pushes can just be 'git push'

# Continue working...
git add .
git commit -m "Add tests for authentication"
git push  # No need for -u origin feature-user-auth anymore

# When feature is complete, merge into main
git checkout main
git pull origin main                  # Get latest main
git merge feature-user-auth           # Merge your feature
git push origin main                  # Push updated main

# Clean up: Delete feature branch
git branch -d feature-user-auth              # Delete local
git push origin --delete feature-user-auth   # Delete remote
```

### Example: Bug Fix Branch

```bash
# You discover a bug in production
git checkout main
git pull origin main

# Create bug fix branch
git checkout -b fix-calculation-error

# Fix the bug
# Edit calculator.py

git add calculator.py
git commit -m "Fix calculation rounding error"

# Push and merge immediately (critical fix)
git push -u origin fix-calculation-error
git checkout main
git merge fix-calculation-error
git push origin main

# Delete bug fix branch
git branch -d fix-calculation-error
git push origin --delete fix-calculation-error
```

### Viewing Branch Differences

```bash
# See commits in feature-x not in main
git log main..feature-x

# See file differences between branches
git diff main..feature-x

# See which branches are merged into main
git branch --merged main

# See which branches are NOT merged
git branch --no-merged main
```

---

## Collaboration

### Pulling Changes from Remote

```bash
# Get latest changes and merge
git pull

# Equivalent to:
git fetch origin        # Download changes
git merge origin/main   # Merge into current branch

# Pull with rebase (cleaner history)
git pull --rebase

# Pull a specific branch
git pull origin main
```

### Handling Merge Conflicts

```bash
# You pull and get a merge conflict
git pull origin main

# Output:
# Auto-merging calculator.py
# CONFLICT (content): Merge conflict in calculator.py
# Automatic merge failed; fix conflicts and then commit the result.

# Check which files have conflicts
git status

# Open calculator.py, you'll see:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> origin/main

# Edit file to resolve conflicts, remove markers
# Choose one version or combine both

# After fixing conflicts:
git add calculator.py
git commit -m "Merge main and resolve conflicts"
git push
```

### Example: Resolving a Conflict

**Before (calculator.py with conflict):**
```python
def add(a, b):
<<<<<<< HEAD
    return a + b  # Your version
=======
    return float(a) + float(b)  # Their version
>>>>>>> origin/main
```

**After (resolved):**
```python
def add(a, b):
    return float(a) + float(b)  # Chose their version with type casting
```

**Then:**
```bash
git add calculator.py
git commit -m "Resolve conflict in add function, use type casting"
git push
```

### Working with Remotes

```bash
# View remote repositories
git remote -v

# Add a remote
git remote add upstream git@github.com:original/repository.git

# Remove a remote
git remote remove upstream

# Rename a remote
git remote rename origin upstream

# Fetch from upstream without merging
git fetch upstream

# Merge upstream changes into your branch
git merge upstream/main
```

### Syncing with Upstream (Forked Repositories)

```bash
# Setup: You forked someone's repo
# origin = your fork
# upstream = original repository

# Add upstream remote (one time)
git remote add upstream git@github.com:original/repository.git

# Regular workflow to stay synced:
git fetch upstream                    # Get updates from original
git checkout main                     # Switch to your main
git merge upstream/main              # Merge original's changes
git push origin main                 # Update your fork

# Shortcut:
git checkout main
git pull upstream main
git push origin main
```

---

## Fixing Mistakes

### Undo Uncommitted Changes

```bash
# Discard changes to a specific file
git checkout -- file.py

# Modern alternative (Git 2.23+)
git restore file.py

# Discard all uncommitted changes
git checkout -- .
git restore .

# Unstage a file (keep changes, just unstage)
git reset file.py
git restore --staged file.py  # Modern alternative
```

### Undo Last Commit

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes unstaged
git reset HEAD~1

# Undo last commit, discard changes completely
git reset --hard HEAD~1

# Example workflow:
git commit -m "Add feature"
# Oops, forgot to add a file!
git reset --soft HEAD~1        # Undo commit, keep changes staged
git add forgotten_file.py
git commit -m "Add feature with all files"
```

### Modify Last Commit

```bash
# Forgot to add a file to last commit
git add forgotten_file.py
git commit --amend --no-edit  # Add to last commit without changing message

# Change last commit message
git commit --amend -m "New commit message"

# Example:
git commit -m "Add calculatro"     # Typo!
git commit --amend -m "Add calculator"  # Fix it
```

### Revert a Commit (Safe for Shared History)

```bash
# Create a new commit that undoes a previous commit
git revert abc123

# Revert the last commit
git revert HEAD

# Revert multiple commits
git revert HEAD~3..HEAD  # Revert last 3 commits

# Example:
git log --oneline
# abc123 Add broken feature
# def456 Update README
# You want to undo abc123:
git revert abc123
git push  # Safe to push because you created a new commit
```

### Recover Deleted Commits

```bash
# View all actions (including deleted commits)
git reflog

# Output:
# abc123 HEAD@{0}: reset: moving to HEAD~1
# def456 HEAD@{1}: commit: Add feature
# You deleted def456, now recover it:

git checkout def456
git checkout -b recovery-branch  # Create branch to save it
```

### Stashing Changes

```bash
# Save work in progress without committing
git stash

# Stash with a message
git stash save "Work in progress on feature X"

# List all stashes
git stash list

# Apply most recent stash (keep stash)
git stash apply

# Apply and remove most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Delete a stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

### Stash Example Workflow

```bash
# You're working on feature-x branch
git checkout feature-x
# Edit files...

# Urgent bug fix needed on main!
git status  # You have uncommitted changes

# Stash your work
git stash save "Feature X in progress"

# Switch to main and fix bug
git checkout main
git checkout -b fix-urgent-bug
# Fix bug...
git add .
git commit -m "Fix urgent bug"
git push

# Return to feature work
git checkout feature-x
git stash pop  # Restore your work
# Continue working...
```

---

## Advanced Operations

### Interactive Rebase (Clean Up History)

```bash
# Clean up last 3 commits before pushing
git rebase -i HEAD~3

# In the editor, you can:
# - pick: keep commit as-is
# - reword: change commit message
# - squash: combine with previous commit
# - drop: delete commit

# Example:
pick abc123 Add feature
squash def456 Fix typo
reword ghi789 Update tests

# This will combine first two commits and let you edit the third message
```

### Cherry-Pick (Apply Specific Commits)

```bash
# Apply a specific commit from another branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Example:
# You're on main, want one commit from feature branch
git log feature-x --oneline
# abc123 Add cool function
# def456 Add tests
# ghi789 Add documentation

# Get just the function:
git checkout main
git cherry-pick abc123
git push
```

### Viewing History

```bash
# Basic log
git log

# One line per commit
git log --oneline

# With graph
git log --oneline --graph --all

# Last N commits
git log -5

# Changes in specific file
git log file.py
git log -p file.py  # With diff

# Commits by author
git log --author="John"

# Commits in date range
git log --since="2 weeks ago"
git log --after="2024-01-01" --before="2024-03-01"

# Find commit that changed specific line
git blame file.py
git blame -L 10,20 file.py  # Lines 10-20 only
```

### Searching Code

```bash
# Search current code
git grep "function_name"

# Search in specific branch
git grep "function_name" branch-name

# Search with context lines
git grep -C 3 "function_name"

# Search all commits for when code was added/removed
git log -S "function_name"
```

### Tagging Releases

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# List tags
git tag
git tag -l "v1.*"  # Pattern matching

# Push tags to remote
git push origin v1.0.0
git push origin --tags  # Push all tags

# Checkout a tag
git checkout v1.0.0

# Delete a tag
git tag -d v1.0.0                    # Local
git push origin --delete v1.0.0     # Remote
```

### Submodules (External Dependencies)

```bash
# Add a submodule
git submodule add git@github.com:user/repo.git libs/repo

# Clone repository with submodules
git clone --recurse-submodules git@github.com:user/project.git

# Initialize submodules after cloning
git submodule init
git submodule update

# Update submodules to latest
git submodule update --remote

# Remove submodule
git submodule deinit libs/repo
git rm libs/repo
```

---

## Quick Reference

### Most Used Commands

```bash
git status                  # Check status
git add .                   # Stage all changes
git commit -m "message"     # Commit changes
git push                    # Push to remote
git pull                    # Pull from remote
git checkout -b branch      # Create and switch to branch
git merge branch           # Merge branch into current
git log --oneline          # View history
git diff                   # View changes
```

### Branch Management

```bash
git branch                           # List local branches
git branch -a                        # List all branches
git checkout -b new-branch          # Create and switch
git checkout main                   # Switch to main
git merge feature                   # Merge feature into current
git branch -d feature               # Delete local branch
git push origin --delete feature    # Delete remote branch
```

### Fixing Mistakes

```bash
git restore file.py                # Discard file changes
git restore --staged file.py       # Unstage file
git reset --soft HEAD~1            # Undo last commit, keep changes
git commit --amend                 # Modify last commit
git revert HEAD                    # Revert last commit safely
git stash                          # Save work in progress
git stash pop                      # Restore stashed work
```

### Viewing Information

```bash
git log --oneline --graph          # Pretty history
git log -p file.py                 # File history with changes
git diff main..feature             # Compare branches
git blame file.py                  # Who changed what
git show abc123                    # Show specific commit
```

### Collaboration

```bash
git clone url                      # Clone repository
git remote -v                      # View remotes
git fetch origin                   # Download changes
git pull origin main              # Pull and merge
git push origin main              # Push to remote
```

---

## Hands-On Tutorial

This section provides step-by-step tutorials you can execute to learn Git through practice. Each scenario includes expected outputs and common pitfalls.

### Tutorial 1: First Repository and Commit

**Scenario**: Create your first Git repository from scratch.

```bash
# 1. Create a practice directory
mkdir git-practice
cd git-practice

# 2. Initialize Git repository
git init

# Expected output:
# Initialized empty Git repository in /path/to/git-practice/.git/

# 3. Check repository status
git status

# Expected output:
# On branch main
# No commits yet
# nothing to commit (create/copy files and use "git add" to track)

# 4. Create your first file
echo "# My First Git Project" > README.md
echo "Learning Git step by step" >> README.md

# 5. Check status again
git status

# Expected output:
# On branch main
# No commits yet
# Untracked files:
#   README.md

# 6. Stage the file
git add README.md

# 7. Check status
git status

# Expected output:
# On branch main
# No commits yet
# Changes to be committed:
#   new file:   README.md

# 8. Create your first commit
git commit -m "add initial README with project description"

# Expected output:
# [main (root-commit) abc123] add initial README with project description
#  1 file changed, 2 insertions(+)
#  create mode 100644 README.md

# 9. View commit history
git log

# Expected output:
# commit abc123def456... (HEAD -> main)
# Author: Your Name <your.email@example.com>
# Date:   Mon Sep 30 10:00:00 2024
#
#     add initial README with project description

# 10. View compact history
git log --oneline

# Expected output:
# abc123 add initial README with project description
```

**What you learned:**
- `git init` creates a new repository
- Files start as "untracked"
- `git add` stages files for commit
- `git commit` saves staged changes
- `git log` shows commit history

---

### Tutorial 2: Making Changes and Committing

**Scenario**: Practice the edit-stage-commit cycle with multiple files.

```bash
# Starting from git-practice directory with one commit

# 1. Create a new Python file
cat > calculator.py << 'EOF'
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
EOF

# 2. Create a test file
cat > test_calculator.py << 'EOF'
from calculator import add, subtract

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2
EOF

# 3. Check what changed
git status

# Expected output:
# On branch main
# Untracked files:
#   calculator.py
#   test_calculator.py

# 4. View differences (nothing yet - files are untracked)
git diff
# (no output - untracked files don't show in diff)

# 5. Stage only calculator.py
git add calculator.py

# 6. Check status
git status

# Expected output:
# On branch main
# Changes to be committed:
#   new file:   calculator.py
#
# Untracked files:
#   test_calculator.py

# 7. Commit calculator.py
git commit -m "add calculator with add and subtract functions"

# 8. Now stage and commit tests
git add test_calculator.py
git commit -m "add unit tests for calculator"

# 9. View commit history
git log --oneline

# Expected output:
# def789 add unit tests for calculator
# abc123 add calculator with add and subtract functions
# abc000 add initial README with project description

# 10. Make a change to calculator.py
cat >> calculator.py << 'EOF'

def multiply(a, b):
    return a * b
EOF

# 11. Check status and diff
git status
# Shows: modified: calculator.py

git diff calculator.py
# Shows: + def multiply(a, b):
#        +     return a * b

# 12. Stage and commit the change
git add calculator.py
git commit -m "add multiply function to calculator"

# 13. View detailed history with changes
git log -p -2

# Shows last 2 commits with full diffs
```

**What you learned:**
- Stage and commit files separately for logical commits
- `git diff` shows unstaged changes
- Modified files must be staged again
- Each commit should be a logical unit of work

---

### Tutorial 3: Working with Branches

**Scenario**: Create a feature branch, make changes, and merge back to main.

```bash
# Starting from git-practice with 4 commits on main

# 1. View current branches
git branch

# Expected output:
# * main

# 2. Create and switch to feature branch
git checkout -b feature-division

# Expected output:
# Switched to a new branch 'feature-division'

# 3. Verify you're on new branch
git branch

# Expected output:
#   main
# * feature-division

# 4. Add division function
cat >> calculator.py << 'EOF'

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

# 5. Check status
git status

# Expected output:
# On branch feature-division
# Changes not staged for commit:
#   modified:   calculator.py

# 6. Stage and commit
git add calculator.py
git commit -m "add divide function with zero check"

# 7. Add corresponding test
cat >> test_calculator.py << 'EOF'

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    try:
        divide(5, 0)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"
EOF

# 8. Stage and commit test
git add test_calculator.py
git commit -m "add tests for divide function"

# 9. View branch history
git log --oneline

# Expected output (on feature-division):
# xyz789 add tests for divide function
# xyz456 add divide function with zero check
# def789 add unit tests for calculator
# abc123 add calculator with add and subtract functions
# abc000 add initial README with project description

# 10. Switch back to main
git checkout main

# 11. Check calculator.py (no divide function here!)
cat calculator.py
# Only shows add, subtract, multiply

# 12. View main branch history
git log --oneline

# Expected output (on main):
# ghi123 add multiply function to calculator
# def789 add unit tests for calculator
# abc123 add calculator with add and subtract functions
# abc000 add initial README with project description

# 13. See commits in feature branch not in main
git log main..feature-division --oneline

# Expected output:
# xyz789 add tests for divide function
# xyz456 add divide function with zero check

# 14. Merge feature branch into main
git merge feature-division

# Expected output:
# Updating ghi123..xyz789
# Fast-forward
#  calculator.py      | 5 +++++
#  test_calculator.py | 8 ++++++++
#  2 files changed, 13 insertions(+)

# 15. Verify divide function is now in main
cat calculator.py
# Now shows add, subtract, multiply, divide

# 16. View updated history
git log --oneline --graph --all

# Expected output:
# * xyz789 (HEAD -> main, feature-division) add tests for divide function
# * xyz456 add divide function with zero check
# * ghi123 add multiply function to calculator
# * def789 add unit tests for calculator
# * abc123 add calculator with add and subtract functions
# * abc000 add initial README with project description

# 17. Delete feature branch (no longer needed)
git branch -d feature-division

# Expected output:
# Deleted branch feature-division (was xyz789).

# 18. Verify branch deleted
git branch

# Expected output:
# * main
```

**What you learned:**
- `git checkout -b` creates and switches to new branch
- Changes on feature branch don't affect main
- `git merge` brings changes from one branch to another
- Delete feature branches after merging to keep repository clean

---

### Tutorial 4: Handling Merge Conflicts

**Scenario**: Create a conflict and learn to resolve it.

```bash
# Starting from git-practice on main branch

# 1. Create two branches from main
git checkout -b branch-a
git checkout main
git checkout -b branch-b

# 2. On branch-b, modify calculator.py
git checkout branch-b
cat > calculator.py << 'EOF'
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide a by b with zero check."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

git add calculator.py
git commit -m "add docstrings to all functions"

# 3. Switch to branch-a and make DIFFERENT changes
git checkout branch-a
cat > calculator.py << 'EOF'
def add(a, b):
    # Addition operation
    return a + b

def subtract(a, b):
    # Subtraction operation
    return a - b

def multiply(a, b):
    # Multiplication operation
    return a * b

def divide(a, b):
    # Division with error handling
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

git add calculator.py
git commit -m "add inline comments to all functions"

# 4. Merge branch-b into branch-a (will conflict!)
git merge branch-b

# Expected output:
# Auto-merging calculator.py
# CONFLICT (content): Merge conflict in calculator.py
# Automatic merge failed; fix conflicts and then commit the result.

# 5. Check status
git status

# Expected output:
# On branch branch-a
# You have unmerged paths.
#   (fix conflicts and run "git commit")
#
# Unmerged paths:
#   (use "git add <file>..." to mark resolution)
#     both modified:   calculator.py

# 6. View the conflict in calculator.py
cat calculator.py

# Expected output:
# def add(a, b):
# <<<<<<< HEAD
#     # Addition operation
# =======
#     """Add two numbers and return the result."""
# >>>>>>> branch-b
#     return a + b
# ... (more conflicts)

# 7. Resolve conflict manually (choose docstrings)
cat > calculator.py << 'EOF'
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide a by b with zero check."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

# 8. Mark conflict as resolved
git add calculator.py

# 9. Check status
git status

# Expected output:
# On branch branch-a
# All conflicts fixed but you are still merging.
#   (use "git commit" to conclude merge)

# 10. Complete the merge
git commit -m "merge branch-b, resolve conflicts using docstrings"

# Expected output:
# [branch-a abc123] merge branch-b, resolve conflicts using docstrings

# 11. View merge commit in history
git log --oneline --graph

# Expected output showing merge:
# *   abc123 (HEAD -> branch-a) merge branch-b, resolve conflicts using docstrings
# |\
# | * def456 (branch-b) add docstrings to all functions
# * | ghi789 add inline comments to all functions
# |/
# * xyz789 add tests for divide function
# ...

# 12. Merge into main and clean up
git checkout main
git merge branch-a
git branch -d branch-a
git branch -d branch-b
```

**What you learned:**
- Conflicts occur when same lines are changed in different branches
- Git marks conflicts with `<<<<<<<`, `=======`, `>>>>>>>`
- You must manually choose which version to keep (or combine them)
- `git add` marks conflict as resolved
- Complete merge with `git commit`

---

### Tutorial 5: Connecting to GitHub and Pushing

**Scenario**: Push your local repository to GitHub.

```bash
# Starting from git-practice with commits on main

# 1. Create repository on GitHub
# Go to github.com → New Repository
# Name it "git-practice"
# Do NOT initialize with README (we already have commits)
# Copy the SSH URL: git@github.com:username/git-practice.git

# 2. Add GitHub as remote
git remote add origin git@github.com:username/git-practice.git

# 3. Verify remote was added
git remote -v

# Expected output:
# origin  git@github.com:username/git-practice.git (fetch)
# origin  git@github.com:username/git-practice.git (push)

# 4. Push main branch to GitHub
git push -u origin main

# Expected output:
# Enumerating objects: 15, done.
# Counting objects: 100% (15/15), done.
# ...
# To github.com:username/git-practice.git
#  * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.

# 5. Make a new commit
echo "## Installation" >> README.md
echo "pip install -r requirements.txt" >> README.md
git add README.md
git commit -m "add installation instructions to README"

# 6. Push update (no need for -u origin main anymore)
git push

# Expected output:
# Enumerating objects: 5, done.
# ...
# To github.com:username/git-practice.git
#    abc123..def456  main -> main

# 7. Create feature branch and push it
git checkout -b feature-power
cat >> calculator.py << 'EOF'

def power(a, b):
    """Raise a to the power of b."""
    return a ** b
EOF

git add calculator.py
git commit -m "add power function"

# 8. Push feature branch to GitHub
git push -u origin feature-power

# Expected output:
# To github.com:username/git-practice.git
#  * [new branch]      feature-power -> feature-power
# Branch 'feature-power' set up to track remote branch 'feature-power'

# 9. View all branches (local and remote)
git branch -a

# Expected output:
# * feature-power
#   main
#   remotes/origin/feature-power
#   remotes/origin/main

# 10. Delete remote feature branch (after merging on GitHub)
git push origin --delete feature-power

# Expected output:
# To github.com:username/git-practice.git
#  - [deleted]         feature-power
```

**What you learned:**
- `git remote add origin` connects local repo to GitHub
- `git push -u origin main` pushes and sets up tracking
- After `-u` once, can just use `git push`
- Can push any branch to GitHub
- Delete remote branches with `git push origin --delete`

---

### Tutorial 6: Real-World Workflow (nc Branch Pattern)

**Scenario**: Practice the workflow used in this project with numbered branches.

```bash
# Starting from clean main branch

# WORKFLOW: Quick commit and merge pattern

# 1. Start on up-to-date main
git checkout main
git pull origin main

# 2. Find next branch number (check existing nc branches)
git branch -a | grep nc
# Suppose you see nc1, nc2, nc3, nc4, nc5
# Next branch will be nc6

# 3. Create and switch to nc6
git checkout -b nc6

# 4. Make your changes (simulate some work)
cat > new_feature.py << 'EOF'
def new_feature():
    """A new feature for the project."""
    return "Feature implemented!"
EOF

# 5. Check status
git status

# Expected output:
# On branch nc6
# Untracked files:
#   new_feature.py

# 6. Stage all changes
git add .

# 7. Commit with descriptive message
git commit -m "add new feature module with implementation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 8. Push branch to remote
git push -u origin nc6

# Expected output:
# To github.com:username/project.git
#  * [new branch]      nc6 -> nc6

# 9. [PAUSE HERE] Review changes on GitHub, run tests, etc.

# 10. After verification, merge to main
git checkout main
git pull origin main

# 11. Check for conflicts BEFORE merging (dry run)
git merge --no-commit --no-ff nc6

# If no conflicts:
git merge --abort  # Cancel dry run
git merge nc6      # Do real merge

# Expected output:
# Updating abc123..def456
# Fast-forward
#  new_feature.py | 3 +++
#  1 file changed, 3 insertions(+)

# 12. Push updated main
git push origin main

# 13. Delete nc6 branch (local and remote)
git branch -d nc6
git push origin --delete nc6

# Expected output:
# Deleted branch nc6 (was def456).
# To github.com:username/project.git
#  - [deleted]         nc6

# 14. Verify clean state
git branch
# Expected output:
# * main

git status
# Expected output:
# On branch main
# Your branch is up to date with 'origin/main'.
# nothing to commit, working tree clean

# SUCCESS! Feature merged and branch cleaned up.

# Next feature? Start with nc7!
```

**What you learned:**
- Numbered branch convention (nc1, nc2, nc3...)
- Always pull main before creating branch
- Commit message includes attribution footer
- Review before merging (don't auto-merge!)
- Clean up branches after merge
- This pattern keeps history clean and organized

---

### Tutorial 7: Fixing Mistakes

**Scenario**: Common mistakes and how to fix them.

```bash
# MISTAKE 1: Committed to wrong branch

# You're on main and make a commit (oops!)
git checkout main
echo "New file" > mistake.txt
git add mistake.txt
git commit -m "add mistake file"

# Realize you should have done this on a feature branch
# Fix: Move commit to new branch

git branch nc7              # Create branch with this commit
git reset --hard HEAD~1     # Remove commit from main
git checkout nc7            # Switch to nc7

# Now the commit is on nc7, not main!

# ---

# MISTAKE 2: Commit message has typo

git commit -m "add calculatro module"  # Typo: calculatro

# Fix: Amend the commit
git commit --amend -m "add calculator module"

# ---

# MISTAKE 3: Forgot to add a file to last commit

git add file1.py
git commit -m "add feature X"

# Oops, forgot file2.py that belongs in this commit
git add file2.py
git commit --amend --no-edit  # Add to last commit

# ---

# MISTAKE 4: Made changes but need to switch branches urgently

git checkout nc7
# Edit files...
# Urgent: need to switch to main for bug fix, but changes aren't ready to commit

# Fix: Stash the changes
git stash save "nc7 work in progress"
git checkout main
# Fix urgent bug...
git checkout nc7
git stash pop  # Restore work

# ---

# MISTAKE 5: Want to undo last commit completely

git commit -m "bad feature"
# Actually, this whole commit was a bad idea

# Fix: Reset (if not pushed yet)
git reset --hard HEAD~1  # Deletes commit and changes

# ---

# MISTAKE 6: Already pushed bad commit

git push origin main
# Oops, that commit broke production!

# Fix: Revert (creates new commit that undoes it)
git revert HEAD
git push origin main

# History now shows:
# abc123 revert "bad commit"
# def456 bad commit  (safely undone)

# ---

# MISTAKE 7: Lost commits after reset

git reset --hard HEAD~3  # Oh no, lost 3 commits!

# Fix: Use reflog to recover
git reflog

# Output:
# abc123 HEAD@{0}: reset: moving to HEAD~3
# def456 HEAD@{1}: commit: important feature
# ghi789 HEAD@{2}: commit: another feature

# Recover the commits
git checkout def456
git checkout -b recovery-branch
# Your commits are back!
```

**What you learned:**
- `git commit --amend` fixes last commit
- `git stash` temporarily saves changes
- `git reset` undoes commits (use with caution)
- `git revert` safely undoes pushed commits
- `git reflog` can recover "lost" commits
- Most mistakes are recoverable!

---

### Tutorial 8: Practice Challenge

**Put it all together**: Complete this realistic workflow without looking at hints.

```bash
# CHALLENGE: Implement a new feature end-to-end

# Requirements:
# 1. Create feature branch nc8
# 2. Add a new file: statistics.py with mean() function
# 3. Add tests in test_statistics.py
# 4. Commit with good message
# 5. Make second commit adding median() function
# 6. Push branch to GitHub
# 7. Merge to main (after imaginary review)
# 8. Clean up branch locally and remotely
# 9. Verify main is clean

# Try to complete this without looking at previous examples!
# Solutions below...
```

<details>
<summary><strong>Solution (click to expand)</strong></summary>

```bash
# 1. Create and switch to nc8
git checkout main
git pull origin main
git checkout -b nc8

# 2. Create statistics.py
cat > statistics.py << 'EOF'
def mean(numbers):
    """Calculate arithmetic mean of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)
EOF

# 3. Create tests
cat > test_statistics.py << 'EOF'
from statistics import mean
import pytest

def test_mean_basic():
    assert mean([1, 2, 3, 4, 5]) == 3.0

def test_mean_empty():
    with pytest.raises(ValueError):
        mean([])
EOF

# 4. Commit
git add statistics.py test_statistics.py
git commit -m "add statistics module with mean function and tests"

# 5. Add median function
cat >> statistics.py << 'EOF'

def median(numbers):
    """Calculate median of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid-1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]
EOF

cat >> test_statistics.py << 'EOF'

def test_median_odd():
    assert median([1, 3, 5]) == 3

def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5
EOF

git add statistics.py test_statistics.py
git commit -m "add median function with tests"

# 6. Push to GitHub
git push -u origin nc8

# 7. Merge to main
git checkout main
git pull origin main
git merge nc8
git push origin main

# 8. Delete branches
git branch -d nc8
git push origin --delete nc8

# 9. Verify
git status
git branch

# Perfect! You've completed the workflow!
```
</details>

---

## Common Workflows Cheat Sheet

### Starting Work on New Feature

```bash
git checkout main
git pull origin main
git checkout -b feature-name
# Do work...
git add .
git commit -m "Implement feature"
git push -u origin feature-name
```

### Merging Feature into Main

```bash
git checkout main
git pull origin main
git merge feature-name
git push origin main
git branch -d feature-name
git push origin --delete feature-name
```

### Syncing Fork with Upstream

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Emergency Bug Fix

```bash
git checkout main
git pull origin main
git checkout -b hotfix-bug
# Fix bug...
git add .
git commit -m "Fix critical bug"
git push -u origin hotfix-bug
git checkout main
git merge hotfix-bug
git push origin main
```

---

## Troubleshooting

### "Your branch is ahead of 'origin/main'"

```bash
# You have local commits not pushed
git push
```

### "Your branch is behind 'origin/main'"

```bash
# Remote has commits you don't have
git pull
```

### "Your branch has diverged"

```bash
# Both local and remote have unique commits
git pull --rebase  # Reapply your commits on top
# Or:
git pull           # Create merge commit
```

### "Permission denied (publickey)"

```bash
# SSH key not set up properly
# 1. Generate key: ssh-keygen -t ed25519
# 2. Add to agent: ssh-add ~/.ssh/id_ed25519
# 3. Add public key to GitHub
```

### "Cannot lock ref"

```bash
# Corrupted branch reference
git remote prune origin
git fetch origin
```

### Accidentally Committed to Wrong Branch

```bash
# On wrong-branch with uncommitted work
git checkout -b correct-branch  # Create correct branch with changes
git checkout wrong-branch
git reset --hard HEAD~1         # Remove commit from wrong branch
```

---

## Best Practices

1. **Commit often, push frequently**: Small commits are easier to review and revert
2. **Write meaningful commit messages**: "Fix bug" is bad, "Fix null pointer in user login" is good
3. **Pull before you push**: Always sync with remote before pushing
4. **Use branches**: Never commit directly to main for features
5. **Review before committing**: Use `git diff` to see what you're committing
6. **Don't commit secrets**: Add sensitive files to .gitignore
7. **Keep main stable**: Only merge tested, working code
8. **Clean up branches**: Delete merged branches to reduce clutter

---

## Additional Resources

- **Official Git Documentation**: https://git-scm.com/doc
- **Interactive Git Tutorial**: https://learngitbranching.js.org/
- **GitHub Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Atlassian Git Tutorials**: https://www.atlassian.com/git/tutorials
- **Pro Git Book (Free)**: https://git-scm.com/book/en/v2

---

**Last Updated**: 2025-09-30
**Version**: 2.0
