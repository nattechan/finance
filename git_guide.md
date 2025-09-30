# Git Guide for Pragmatists

A practical, no-nonsense guide to using Git for everyday development work.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Starting a Project](#starting-a-project)
3. [Daily Workflow](#daily-workflow)
4. [Branching Strategy](#branching-strategy)
5. [Collaboration](#collaboration)
6. [Fixing Mistakes](#fixing-mistakes)
7. [Advanced Operations](#advanced-operations)
8. [Quick Reference](#quick-reference)
9. [Simple Tutorial](#simple-tutorial)

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

## Simple Tutorial

```bash
# You are currently on an up-to-date main branch
git checkout -b xyz
# Create a new branch called xyz. Checkout to that branch

# Check the status of your current branch
git status  # You have uncommitted changes

# Stage changes
git add ["file name"]

# Alternatively, we can add all changes
git add .

# Commit these changes
git commit -m ["input message"]

# Push branch
git push origin xyz

# Switch to main
git checkout main
git pull origin main

# Merge branch to main
git merge xyz

# Push the updated main to remote
git push origin main

# (Optional) Delete the xyz branch locally and remotely if you're done 
with it
git branch -d xyz              # Delete local branch
git push origin --delete xyz   # Delete remote branch
```

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

---

**Last Updated**: 2025-09-29
**Version**: 1.0