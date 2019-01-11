### Release Procedure

*On Local*
- Finish features
- Start release branch
- Add and commit release notes
- Finish release branch
- `git push`

*On LIVE*
- `git status`
- Check and resolve any diffs
- `git reset --hard HEAD` (or `git stash`)
- `git pull`
- Make any changes out of repo (e.g. in /private or ~/web2py)
- Modify version number in appconfig.ini
- Restart server if needed

 *Finally*
 - Move appropriate cards in Trello to Done
 - Resolve any Bitbucket/github issues and tag with release merge commit
