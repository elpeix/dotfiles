-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")

vim.cmd(":Copilot disable")
local copilot_enabled = false
vim.api.nvim_create_user_command("ToggleCopilot", function()
  if copilot_enabled then
    vim.cmd(":Copilot disable")
    copilot_enabled = false
  else
    vim.cmd(":Copilot enable")
    copilot_enabled = true
  end
end, {})
