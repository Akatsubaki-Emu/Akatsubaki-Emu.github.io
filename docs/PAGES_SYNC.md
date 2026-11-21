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


## Revalidation — 2026-11-10

The latest available GitHub Actions mirror run inspected during this review was:

- Run: https://github.com/I-Steam/I-steam.github.io/actions/runs/42434495593
- Run ID: `42434495593`
- Job ID: `128590344406`
- Commit on GitHub: `428a372743406a4e3f9c29ae5bb82ced4ac972fe`
- Result: failed at **Push mirror update to GitHub**.
- Checkout, GitLab fetch, and reconciliation/merge all succeeded.
- The exact rejection remains: `refusing to allow a GitHub App to create or update workflow '.github/workflows/main.yml' without 'workflows' permission`.

The GitHub branch still contains the old workflow (blob SHA `7f79c8b7be522b5bcd98de01becf4f102ec3f778`), not this canonical token-authenticated workflow. A direct GitHub file update attempt returned HTTP 403 `Resource not accessible by integration`. Therefore the GitLab-side change is prepared and committed, but GitHub activation and the secret are outstanding.

### Local validation performed

- YAML parsing confirmed the quoted `"on"` key and all three triggers (`push`, `workflow_dispatch`, `schedule`).
- Embedded Bash scripts passed `bash -n` syntax validation.
- A temporary local Git test repository exercised the three reconciliation cases:
  - GitLab-ahead fast-forward: passed.
  - GitHub-ahead preservation: passed.
  - Diverged histories with a conflicting file: passed, with GitLab's content winning.
- These are logic/syntax tests, not a successful GitHub-hosted mirror run.

### Remaining activation requirement

A repository owner with sufficient GitHub access must replace `.github/workflows/main.yml` with the canonical file and add the `MIRROR_TOKEN` Actions secret. The token must be scoped to this repository with **Contents: Read and write** and **Workflows: Read and write**. Afterward, manually run the workflow and verify the push step and branch contents. Do not mark synchronization fully operational before that end-to-end test passes.


## Xthrx AltSource catalogue

- The source manifest is \`tools/xthrx-alt-source/sources.json\` and currently contains 125 unique HTTP(S) candidate feeds.
- \`tools/xthrx-alt-source/build_xthrx_repo.py\` fetches each candidate independently, accepts supported AltStore / SideStore / PAL JSON layouts, normalises version metadata, and deduplicates by exact bundle identifier.
- \`tools/xthrx-alt-source/test_build_xthrx_repo.py\` provides offline regression coverage. The updater runs these tests before making upstream requests.
- GitHub Actions workflow: \`.github/workflows/update-xthrx-alt-source.yml\`; it runs every six hours, on relevant source changes, or manually.
- Generated catalogue: \`altsource/Xthrx's repo.json\`.
- Feed health report: \`altsource/xthrx-source-report.json\`.
- Public source URL after the GitHub Pages deployment and first successful catalogue run: https://akatsubaki-emu.github.io/altsource/Xthrx%27s%20repo.json

The 125 configured URLs are candidates, not a claim that all are online or compatible. The report records per-feed success/failure and valid/rejected app counts. If no compatible apps are found, the builder exits non-zero and does not replace the published catalogue with an empty file. SideStore-required version sizes are populated with the upstream size or zero when omitted.

The source generator and Pages files are committed in the GitLab canonical repository. The corresponding GitHub mirror must contain the same files before the GitHub Actions updater can run. A successful unit-test run does not prove that any particular upstream feed is live; the first hosted run is required to measure actual feed health.
