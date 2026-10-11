from discord import ui, ButtonStyle, Interaction, Embed, Colour
from ...music import GM
from ...music.voice import VoiceManager
from ...music.YM.Track import Track
from ...music.YM.Wave import Wave


def check_voice(func):
    async def wrapper(*args, **kwargs):
        if args[1].user.voice:
            return await func(*args)
        else:
            await args[1].response.send_message(
                "Для выполнения этого действия вы должны находится в голосовом канале!",
                ephemeral=True
            )
    return wrapper


class MediaPlayer(ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @ui.button(label="⏸", style=ButtonStyle.green, custom_id="play_or_pause")
    @check_voice
    async def play_or_pause(self, interaction: Interaction, button: ui.Button):
        VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)
        if not interaction.user.voice.channel or interaction.user.voice.channel.id != VM.voiceChannel.id:
            await interaction.response.send_message(
                "Для этого действия вам нужно находится в текущем голосом канале!",
                ephemeral=True
            )
        else:
            if not VM.voiceClient.is_paused():
                VM.voiceClient.pause()
                button.label = "▶️"
                button.style = ButtonStyle.red
            else:
                VM.voiceClient.resume()
                button.label = "⏸"
                button.style = ButtonStyle.green
            await interaction.response.edit_message(view=self)
            
    
    @ui.button(label="⏩", style=ButtonStyle.blurple, custom_id="skip_track")
    @check_voice
    async def skip_track(self, interaction: Interaction, button: ui.Button):
        VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)
        if not interaction.user.voice.channel or interaction.user.voice.channel.id != VM.voiceChannel.id:
            await interaction.response.send_message(
                "Для этого действия вам нужно находится в текущем голосом канале!",
                ephemeral=True
            )
        else:
            VM.voiceClient.stop()

            await interaction.response.edit_message(view=self)
    

    @ui.button(label="⏭", style=ButtonStyle.blurple, custom_id="skip_playlist")
    @check_voice
    async def skip_playlist(self, interaction: Interaction, button: ui.Button):
        VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)
        if not interaction.user.voice.channel or interaction.user.voice.channel.id != VM.voiceChannel.id:
             await interaction.response.send_message(
                "Для этого действия вам нужно находится в текущем голосом канале!",
                ephemeral=True
            )
        else:
            VM.counter = 0
            await VM.skip(playlist=True)
            VM.voiceClient.stop()
            await interaction.response.edit_message(view=self)


    @ui.button(label="⏹", style=ButtonStyle.red, custom_id="stop")
    @check_voice
    async def stop(self, interaction: Interaction, button:ui.Button):
        VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)
        if not interaction.user.voice.channel or interaction.user.voice.channel.id != VM.voiceChannel.id:
             await interaction.response.send_message(
                "Для этого действия вам нужно находится в текущем голосом канале!",
                ephemeral=True
            )
        else:
            VM.queue.clear()
            VM.voiceClient.stop()

    
    @ui.button(label="❔", style=ButtonStyle.grey, custom_id="help", row=1)
    async def help(self, interaction: Interaction, button: ui.Button):
        embed = Embed(
            title="Подсказка",
            colour=Colour.green()
        )

        embed.description = "Данный бот проигрывает Треки/Альбомы/Плейлисты/Подкасты/Книги" \
                            " из Яндекс.Музыки!\n\n" \
                            "Вы можете добавить трек отправив ссылку/название трека или отрывок из песни с помощью команды: </play:1111348061596287157>\n\n" \
                            
        embed.add_field(
            name="Подсказки по кнопкам",
            value = "`▶️\⏸` - Паузка или продолжение проигрывания.\n" \
                    "`⏩` - Пропустить один Трек\Подкаст\Книгу в очереди.\n" \
                    "`⏭` - Пропустить целый плейлист в очереди или выключить «Мою волну».\n" \
                    "`⏹` - Полностью остановить проигрывание и очистить очередь!\n" \
                    "`📃` - Очередь треков."
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
    

    @ui.button(label="📃", style=ButtonStyle.blurple, custom_id="queue", row=1)
    @check_voice
    async def queue(self, interaction: Interaction, button: ui.Button):
        embed = Embed(
            title="Очередь треков"
        )

        VM: VoiceManager = await GM.get_guild(interaction.user.voice.channel, interaction.channel)

        for mediaItem in VM.queue[:8]:
            if isinstance(mediaItem, Track):
                mediaItemQueue = []
                if mediaItem.artists:
                    artists = ", ".join([artist.name for artist in mediaItem.artists])
                    mediaItemQueue.append(f"**{artists}** - _{mediaItem.title}_")
                else:
                    mediaItemQueue.append(f"_{mediaItem.title}_")
        
                embed.add_field(
                    name="Трек",
                    value='\n'.join(mediaItemQueue)
                )
            else:
                mediaItemQueue = []
                for index, item in enumerate(mediaItem.tracks[:8]):
                    if item.artists:
                        artists = ", ".join([artist.name for artist in item.artists])
                        mediaItemQueue.append(f"{index+1}. **{artists}** - _{item.title}_")
                    else:
                        mediaItemQueue.append(f"{index+1}. _{item.title}_")

                if isinstance(mediaItem, Wave):
                    mediaItemQueue.append("\nСледующие треки подбираются автоматически")
                elif len(mediaItem.tracks) > 8:
                    mediaItemQueue.append(f"\n И ещё {len(mediaItem.tracks) - 8} треков!")

                embed.add_field(
                    name = mediaItem.title,
                    value='\n'.join(mediaItemQueue)
                )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)





