#!/usr/bin/env bash
# scripts/git-sync.sh
# Safe git pull+push for this multi-agent repo. Tests as it goes.
#
# The goal: any Cowork/Claude-Code/Builder agent can run this and have their
# work land on origin/master WITHOUT clobbering the other channels'
# in-flight commits, and WITHOUT leaving Matt in a "stash has conflicts,
# working tree is a mess" state.
#
# Usage:
#   scripts/git-sync.sh                          # pull --rebase + push local commits
#   scripts/git-sync.sh --pull-only              # just pull, don't push
#   scripts/git-sync.sh --commit "msg" [paths…]  # stage paths, commit, then sync
#                                                # (no paths given => git add -A)
#   scripts/git-sync.sh --dry-run                # print the plan, touch nothing
#   scripts/git-sync.sh --help
#
# What it does (default mode):
#   1. Preflight — repo root, git installed, no stale .git/index.lock
#   2. If working tree is dirty: stash -u (keeps untracked too)
#   3. git pull --rebase origin master         (NEVER plain pull)
#   4. git push  origin master                 (NEVER --force)
#   5. git stash pop                           (restores in-flight WIP)
#   6. git status --short --branch             (final sanity print)
#
# Hard-won facts baked in:
#   - Plain `git pull` creates noisy merge commits → use --rebase
#   - Plain `git push` fails when another agent pushed → must pull first
#   - `git push --force` has destroyed Matt's commits in the past → never
#   - Working tree is ALMOST ALWAYS dirty (WIP, private/ notes) → stash first
#   - Stale .git/index.lock from a crashed commit blocks every git command
#   - On failed rebase or failed push, ALWAYS restore the stash before exiting
#     (otherwise the user thinks their changes are gone)
#   - stash pop after rebase CAN conflict; the stash stays in the stack until
#     you resolve + `git stash drop`, so we tell the user exactly what to do

set -uo pipefail

# ─── helpers ──────────────────────────────────────────────────────────────
say()   { printf "\n\033[1;36m→ %s\033[0m\n" "$*"; }
ok()    { printf "  \033[32m✓\033[0m %s\n" "$*"; }
warn()  { printf "  \033[33m⚠\033[0m %s\n" "$*"; }
fail()  { printf "\n  \033[31m✗ %s\033[0m\n" "$*"; exit 1; }

# ─── parse args ───────────────────────────────────────────────────────────
MODE="sync"           # sync | pull-only | commit
COMMIT_MSG=""
DRY=0
COMMIT_PATHS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --pull-only) MODE="pull-only"; shift ;;
    --dry-run)   DRY=1; shift ;;
    --commit)
      MODE="commit"
      COMMIT_MSG="${2:-}"
      [ -n "$COMMIT_MSG" ] || fail "--commit requires a message (got empty string)"
      shift 2
      ;;
    -h|--help)
      sed -n '2,30p' "$0"
      exit 0
      ;;
    --*)
      fail "unknown flag: $1 (see --help)"
      ;;
    *)
      COMMIT_PATHS+=("$1")
      shift
      ;;
  esac
done

# ─── preflight ────────────────────────────────────────────────────────────
say "Preflight"

command -v git >/dev/null 2>&1 || fail "git is not in PATH"
ok "git found: $(git --version)"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT" || fail "could not cd to $REPO_ROOT"
[ -d .git ] || fail "not a git repo at $REPO_ROOT"
ok "repo root: $REPO_ROOT"

# Branch + remote
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
[ -n "$BRANCH" ] && [ "$BRANCH" != "HEAD" ] \
  || fail "could not determine current branch (detached HEAD?). Run: git switch master"
REMOTE="$(git config --get "branch.$BRANCH.remote" 2>/dev/null || echo origin)"
if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  fail "remote '$REMOTE' has no URL. Check: git remote -v"
fi
ok "branch: $BRANCH  ·  remote: $REMOTE ($(git remote get-url "$REMOTE"))"

if [ "$BRANCH" != "master" ] && [ "$BRANCH" != "main" ]; then
  warn "branch is '$BRANCH' (not master/main). Pushing to this branch's tracking remote."
fi

# Stale lock
if [ -f .git/index.lock ]; then
  warn "found .git/index.lock — a previous git command may have crashed"
  if pgrep -f "/git( |$)" >/dev/null 2>&1 || pgrep -x git >/dev/null 2>&1; then
    fail "another git process IS running. Refusing to remove lock. Wait and retry."
  else
    warn "no git processes are running; removing stale lock"
    [ $DRY -eq 1 ] || rm -f .git/index.lock
    ok "removed .git/index.lock"
  fi
fi

