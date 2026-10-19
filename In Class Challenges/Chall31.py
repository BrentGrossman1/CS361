import struct
import zlib
import json
import time
import hmac
import hashlib

# magic numbers
MAGIC = 0xCAFE
SUPPORTED_VERSIONS = (3, 4)
LATEST_VERSION = 4
HEADER_SIZE = 12

FLAG_COMPRESSED = 0x01
FLAG_SIGNED = 0x02

MSG_LOGIN = 0x0001
MSG_MOVE = 0x0002
MSG_CHAT = 0x0003
MSG_LOGIN_REPLY = 0x8001
MSG_POSITION_CORRECTION = 0x8002
MSG_VERSION_ERROR = 0xFFFF

MAX_CHAT_LENGTH = 256
SPEED_TOLERANCE = 1.1


def header_is_valid(magic, version, seq, conn):
    if magic != MAGIC:
        conn.close()
        return False
    if version not in SUPPORTED_VERSIONS:
        conn.send(struct.pack(">HBBH", MAGIC, LATEST_VERSION, 0, MSG_VERSION_ERROR))
        return False
    if seq <= conn.last_seq:
        return False
    conn.last_seq = seq
    return True


def checksum_is_valid(body, trailer):
    # ones-complement 16-bit checksum
    total = 0
    for i in range(0, len(body) - 1, 2):
        total += (body[i] << 8) | body[i + 1]
    if len(body) % 2:
        total += body[-1] << 8
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total & 0xFFFF) == struct.unpack(">H", trailer[:2])[0]


def signature_is_valid(body, trailer, session_key):
    sig = trailer[2:34]
    expected = hmac.new(session_key, body, hashlib.sha256).digest()
    return hmac.compare_digest(sig, expected)


def login(conn, body, server, version):
    name_len = body[0]
    username = body[1:1 + name_len].decode("utf-8")
    token = body[1 + name_len:1 + name_len + 32].hex()
    row = server.db.execute(
        "SELECT id, banned, last_seen FROM players WHERE username = ? AND token = ?",
        (username, token),
    ).fetchone()
    if row is None or row[1]:
        conn.send(struct.pack(">HBBHB", MAGIC, version, 0, MSG_LOGIN_REPLY, 0))
        return
    player = server.world.spawn_player(row[0], username)
    conn.player = player
    server.db.execute("UPDATE players SET last_seen = ? WHERE id = ?", (int(time.time()), row[0]))
    server.db.commit()
    server.broadcast_system_message(f"{username} has joined the game")
    conn.send(struct.pack(">HBBHBI", MAGIC, version, 0, MSG_LOGIN_REPLY, 1, player.entity_id))


def move_player(conn, body, server, version):
    if conn.player is None:
        return
    x, y, z = struct.unpack(">fff", body[:12])
    packed_rot = struct.unpack(">H", body[12:14])[0]
    yaw = ((packed_rot >> 8) & 0xFF) * (360.0 / 256)
    pitch = (packed_rot & 0xFF) * (180.0 / 256) - 90.0
    dx, dy, dz = x - conn.player.x, y - conn.player.y, z - conn.player.z
    elapsed = time.time() - conn.player.last_move_time
    if (dx * dx + dy * dy + dz * dz) ** 0.5 > conn.player.max_speed * elapsed * SPEED_TOLERANCE:
        server.anticheat.flag(conn.player, "speed")
        conn.send(struct.pack(">HBBHfff", MAGIC, version, 0, MSG_POSITION_CORRECTION,
                              conn.player.x, conn.player.y, conn.player.z))
        return
    conn.player.last_move_time = time.time()
    server.world.move_entity(conn.player, x, y, z, yaw, pitch)


def send_chat(conn, body, server):
    if conn.player is None:
        return
    msg = json.loads(body.decode("utf-8"))
    text = msg.get("text", "")[:MAX_CHAT_LENGTH]
    text = "".join(c for c in text if c.isprintable())
    for word in server.config["banned_words"]:
        text = text.replace(word, "*" * len(word))
    if msg.get("channel") == "team":
        server.chat.send_to_team(conn.player.team, conn.player.name, text)
    else:
        server.chat.broadcast(conn.player.name, text)


def handle_packet(data, conn, server):
    if len(data) < HEADER_SIZE:
        server.logger.warning("short packet from %s", conn.addr)
        return

    magic, version, flags, msg_type, seq, payload_len = struct.unpack(">HBBHIH", data[:HEADER_SIZE])

    if not header_is_valid(magic, version, seq, conn):
        return

    body = data[HEADER_SIZE:HEADER_SIZE + payload_len]
    trailer = data[HEADER_SIZE + payload_len:]

    if not checksum_is_valid(body, trailer):
        server.metrics.increment("packets.bad_checksum")
        return

    if flags & FLAG_COMPRESSED:
        body = zlib.decompress(body)

    if flags & FLAG_SIGNED and not signature_is_valid(body, trailer, conn.session_key):
        server.ban_list.add(conn.addr[0])
        conn.close()
        return

    if msg_type == MSG_LOGIN:
        login(conn, body, server, version)
    elif msg_type == MSG_MOVE:
        move_player(conn, body, server, version)
    elif msg_type == MSG_CHAT:
        send_chat(conn, body, server)
    else:
        server.logger.info("unknown msg_type 0x%04x from %s", msg_type, conn.addr)