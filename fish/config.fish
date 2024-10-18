set fish_greeting

zoxide init fish | source

set -x VIRTUAL_ENV_DISABLE_PROMPT 1

if status is-interactive
    # Commands to run in interactive sessions can go here
    set FLINE_PATH $HOME/.config/fish/fishline
    source $FLINE_PATH/init.fish
    source $FLINE_PATH/themes/custom.fish
end


# Alias

## System
alias dup="sudo zypper dup"
alias install="sudo zypper install"
alias fzb='fzf --preview="bat --color=always {}"'
alias nzb='nvim $(fzf --preview="bat --color=always {}")'
alias vi='nvim'

## Git
alias gst='git status'
alias gft='git fetch -p'
alias gpl='git pull'
alias gph='git push'
alias gdf='git diff'
alias gus='git reset HEAD --'
alias gad='git add --update'
alias gck='git checkout'
alias gsw='git switch'
alias gcm='git commit -v'
alias gbr='git branch'
alias glg='git log --pretty=format:"%h %s" --graph'
alias gth='git stash'
