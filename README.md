# standard version release branch

Github action to open releases following [conventional-commits](https://www.conventionalcommits.org/en/v1.0.0/), in order:

- Create a release branch
- Update Changelog and tags with [standard-version](https://github.com/conventional-changelog/standard-version)
- Push the brand new branch to your repo
- Open the pull request against the branch you specify

## Usage

### Example Workflow file

```yaml
name: Create Release Branch

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'The version you want to release.'
        required: false

jobs:
  create-release-branch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - uses: Wuerike/standard-version-release-branch@1.2.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          release_version: ${{ github.event.inputs.version }}
          origin_branch: develop
          target_branch: master
          as_draft: true
          pr_template: 'PR opened by [standard-version-release-branch](https://github.com/Wuerike/standard-version-release-branch)'
```
### Inputs

| Name              | Type      | Description |
| -------           | ------    | ----------- |
| `github_token`    | string    | Github Token with write permissions **Required**|
| `release_version` | string    | Version you want to release, in the formart MAJOR.MINOR.PATH **Optional**|
| `origin_branch`   | string    | Branch from where the release should be opened, usually develop **Required**|
| `target_branch`   | string    | Branch where the release should be merged, usually master or main **Required**|
| `as_draft`        | bool      | Boolean flag to open as draft or not, **Default: False**|
| `pr_template`     | string    | Template to be used as PR description **Default: "PR opened by [standard-version-release-branch](https://github.com/Wuerike/standard-version-release-branch)"** |

## Contributing

This project is totally open source and contributors are welcome.

### Workflow

We use GitFlow, you can find more about this workfow here.

### Branching

- **New Features** `feat/<Name-of-feature>` from `develop`.
- **Bugfix** `fix/<Name-of-bugfix>` from `develop`.
- **Hotfix** `hotfix/<Name-of-hotfix>` from `master`.

### Commit messages

See [standard-version](https://github.com/conventional-changelog/standard-version#commit-message-convention-at-a-glance) for commit guidelines.
