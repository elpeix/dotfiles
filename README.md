# Dotfiles

## Steps

1. Install [GNU stow](https://www.gnu.org/software/stow/).

2. Install dependencies.

   - Git
   - Fish (shell)
   - zoxide (smarter cd command)
   - fzf (search all in terminal)
   - Alacritty (terminal emulator)
   - tmux (terminal multiplexer)
     - [tmux plugins](https://github.com/tmux-plugins/tpm)
   - QTile (Window manager)
   - rofi (system menus)
   - i3lock (screen locker)
   - picom (compositor for X)
   - neovim (editor)
   - lazygit (awesome git in terminal)
   - lxappearance (gtk themes, icons, cursor)
     - Icons: papirus
   - [Nerd Fonts](https://www.nerdfonts.com/)

3. Clone dotfiles repo to home directory.

   ```console
   git clone https://github.com/elpeix/dotfiles.git ~/.dotfiles
   ```

4. Use GNU stow to symlink the directories.

   ### Fish, Tmux, Nvim, Alacritty, etc. to ~/.config

   ```console
   cd .dotfiles
   stow .
   ```
