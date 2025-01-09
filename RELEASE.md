# RELEASES

## Release policy

We strive to improve the repo and fix known issues.

## Checklist

This checklist guides you through preparing, testing and documenting a release.

```
Please ensure to SQUASH MERGE to DEVELOP and MERGE to MAIN
```

###  Squash Merging a Pull Request into Develop

- [ ] Update your current branch with your work
    - [ ] Decide which commits you want to push to your branch.
    - [ ] Update dependencies.
    - [ ] Ensure tests have been ran and passed.
    - [ ] Check whether documentation has been updated and is relevant to any new functionalities.
    - [ ] Commit & push
        - local changes (e.g. from the change log updates): `git commit -am "..."`
        - `git push`

- [ ] Create a Pull Request
    - [ ] Provide an appropriate title for your pull request.
    - [ ] Choose a REVIEWER from the [Code Owners List](./CODEOWNERS.md).
    - [ ] Use appropriate labels on your pull request, under Labels on the right hand side.
    - [ ] If necessary link issues into your pull request by selecting an ID under Development on the right hand side.
    - [ ] Check whether all tests have passed and that Sonarcloud has not flagged any issues. If there are any issues please make the changes on your branch.

- [ ] Review and Approve a Pull Request
    - [ ] The REVIEWER must review the code and ask questions/comment where appropriate.
    - [ ] Before the REVIEWER can squash merge into Develop all comments/questions should be closed and all checks must be passed.
    - [ ] The REVIEWER  who approves the request must do a __SQUASH MERGE__ into Develop.

### Merging Develop to Main

- [ ] Create a Pull Request from Develop to Main
    - [ ] Provide the the version number ie. vX.X.X as the title.
    - [ ] Choose two REVIEWERs from the [Code Owners List](./CODEOWNERS.md), under Reviewers on the right hand side.
    - [ ] Check whether all tests have passed and that Sonarcloud has not flagged any issues. If there are any issues you will not be able to merge.

- [ ] Review and Approve a Pull Request
    - [ ] The REVIEWERs must ensure that the only changes into Main are coming from Develop.
    - [ ] The REVIEWER must review the code and ask questions/comment where appropriate.
    - [ ] Before the REVIEWER can  merge into Main all comments/questions should be closed and all checks must be passed.
    - [ ] The REVIEWERs who approves the request must __MERGE__ into Main.

### Creating a New Release from Main

- [ ] Verify you have successfully merged into Main 

- [ ] Create a New Realease
    - [ ] Click on the _Release_ tab on the right hand side of the repository.
    - [ ] Click on the _Draft a new release_ button
    - [ ] Provide an appropriate Tag Name, please use the version number ie. vX.X.X
    - [ ] Select main as the Target
    - [ ] Provide an appropriate Title, please use the version number ie. vX.X.X
    - [ ] Click the _Generate release notes_ button.
    - [ ] Verify the Notes.
    - [ ] Tick the  _Set as the latest release_ option.
    - [ ] Create your release by clicking the  _Publish release_ button.
    
- [ ] Verify the Release is Successful
    - [ ] If the release has failed troubleshoot the issue and re run the job.
    - [ ] Mention the release on suitable social media accounts.