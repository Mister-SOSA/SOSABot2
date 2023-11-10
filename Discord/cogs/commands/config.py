from discord.ext import commands
from common.utils import configutil as cfg
import discord

CONFIG_KEY_CHOICES = [discord.app_commands.Choice(name=key, value=key) for key in cfg.fetch_convar_keys()]

@commands.has_any_role("SOSA", "Admin")
@commands.hybrid_command(
    name="config", 
    description='View or change convars.'
)
@discord.app_commands.choices(action=[
    discord.app_commands.Choice(name="View", value="View"),
    discord.app_commands.Choice(name="Set", value="Set")
],
                              convar=CONFIG_KEY_CHOICES
)
async def config(
    ctx,
    action: discord.app_commands.Choice[str],
    convar: str = None,
    value: str = None,
):
    action = action.value
    
    if action == "View":
        cfg_json = cfg.fetch_convars()
        
        embed = discord.Embed(
            title = "🔧 Config",
            description = f"",
            color=discord.Color.lighter_gray()
        )
        
        for convar in cfg_json:
            embed.add_field(
                name=convar,
                value=f"`{cfg_json[convar]}`",
                inline=False
            )
            
        await ctx.send(embed=embed)
        
        return
    
    if action == "Set":
        cfg.set_convar(convar, value)
        
        embed = discord.Embed(
            title = "🔧 Config",
            description = f"Set `{convar}` to `{value}`.",
           color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
        
        return
    
    await ctx.send("Invalid action.", ephemeral=True)


async def setup(client):
    client.add_command(config)
