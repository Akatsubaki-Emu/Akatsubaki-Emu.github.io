# GitHub Actions CI/CD and GitLab mirror synchronization

## Canonical repository and mirror

- **Canonical development destination:** https://github.com/Akatsubaki-Emu/Akatsubaki-Emu, existing branch `main`.
- **GitLab mirror:** https://gitlab.com/chantinlongxthrx/I-steam, existing branch `main`.
- GitHub `main` is authoritative. New source, workflow and documentation commits are made directly on GitHub `main`; GitLab is a downstream mirror.
- The GitHub-to-GitLab sync workflow pushes only when GitLab `main` is an ancestor of GitHub `main`. It refuses divergent or newer GitLab history and never force-pushes.
- GitLab-to-GitHub reconciliation is a separate, manual operation. It is restricted to the organization owner and requires an explicit authorization input; do not use it to bypass review of GitLab-only commits.

## GitHub Actions workflows

- `validate-repository.yml` — workflow/project YAML, source-contract, Python, native C/C++ and Swift runtime validation.
- `validate-ios-build.yml` — iOS, tvOS and visionOS simulator compilation.
- `build-core-only-ios.yml` — QEMU-free diagnostic iOS IPA.
- `build-qemu-runtime.yml` — physical iOS arm64 QEMU/UTM JIT and TCI runtime variants.
- `release.yml` — release orchestration, asset validation and publication.
- `blank.yml` — GitHub-to-GitLab fast-forward-only synchronization.
- `reconcile-gitlab-main.yml` — manual, owner-authorized GitLab-to-GitHub history integration.
- `.gitlab-ci.yml` is retired for Apple-platform builds; GitHub Actions owns Apple-platform validation.

## Synchronization rules

1. GitHub `main` is canonical; GitLab `main` is a downstream mirror.
2. Sync pushes only when GitLab is an ancestor of GitHub; it refuses divergent or newer GitLab history.
3. Review GitLab-only commits individually. Merge only after explicit owner authorization for this repository and exact history.
4. Never create branches, force-push, reset or discard commits.
5. Verify both SHAs before claiming synchronization.
6. Queued, skipped, cancelled or failed workflow jobs are not passing tests.
7. Simulator compilation, IPA archiving or QEMU compilation does not prove physical-device guest execution.

## Required secret

- `GITLAB_TOKEN`: minimum GitLab repository write scope for the GitHub-to-GitLab sync workflow. Never commit credentials.
