# conf-repo

## RATIONALITY

I use a lot of different softwares, and many of the I have to tweak their conf or rc files to my needs.

I'm also used to have some shell scripts to different purposes.

I don't like to use just a simple backup, because I need the features of version control system: rolling back, diffs, even sharing thoughts and discuss them with other people.

## IDEAS

After digging a little, I came to the idea of creating a subdir with all the config txt files hardlinked, so when I send a git add . or a git status command, I can see every change like in any normal repo.

## ROADMAP

- Linker: This should create hard links. First, on creating the repo it hardlink conf files to the special repo. And, if the repo is clonned in a newly setup system, update and harlink back to the mandatory conf sites.
- Crawler: This dig into the user home directory, seeking for files that "looks-alike" config or simple scripts files. Persists a list of included and excluded files, and can notify me if new files that conforms the criteria were added.
- Secret: some txt include secrets, like passwords and tokens. This should not be added like normal files, this should be encrypted. Now, this will be excluded from "normal" config-repo and added to a "secret" config repo. This may be added to a .git-secret schema.

## CONSIDERATIONS

I'm a linux user, so this will work on any posix operating system. 
The config repo path will be added to the config file of this program located in ~/.config/conf-repo.conf and by default will be ~/.local/conf-repo
