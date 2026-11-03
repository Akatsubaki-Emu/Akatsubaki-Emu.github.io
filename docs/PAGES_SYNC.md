# Pages repository synchronization

## Canonical direction

- GitLab `chantinlongxthrx/i-steam.github.io`, branch `main`, is the canonical website source.
- GitHub `I-Steam/I-steam.github.io`, branch `main`, is the published mirror.
- GitHub Actions performs the recurring GitLab-to-GitHub synchronization. GitLab CI runners are not required for this mirror.
- The workflow is stored at `.github/workflows/main.yml` and runs on GitHub `main` pushes, manual dispatch, and every 15 minutes.

## Authentication

The GitLab repository is publicly readable, so the mirror workflow needs no GitLab token or GitLab write access.

The built-in GitHub Actions `GITHUB_TOKEN` is not sufficient: GitHub explicitly rejected the mirror push because that token cannot update workflow files under `.github/workflows/` without the special `workflows` permission. The observed failure was:

`refusing to allow a GitHub App to create or update workflow ... without workflows permission`

The workflow therefore uses a dedicated fine-grained personal access token stored as the GitHub repository Actions secret `MIRROR_TOKEN`.

Create a fine-grained token for **only** `I-Steam/I-steam.github.io` with:
- **Contents:** Read and write
- **Workflows:** Read and write

The token owner must have write access to the repository. Add it under GitHub repository **Settings → Secrets and variables → Actions → New repository secret**, with the exact name `MIRROR_TOKEN`. Never put the token in this repository, workflow YAML, README, or message board.

The workflow checks for the secret before checkout and reports a clear error if it is missing. The checkout action uses this token for the subsequent Git push.

## Reconciliation behavior

1. Fetch GitHub `main` and public GitLab `main`.
2. If both refs match, finish without a commit.
3. If GitLab is ahead, fast-forward the GitHub mirror.
4. If GitHub has mirror-only commits and GitLab has no newer commits, leave GitHub unchanged.
5. If both branches have new commits, merge GitLab into GitHub. On content conflicts, prefer GitLab because it is canonical.
6. Push to GitHub using a normal, non-force push. If a merge or push cannot be completed safely, stop and report the failure.

The workflow never pushes to GitLab, never force-pushes, and never requires GitLab CI compute minutes.

## One-time activation

The workflow must exist in the GitHub repository at `.github/workflows/main.yml` for GitHub Actions to execute it. Copy the canonical file from the GitLab repository to that exact path on GitHub once, then add the `MIRROR_TOKEN` repository secret. Open the GitHub Actions tab and manually run **GitLab to GitHub Pages Mirror**.

## Validation and limitations

- The canonical workflow and this guide are committed in GitLab.
- A previous run proved that checkout, public GitLab fetch, and divergent-history merge all succeed. The push failed specifically because the token lacked `workflows` permission.
- A successful mirror push with `MIRROR_TOKEN` is not yet verified.
- A public GitLab repository is assumed. If its visibility changes, provide a read-only GitLab credential and adjust the fetch step.
- Conflicting files prefer GitLab; review future changes to this policy before adding GitHub-only website content.
