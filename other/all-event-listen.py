import discord


# メインの変数を定義
print(console_prefix, "Setting main variables..")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot_token = "TOKEN"
try:
    # "アプリケーションコマンド" イベント

    @client.event
    async def on_raw_app_command_permissions_update(payload):
        print(payload)

    @client.event
    async def on_app_command_completion(interaction, command):
        print(interaction, command)

    # "AutoMod" イベント

    @client.event
    async def on_automod_rule_create(rule):
        print(rule)

    @client.event
    async def on_automod_rule_update(rule):
        print(rule)

    @client.event
    async def on_automod_rule_delete(rule):
        print(rule)

    @client.event
    async def on_automod_action(execution):
        print(execution)

    # "Channels" イベント

    @client.event
    async def on_guild_channel_create(channel):
        print(channel)

    @client.event
    async def on_guild_channel_delete(channel):
        print(channel)

    @client.event
    async def on_guild_channel_update(before, after):
        print(before, after)

    @client.event
    async def on_guild_channel_pins_update(channel, last_pin):
        print(channel, last_pin)

    @client.event
    async def on_private_channel_update(before, after):
        print(before, after)
    
    @client.event
    async def on_private_channel_pins_update(channel, last_pin):
        print(channel, last_pin)

    @client.event
    async def on_typing(channel, user, when):
        print(channel, user, when)

    @client.event
    async def on_raw_typing(payload):
        print(payload)

    # "Connection" イベント
    
    @client.event
    async def on_connect():
        print()

    @client.event
    async def on_disconnect():
        print()

    @client.event
    async def on_shard_connect(shard_id):
        print(shard_id)

    @client.event
    async def on_shard_disconnect(shard_id):
        print(shard_id)

    # "Debug" イベント

    @client.event
    async def on_error(event, args, kwargs):
        print(event, args, kwargs)

    @client.event
    async def on_socket_event_type(event_type):
        print(event_type)

    @client.event
    async def on_socket_raw_receive(msg):
        print(msg)

    @client.event
    async def on_socket_raw_send(payload):
        print(payload)

    # "Gateway" イベント

    @client.event
    async def on_ready():
        print()

    @client.event
    async def on_resumed():
        print()

    @client.event
    async def on_shard_ready(shard_id):
        print(shard_id)

    @client.event
    async def on_shard_resumed(shard_id):
        print(shard_id)

    # "Guilds" イベント

    @client.event
    async def on_guild_available(guild):
        print(guild)

    @client.event
    async def on_guild_unavailable(guild):
        print(guild)

    @client.event
    async def on_guild_join(guild):
        print(guild)

    @client.event
    async def on_guild_remove(guild):
        print(guild)

    @client.event
    async def on_guild_update(before, after):
        print(before, after)

    @client.event
    async def on_guild_emojis_update(guild, before, after):
        print(guild, before, after)

    @client.event
    async def on_guild_stickers_update(guild, before, after):
        print(guild, before, after)

    @client.event
    async def on_invite_create(invite):
        print(invite)

    @client.event
    async def on_invite_delete(invite):
        print(invite)

    # "Integrations" イベント

    @client.event
    async def on_integration_create(integration):
        print(integration)

    @client.event
    async def on_integration_update(integration):
        print(integration)

    @client.event
    async def on_guild_integrations_update(guild):
        print(guild)

    @client.event
    async def on_webhooks_update(channel):
        print(channel)

    @client.event
    async def on_raw_integration_delete(payload):
        print(payload)

    # "Interactions" イベント

    @client.event
    async def on_interaction(interaction):
        print(interaction)

    # "Members" イベント

    @client.event
    async def on_member_join(member):
        print(member)

    @client.event
    async def on_member_remove(member):
        print(member)

    @client.event
    async def on_raw_member_remove(payload):
        print(payload)

    @client.event
    async def on_member_update(before, after):
        print(before, after)

    @client.event
    async def on_user_update(before, after):
        print(before, after)

    @client.event
    async def on_member_ban(guild, user):
        print(guild, user)

    @client.event
    async def on_member_unban(guild, user):
        print(guild, user)

    @client.event
    async def on_presence_update(before, after):
        print(before, after)

    # "Messages" イベント

    @client.event
    async def on_message(message):
        print(message)

    @client.event
    async def on_message_edit(before, after):
        print(before, after)

    @client.event
    async def on_message_delete(message):
        print(message)

    @client.event
    async def on_bulk_message_delete(messages):
        print(messages)
    
    @client.event
    async def on_raw_message_edit(payload):
        print(payload)

    @client.event
    async def on_raw_message_delete(payload):
        print(payload)
    
    @client.event
    async def on_raw_bulk_message_delete(payload):
        print(payload)

    # "Reactions" イベント

    @client.event
    async def on_reaction_add(reaction, user):
        print(reaction, user)

    @client.event
    async def on_reaction_remove(reaction, user):
        print(reaction, user)

    @client.event
    async def on_reaction_clear(message, reactions):
        print(message, reactions)
    
    @client.event
    async def on_reaction_clear_emoji(reaction):
        print(reaction)

    @client.event
    async def on_raw_reaction_add(payload):
        print(payload)
    
    @client.event
    async def on_raw_reaction_remove(payload):
        print(payload)

    @client.event
    async def on_raw_reaction_clear(payload):
        print(payload)

    @client.event
    async def on_raw_reaction_clear_emoji(payload):
        print(payload)

    # "Roles" イベント
    
    @client.event
    async def on_guild_role_create(role):
        print(role)

    @client.event
    async def on_guild_role_delete(role):
        print(role)

    @client.event
    async def on_guild_role_update(before, after):
        print(before, after)

    # "Scheduled Events" イベント
    
    @client.event
    async def on_scheduled_event_create(event):
        print(event)
    
    @client.event
    async def on_scheduled_event_delete(event):
        print(event)

    @client.event
    async def on_scheduled_event_update(before, after):
        print(before,after)

    @client.event
    async def on_scheduled_event_user_add(event, user):
        print(event, user)

    @client.event
    async def on_scheduled_event_user_remove(event, user):
        print(event, user)
    
    # "Stages" イベント

    @client.event
    async def on_stage_instance_create(stage_instance):
        print(stage_instance)

    @client.event
    async def on_stage_instance_delete(stage_instance):
        print(stage_instance)

    @client.event
    async def on_stage_instance_update(before, after):
        print(before, after)

    # "Threads" イベント

    @client.event
    async def on_thread_create(thread):
        print(thread)

    @client.event
    async def on_thread_join(thread):
        print(thread)

    @client.event
    async def on_thread_update(before, after):
        print(before, after)

    @client.event
    async def on_thread_remove(thread):
        print(thread)
    
    @client.event
    async def on_thread_delete(thread):
        print(thread)
    
    @client.event
    async def on_raw_thread_update(payload):
        print(payload)

    @client.event
    async def on_raw_thread_delete(payload):
        print(payload)

    @client.event
    async def on_thread_member_join(member):
        print(member)

    @client.event
    async def on_thread_member_remove(member):
        print(member)

    @client.event
    async def on_raw_thread_member_remove(payload):
        print(payload)

    # "Voice" イベント

    @client.event
    async def on_voice_state_update(member, before, after):
        print(member, before, after)
    client.run(token)
except Exception as e:
    print(e)
