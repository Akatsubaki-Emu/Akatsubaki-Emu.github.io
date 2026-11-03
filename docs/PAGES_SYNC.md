# Pages repository synchronization

## Canonical direction

- GitLab `chantinlongxthrx/i-steam.github.io`, branch `main`, is the canonical website source.
- GitHub `I-Steam/I-steam.github.io`, branch `main`, is the published mirror.
- GitHub Actions performs the recurring GitLab-to-GitHub synchronization. GitLab CI runners are not required for this mirror.
- The workflow is stored at `.github/workflows/main.yml`. It is copied to GitHub once, then runs on a five-minute schedule, manual dispatch, and GitHub main pushes.

## Authentication

The GitLab repository is publicly readable, so the mirror workflow does not need a GitLab token or GitLab write access. GitHub Actions uses its built-in `GITHUB_TOKEN` with repository `contents: write` permission to update the GitHub mirror.

## Reconciliation behavior

1. Fetch GitHub `main` and public GitLab `main`.
2. If both refs match, finish without a commit.
3. If GitLab is ahead, fast-forward the GitHub mirror.
4. If GitHub has mirror-only commits and GitLab has no newer commits, leave GitHub unchanged.
5. If both branches have new commits, merge GitLab into GitHub. On content conflicts, prefer GitLab because it is canonical.
6. Push to GitHub using a normal, non-force push. If a merge or push cannot be completed safely, stop and report the failure.

The workflow never pushes to GitLab, never force-pushes, and never requires GitLab CI compute minutes.

## One-time activation

The workflow must exist in the GitHub repository at `.github/workflows/main.yml` for GitHub Actions to execute it. Copy the canonical file from the GitLab repository to that exact path on GitHub once. Then open the GitHub Actions tab and manually run **GitLab to GitHub Pages Mirror**.

## Validation and limitations

- The workflow source is committed in GitLab as the canonical copy.
- GitHub Actions execution and successful mirror push must be verified in the GitHub Actions run history.
- A public GitLab repository is assumed. If its visibility changes, provide a read-only GitLab credential through GitHub Actions secrets and adjust the fetch step.
- Conflicting files prefer GitLab; review future changes to this policy before adding GitHub-only website content.