# ─── --commit mode: stage + commit before syncing ─────────────────────────
if [ "$MODE" = "commit" ]; then
  say "Commit"
  if [ "${#COMMIT_PATHS[@]}" -eq 0 ]; then
    warn "no paths given; will use 'git add -A' (stages everything)"
    COMMIT_PATHS=("-A")
  fi

  if [ $DRY -eq 1 ]; then
    echo "  would: git add ${COMMIT_PATHS[*]}"
    echo "  would: git commit -m \"$COMMIT_MSG\""
  else
    git add "${COMMIT_PATHS[@]}" || fail "git add failed"
    if git diff --cached --quiet; then
      warn "nothing is staged — no commit to make (paths had no changes?)"
    else
      git commit -m "$COMMIT_MSG" || fail "git commit failed (pre-commit hook? signing?)"
      ok "committed: $COMMIT_MSG"
    fi
  fi
fi

# ─── stash if working tree is dirty ───────────────────────────────────────
STASHED=0
DIRTY=0
if ! git diff --quiet 2>/dev/null; then DIRTY=1; fi
if ! git diff --cached --quiet 2>/dev/null; then DIRTY=1; fi
if [ -n "$(git ls-files --others --exclude-standard 2>/dev/null)" ]; then DIRTY=1; fi

if [ $DIRTY -eq 1 ]; then
  say "Stash working tree (dirty)"
  if [ $DRY -eq 1 ]; then
    echo "  would: git stash push -u -m 'git-sync.sh auto stash'"
  else
    STAMP="$(date +%s)"
    if git stash push -u -m "git-sync.sh auto stash $STAMP" >/dev/null; then
      STASHED=1
      ok "stashed working tree + untracked files"
    else
      fail "git stash push failed"
    fi
  fi
else
  ok "working tree is clean; no stash needed"
fi

# ─── restore-stash helper (used on every failure path) ────────────────────
restore_stash_on_fail() {
  if [ $STASHED -eq 1 ] && [ $DRY -eq 0 ]; then
    warn "restoring stash before exit so your changes aren't lost"
    git stash pop >/dev/null 2>&1 || \
      warn "  stash pop had conflicts. Your WIP is at: git stash list"
  fi
}

# ─── fetch + pull --rebase ────────────────────────────────────────────────
say "git fetch $REMOTE && git pull --rebase $REMOTE $BRANCH"
if [ $DRY -eq 1 ]; then
  echo "  would: git fetch $REMOTE"
  echo "  would: git pull --rebase $REMOTE $BRANCH"
else
  if ! git fetch "$REMOTE" 2>&1 | sed 's/^/    /'; then
    restore_stash_on_fail
    fail "git fetch failed — check network / remote auth"
  fi
  if git pull --rebase "$REMOTE" "$BRANCH" 2>&1 | sed 's/^/    /'; then
    ok "pulled and rebased onto $REMOTE/$BRANCH"
  else
    restore_stash_on_fail
    fail "git pull --rebase failed — resolve conflicts, then re-run. (Stash restored.)"
  fi
fi

# ─── push (unless --pull-only) ────────────────────────────────────────────
if [ "$MODE" != "pull-only" ]; then
  AHEAD=0
  if [ $DRY -eq 0 ]; then
    AHEAD="$(git rev-list --count "$REMOTE/$BRANCH..HEAD" 2>/dev/null || echo 0)"
  fi

  if [ "$AHEAD" = "0" ] && [ $DRY -eq 0 ]; then
    ok "local is already at $REMOTE/$BRANCH — nothing to push"
  else
    say "git push $REMOTE $BRANCH  ($AHEAD local commit$([ "$AHEAD" = "1" ] || echo s) to push)"
    if [ $DRY -eq 1 ]; then
      echo "  would: git push $REMOTE $BRANCH"
    else
      if git push "$REMOTE" "$BRANCH" 2>&1 | sed 's/^/    /'; then
        ok "pushed $AHEAD commit(s) to $REMOTE/$BRANCH"
      else
        restore_stash_on_fail
        fail "git push failed — check network / auth / branch protection. (Stash restored.)"
      fi
    fi
  fi
else
  ok "--pull-only mode; skipping push"
fi

# ─── restore stash (happy path) ───────────────────────────────────────────
if [ $STASHED -eq 1 ] && [ $DRY -eq 0 ]; then
  say "Restore stashed changes"
  if git stash pop >/dev/null 2>&1; then
    ok "stash pop OK — your WIP is back in the working tree"
  else
    warn "stash pop had conflicts — your WIP is still safely in the stash"
    warn "  see it:     git stash list"
    warn "  re-apply:   git stash apply"
    warn "  resolve, then: git add <files> && git stash drop"
  fi
fi

# ─── final status ─────────────────────────────────────────────────────────
say "Final status"
git status --short --branch 2>&1 | sed 's/^/  /'

say "Done."
