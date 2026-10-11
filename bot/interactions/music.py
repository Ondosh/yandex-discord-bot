from .import Bot
from discord import Interaction, app_commands, Embed, Colour
from ..music.YM.fetch_link import fetch_link
from ..music.voice import VoiceManager
from ..music import GM
from ..music.YM.Track import Track
from ..music.YM.Album import Album
from ..music.YM.Playlist import Playlist
from ..music.YM.Wave import Wave
from ..music.event_loop import event_loop


@Bot.tree.command(description="Проигрывание трека")
@app_commands.describe(track="Название Трека/Плейлиста/Альбома/Подкаста/Книги или ссылка(Яндекс.Музыка)!")
@app_commands.rename(track="трек")
async def play(interaction: Interaction, track: str):
    await interaction.response.send_message("Ожидайте...", ephemeral=True)
    if interaction.user.voice:
        mediaItem = await fetch_link(track)
        if not mediaItem:
            await interaction.edit_original_response(content="По вашему запросу ничего не найдено!")
        else:
            await enqueue(interaction, mediaItem)
    else:
        await interaction.edit_original_response(
                content="Для выполнения этого действия вы должны находится в голосовом канале!"
            )


@Bot.tree.command(description="Включить «Мою волну» — бесконечный автоподбор треков")
async def wave(interaction: Interaction):
    await interaction.response.send_message("Ожидайте...", ephemeral=True)
    if interaction.user.voice:
        if wave_in_queue(interaction.guild.id):
            await interaction.edit_original_response(content="«Моя волна» уже в очереди!")
            return

        mediaItem = await Wave().start()
        if wave_in_queue(interaction.guild.id):  # Повторно: пока грузилась волна, её могли включить ещё раз
            await interaction.edit_original_response(content="«Моя волна» уже в очереди!")
        elif not mediaItem:
            await interaction.edit_original_response(content="Не удалось запустить «Мою волну»!")
        else:
            await enqueue(interaction, mediaItem)
    else:
        await interaction.edit_original_response(
                content="Для выполнения этого действия вы должны находится в голосовом канале!"
            )


def wave_in_queue(guild_id: int) -> bool:
    VM = GM.guilds.get(guild_id)
    return bool(VM) and any(isinstance(item, Wave) for item in VM.queue)


async def enqueue(interaction: Interaction, mediaItem):
    """Добавляет mediaItem в очередь и запускает проигрывание, если бот ещё не играет"""
    VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)
    if not VM.queue:
        VM.queue.append(mediaItem)
        try:
            await add_to_queue_message(interaction, mediaItem)
        except: ...
        await event_loop(VM)
        await GM.delete_guild(interaction.guild.id)
    else:
        if interaction.user.voice.channel == VM.voiceChannel:
            VM.queue.append(mediaItem)
            await add_to_queue_message(interaction, mediaItem)
        else:
            await interaction.edit_original_response(content="Похоже бот уже где-то играет!")


async def add_to_queue_message(interaction: Interaction, mediaItem):
    embed = Embed(
        colour=Colour.green(),
        description="{} `{}` добавлен в очередь!"
    )

    if isinstance(mediaItem, Track):
        embed.description = embed.description.format("Трек", mediaItem.title)
    elif isinstance(mediaItem, Album):
        embed.description = embed.description.format("Албом", mediaItem.title)
    elif isinstance(mediaItem, Playlist):
        embed.description = embed.description.format("Плейлист", mediaItem.title)
    elif isinstance(mediaItem, Wave):
        embed.description = "«Моя волна» включена! Чтобы выключить её, нажмите `⏭`, когда она играет."

    await interaction.edit_original_response(embed=embed)
