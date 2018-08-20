A directory containing files I use to configure my dev environment. See the various sections for installation info.

#Vim

  1. To use the vimrc file in the repo, create a vimrc in your home directory with the following, substituting `<path_to_this_readme_dir>` with a real one.
  ```vim
    fun! MySys()
      return "linux"
    endfun

    set runtimepath=<path_to_this_readme_dir>/vim,$VIMRUNTIME
    source <path_to_this_readme_dir>/vim/vimrc
  ```
  1. Run ```git submodule update --init``` to install the submodules
  1. Compile Command-T:
    1. `cd ./vim/bundle/command-t/ruby/command-t`
    1. `ruby extconf.rb`
    1. `make`
  1. Optional: Install eslint for better JavaScript warnings
    1. npm install -g eslint
    1. npm install -g babel-eslint
  1. Optional: Install flake8 for better Python warnings
    1. pip install flake8
  1. Fire up Vim and make something awesome!

## Adding Plugins

 1. `git submodule add <url_to_git_repo> vim/bundle/<plugin_name>`
 1. `git submodule init`

## Updating Plugins

1. `git submodule update --remote vim/bundle/<plugin_name>`

## Removing Plugins

git 1.8+

 1. `git submodule deinit vim/bundle/<plugin_name>`
 1. `git rm vim/bundle/<plugin_name>`

Royal pain for git versions 1.7-.

 1. Delete the relevant section from the .gitmodules file.
 1. `git add .gitmodules`
 1. Delete the relevant section from .git/config.
 1. `git rm --cached path_to_submodule` (no trailing slash).
 1. `rm -rf .git/modules/path_to_submodule` (may not exist)
 1. `git commit -m "Removed submodule <name>"`
 1. `rm -rf path_to_submodule` Delete the now untracked submodule files

#Utility Scripts

Try ```echo "export PATH=`pwd`/utility_scripts/:\$PATH" >> ~/.bashrc```. You may need to go tidy up your bashrc if it already has an export statement.
