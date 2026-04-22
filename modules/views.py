import discord

class ConfirmView(discord.ui.View):
    def __init__(self, author, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message(
                "This isn't your confirmation.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
    async def confirm(self, button, interaction):
        self.value = True
        self.disable_all_items()
        await interaction.response.edit_message(content="Confirmed.", view=self)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, button, interaction):
        self.value = False
        self.disable_all_items()
        await interaction.response.edit_message(content="Cancelled.", view=self)
        self.stop()

    async def timeout_event(self):
        self.disable_buttons()
        self.stop()

    def disable_buttons(self):
        for item in self.children:
            item.disabled = True