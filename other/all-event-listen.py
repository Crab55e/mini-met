import discord
class Bot(discord.client):

    async def on_raw_app_command_permissions_update(payload):
        pass

    async def on_app_command_completion(interaction, command):
        pass

    async def on_automod_rule_create(rule):
        pass

    async def on_automod_rule_update(rule):
        pass

    async def on_automod_rule_delete(rule):
        pass

    async def on_automod_action(execution):
        pass

    async def on_guild_channel_create(channel):
        pass

    async def on_guild_channel_delete(channel):
        pass

    async def on_guild_channel_update(before, after):
        pass

    async def on_guild_channel_pins_update(channel, last_pin):
        pass

    async def on_private_channel_update(before, after):
        pass

    async def on_private_channel_pins_update(channel, last_pin):
        pass

    async def on_typing(channel, user, when):
        pass

    async def on_raw_typing(payload):
        pass

    async def on_connect():
        pass

    async def on_disconnect():
        pass

    async def on_shard_connect(shard_id):
        pass

    async def on_shard_disconnect(shard_id):
        pass

    async def on_error(event, args, kwargs):
        pass

    async def on_socket_event_type(event_type):
        pass

    async def on_socket_raw_receive(msg):
        pass

    async def on_socket_raw_send(payload):
        pass

    async def on_ready():
        pass

    async def on_resumed():
        pass

    async def on_shard_ready(shard_id):
        pass

    async def on_shard_resumed(shard_id):
        pass

    async def on_guild_available(guild):
        pass

    async def on_guild_unavailable(guild):
        pass

    async def on_guild_join(guild):
        pass

    async def on_guild_remove(guild):
        pass

    async def on_guild_update(before, after):
        pass

    async def on_guild_emojis_update(guild, before, after):
        pass

    async def on_guild_stickers_update(guild, before, after):
        pass

    async def on_invite_create(invite):
        pass

    async def on_invite_delete(invite):
        pass

    async def on_integration_create(integration):
        pass

    async def on_integration_update(integration):
        pass

    async def on_guild_integrations_update(guild):
        pass

    async def on_webhooks_update(channel):
        pass

    async def on_raw_integration_delete(payload):
        pass

    async def on_interaction(interaction):
        pass

    async def on_member_join(member):
        pass

    async def on_member_remove(member):
        pass

    async def on_raw_member_remove(payload):
        pass

    async def on_member_update(before, after):
        pass

    async def on_user_update(before, after):
        pass

    async def on_member_ban(guild, user):
        pass

    async def on_member_unban(guild, user):
        pass

    async def on_presence_update(before, after):
        pass

    async def on_message(message):
        pass

    async def on_message_edit(before, after):
        pass

    async def on_message_delete(message):
        pass

    async def on_bulk_message_delete(messages):
        pass

    async def on_raw_message_edit(payload):
        pass

    async def on_raw_message_delete(payload):
        pass

    async def on_raw_bulk_message_delete(payload):
        pass

    async def on_reaction_add(reaction, user):
        pass

    async def on_reaction_remove(reaction, user):
        pass

    async def on_reaction_clear(message, reactions):
        pass

    async def on_reaction_clear_emoji(reaction):
        pass

    async def on_raw_reaction_add(payload):
        pass

    async def on_raw_reaction_remove(payload):
        pass

    async def on_raw_reaction_clear(payload):
        pass

    async def on_raw_reaction_clear_emoji(payload):
        pass

    async def on_guild_role_create(role):
        pass

    async def on_guild_role_delete(role):
        pass

    async def on_guild_role_update(before, after):
        pass

    async def on_scheduled_event_create(event):
        pass

    async def on_scheduled_event_delete(event):
        pass

    async def on_scheduled_event_update(before, after):
        pass

    async def on_scheduled_event_user_add(event, user):
        pass

    async def on_scheduled_event_user_remove(event, user):
        pass

    async def on_stage_instance_create(stage_instance):
        pass

    async def on_stage_instance_delete(stage_instance):
        pass

    async def on_stage_instance_update(before, after):
        pass

    async def on_thread_create(thread):
        pass

    async def on_thread_join(thread):
        pass

    async def on_thread_update(before, after):
        pass

    async def on_thread_remove(thread):
        pass

    async def on_thread_delete(thread):
        pass

    async def on_raw_thread_update(payload):
        pass

    async def on_raw_thread_delete(payload):
        pass

    async def on_thread_member_join(member):
        pass

    async def on_thread_member_remove(member):
        pass

    async def on_raw_thread_member_remove(payload):
        pass

    async def on_voice_state_update(member, before, after):
        pass
