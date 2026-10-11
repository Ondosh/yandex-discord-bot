from .import Bot
from discord import Interaction, Colour, Embed


@Bot.tree.command(description="Помощь")
async def help(interaction: Interaction):
    commands = {command.name: command for command in await Bot.tree.fetch_commands()}
    embed = Embed(
        title="Помощь",
        description="Здесь описаны все существующие команды бота:",
        color=Colour.blurple()
    )
    embed.add_field(
        name="Музыка",
        value=  f"{commands['play'].mention} - проигрывание Трека/Альбома/Плейлиста/Подкаста/Книги из Яндекс.Музыки.\n"
                f"{commands['wave'].mention} - «Моя волна»: бесконечный автоподбор треков.\n\n"
                "Данный бот проигрывает Треки/Альбомы/Плейлисты/Подкасты/Книги из Яндекс.Музыки" \
                f"Чтобы воспроизвести что либо вы можете отправить ссылку/название трека или отрывок из него этой командой!",
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)