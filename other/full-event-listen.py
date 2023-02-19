import discord
import typing
import datetime

class Bot(discord.Client):

    async def on_raw_app_command_permissions_update(
            self,
            payload: discord.RawAppCommandPermissionsUpdateEvent
):
        return

    async def on_app_command_completion(
            self,
            interaction: discord.Interaction,
            command: typing.Union[discord.app_commands.Command,discord.app_commands.ContextMenu]
):
        return

    async def on_automod_rule_create(
            self,
            rule: discord.AutoModRule
):
        return

    async def on_automod_rule_update(
            self,
            rule: discord.AutoModRule
):
        return

    async def on_automod_rule_delete(
            self,
            rule: discord.AutoModRule
):
        return

    async def on_automod_action(
            self,
            execution: discord.AutoModAction
):
        return

    async def on_guild_channel_create(
            self,
            channel: discord.abc.GuildChannel
):
        return

    async def on_guild_channel_delete(
            self,
            channel: discord.abc.GuildChannel
):
        return

    async def on_guild_channel_update(
            self,
            before: discord.abc.GuildChannel,
            after: discord.abc.GuildChannel
):
        return

    async def on_guild_channel_pins_update(
            self,
            channel: typing.Union[discord.abc.GuildChannel, discord.Thread],
            last_pin: typing.Optional[datetime.datetime]
):
        return

    async def on_private_channel_update(
            self,
            before: discord.GroupChannel,
            after: discord.GroupChannel
):
        return

    async def on_private_channel_pins_update(
            self,
            channel: discord.abc.PrivateChannel,
            last_pin: typing.Optional[datetime.datetime]
):
        return

    async def on_typing(
            self,
            channel: discord.abc.Messageable,
            user: typing.Union[discord.User,discord.Member],
            when: datetime.datetime
):
        return

    async def on_raw_typing(
            self,
            payload: discord.RawTypingEvent
):
        return

    async def on_connect(
            self
):
        return

    async def on_disconnect(
            self
    ):
        return

    async def on_shard_connect(
            self,
            shard_id: int
):
        return

    async def on_shard_disconnect(
            self,
            shard_id: int
):
        return

    async def on_error(
            self,
            event: str,
            *args,
            **kwargs
):
        return

    async def on_socket_event_type(
            self,
            event_type: str
):
        return

    async def on_socket_raw_receive(
            self,
            msg: str
):
        return

    async def on_socket_raw_send(
            self,
            payload
):
        return

    async def on_ready(
            self
):
        return

    async def on_resumed(
            self
):
        return

    async def on_shard_ready(
            self,
            shard_id: int
):
        return

    async def on_shard_resumed(
            self,
            shard_id: int
):
        return

    async def on_guild_available(
            self,
            guild: discord.Guild
):
        return

    async def on_guild_unavailable(
            self,
            guild: discord.Guild):
        return

    async def on_guild_join(
            self,
            guild: discord.Guild):
        return

    async def on_guild_remove(
            self,
            guild: discord.Guild):
        return

    async def on_guild_update(
            self,
            before: discord.Guild,
            after: discord.Guild
):
        return

    async def on_guild_emojis_update(
            self,
            guild: discord.Guild,
            before: typing.Sequence[discord.Emoji],
            after: typing.Sequence[discord.Emoji]
):
        return

    async def on_guild_stickers_update(
            self,
            guild: discord.Guild,
            before: typing.Sequence[discord.GuildSticker],
            after: typing.Sequence[discord.GuildSticker]
):
        return

    async def on_audit_log_entry_create(
            self,
            entry: discord.AuditLogEntry
):
        return

    async def on_invite_create(
            self,
            invite: discord.Invite
):
        return

    async def on_invite_delete(
            self,
            invite: discord.Invite
):
        return

    async def on_integration_create(
            self,
            integration: discord.Integration
):
        return

    async def on_integration_update(
            self,
            integration: discord.Integration
):
        return

    async def on_guild_integrations_update(
            self,
            guild: discord.Guild
):
        return

    async def on_webhooks_update(
            self,
            channel: discord.abc.GuildChannel
):
        return

    async def on_raw_integration_delete(
            self,
            payload: discord.RawIntegrationDeleteEvent
):
        return

    async def on_interaction(
            self,
            interaction: discord.Interaction
):
        return

    async def on_member_join(
            self,
            member: discord.Member
):
        return

    async def on_member_remove(
            self,
            member: discord.Member
):
        return

    async def on_raw_member_remove(
            self,
            payload: discord.RawMemberRemoveEvent
):

        return

    async def on_member_update(
            self,
            before: discord.Member,
            after: discord.Member
):
        return

    async def on_user_update(
            self,
            before: discord.User,
            after: discord.User
):
        return

    async def on_member_ban(
            self,
            guild: discord.Guild,
            user: typing.Union[discord.User, discord.Member]
):
        return

    async def on_member_unban(
            self,
            guild: discord.Guild,
            user: discord.User
):
        return

    async def on_presence_update(
            self,
            before: discord.Member,
            after: discord.Member
):
        return

    async def on_message(
            self,
            message: discord.Message
):
        return

    async def on_message_edit(
            self,
            before: discord.Message,
            after: discord.Message
):
        return

    async def on_message_delete(
            self,
            message: discord.Message
):
        return

    async def on_bulk_message_delete(
            self,
            messages: list[discord.Message]
):
        return

    async def on_raw_message_edit(
            self,
            payload: discord.RawMessageUpdateEvent
):
        return

    async def on_raw_message_delete(
            self,
            payload: discord.RawMessageDeleteEvent
):
        return

    async def on_raw_bulk_message_delete(
            self,
            payload: discord.RawBulkMessageDeleteEvent
):
        return

    async def on_reaction_add(
            self,
            reaction: discord.Reaction,
            user: typing.Union[discord.Member, discord.User]
):
        return

    async def on_reaction_remove(
            self,
            reaction: discord.Reaction,
            user: typing.Union[discord.Member, discord.User]
):
        return

    async def on_reaction_clear(
            self,
            message: discord.Message,
            reactions: list[discord.Reaction]
):
        return

    async def on_reaction_clear_emoji(
            self,
            reaction: discord.Reaction
):
        return

    async def on_raw_reaction_add(
            self,
            payload: discord.RawReactionActionEvent
):
        return

    async def on_raw_reaction_remove(
            self,
            payload: discord.RawReactionActionEvent
):
        return

    async def on_raw_reaction_clear(
            self,
            payload: discord.RawReactionClearEvent
):
        return

    async def on_raw_reaction_clear_emoji(
            self,
            payload: discord.RawReactionClearEmojiEvent
):
        return

    async def on_guild_role_create(
            self,
            role: discord.Role
):
        return

    async def on_guild_role_delete(
            self,
            role: discord.Role
):
        return

    async def on_guild_role_update(
            self,
            before: discord.Role,
            after: discord.Role
):
        return

    async def on_scheduled_event_create(
            self,
            event: discord.ScheduledEvent
):
        return

    async def on_scheduled_event_delete(
            self,
            event: discord.ScheduledEvent
):
        return

    async def on_scheduled_event_update(
            self,
            before: discord.ScheduledEvent,
            after: discord.ScheduledEvent
):
        return

    async def on_scheduled_event_user_add(
            self,
            event: discord.ScheduledEvent,
            user: discord.User
):
        return

    async def on_scheduled_event_user_remove(
            self,
            event: discord.ScheduledEvent,
            user: discord.User
):
        return

    async def on_stage_instance_create(
            self,
            stage_instance: discord.StageInstance
):
        return

    async def on_stage_instance_delete(
            self,
            stage_instance: discord.StageInstance
):
        return

    async def on_stage_instance_update(
            self,
            before: discord.StageInstance,
            after:discord.StageInstance
):
        return

    async def on_thread_create(
            self,
            thread: discord.Thread
):
        return

    async def on_thread_join(
            self,
            thread: discord.Thread
):
        return

    async def on_thread_update(
            self,
            before: discord.Thread,
            after: discord.Thread
):
        return

    async def on_thread_remove(
            self,
            thread: discord.Thread
):
        return

    async def on_thread_delete(
            self,
            thread: discord.Thread
):
        return

    async def on_raw_thread_update(
            self,
            payload: discord.RawThreadUpdateEvent
):
        return

    async def on_raw_thread_delete(
            self,
            payload: discord.RawThreadDeleteEvent
):
        return

    async def on_thread_member_join(
            self,
            member: discord.ThreadMember
):
        return

    async def on_thread_member_remove(
            self,
            member: discord.ThreadMember
):
        return

    async def on_raw_thread_member_remove(
            self,
            payload # Payload data is not supported for this event | このイベントではpayloadのclassがありません
            # TODO: payload classがリリースされたらアノテーションを追加する
):
        return

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
):
        return
