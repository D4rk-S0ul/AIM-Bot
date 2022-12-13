from Config import servers, ping_role_ids


def get_server(ctx_or_thread):
    return servers.get(ctx_or_thread.guild.id)

def get_ping_role(server, ctx_or_thread):
    ping_role_id = ping_role_ids.get(server)
    return ctx_or_thread.guild.get_role(ping_role_id)