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
  1. Fire up Vim and make something awesome!

## Adding Plugins


 1. `git submodule add <url_to_git_repo> vim/bundle/<plugin_name>`
 1. `git submodule init`

## Removing Plugins

Royal pain for git versions 1.7-.

git 1.8

 1. `git submodule deinit <plugin_name>`
 1. `git rm vim/bundle/<plugin_name>`
 
#Utility Scripts
Try ```echo "export PATH=`pwd`/utility_scripts/:\$PATH" >> ~/.bashrc```. You may need to go tidy up your bashrc if it already has an export statement.
