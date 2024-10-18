# Dotfiles

## Steps

1. Install [GNU stow](https://www.gnu.org/software/stow/).

2. Install dependencies.

   - Git
   - Fish (shell)
   - zoxide (smarter cd command)
   - Alacritty (terminal emulator)
   - tmux (terminal multiplexer)
   - QTile (Window manager)
   - rofi (system menus)
   - i3lock (screen locker)
   - picom (compositor for X)
   - nvim (editor)
   - lxappearance

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
