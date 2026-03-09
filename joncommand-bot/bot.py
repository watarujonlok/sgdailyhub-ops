#!/usr/bin/env python3
import json, os, time, urllib.parse, urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
OWNER = os.environ.get("ALLOW_USER_ID", "212307908").strip()
API = f"https://api.telegram.org/bot{TOKEN}"
VPN_BASE = os.environ.get("VPN_BASE", "http://127.0.0.1:8111")
STATE_FILE = "/tmp/state.json"
ARRIVAL_URL = "https://arrivelah2.busrouter.sg/"

if not TOKEN:
    raise SystemExit("BOT_TOKEN missing")

state = {"users": {}}


def load_state():
    global state
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception:
        state = {"users": {}}


def save_state():
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_FILE)


def user(uid):
    return state["users"].setdefault(str(uid), {"last_chat_id": None})


def tg(method, payload=None, timeout=30):
    data = urllib.parse.urlencode(payload).encode() if payload is not None else None
    req = urllib.request.Request(f"{API}/{method}", data=data)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def send(chat_id, text, reply_to=None):
    payload = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    try:
        tg("sendMessage", payload, timeout=20)
    except Exception:
        pass


def arrivals(stop_id, svc=None, limit=8):
    u = ARRIVAL_URL + "?id=" + urllib.parse.quote(str(stop_id))
    with urllib.request.urlopen(u, timeout=20) as r:
        d = json.loads(r.read().decode())
    svcs = d.get("services") or []
    out = []
    for s in svcs:
        no = str(s.get("no") or s.get("service") or s.get("ServiceNo") or "")
        if svc and no != svc:
            continue
        eta_txt = "NA"
        for key in ("next", "nextBus", "next2", "next3"):
            v = s.get(key)
            if isinstance(v, dict):
                t = v.get("time") or v.get("eta")
                if t:
                    try:
                        dt = datetime.fromisoformat(str(t).replace("Z", "+00:00"))
                        mins = max(int((dt - datetime.now(timezone.utc)).total_seconds() // 60), 0)
                        eta_txt = f"{mins}m"
                    except Exception:
                        pass
                    break
        out.append((9999 if eta_txt == "NA" else int(eta_txt[:-1]), f"{no}: {eta_txt}"))
    out.sort(key=lambda x: x[0])
    return [x[1] for x in out[:limit]] or ["No arrival data."]


def vpn_get(path):
    with urllib.request.urlopen(VPN_BASE + path, timeout=15) as r:
        return json.loads(r.read().decode())


def vpn_post(path):
    req = urllib.request.Request(VPN_BASE + path, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def resolve_rid(raw):
    rid = raw
    if rid.isdigit():
        d0 = vpn_get("/api/vpn/requests")
        pending = d0.get("pending", [])
        idx = int(rid)
        if idx < 1 or idx > len(pending):
            return None, f"Invalid index: {idx}. Use /vpnlist first."
        rid = pending[idx - 1].get("id") or ""
        if not rid:
            return None, "Could not resolve request id from index."
    return rid, None


def help_text():
    return (
        "Commands:\n"
        "Bus:\n"
        "/bus <StopCode> [ServiceNo]\n\n"
        "VPN:\n"
        "/vpnlist\n"
        "/vpnapprove <id|index>\n"
        "/vpnreject <id|index>\n"
        "/vpnstatus <id>\n"
        "/vpnfix <id|index>"
    )


def handle_text(chat_id, uid, mid, text):
    if str(uid) != OWNER:
        return send(chat_id, "Unauthorized.", mid)

    t = (text or "").strip()
    if not t:
        return
    cmd, *rest = t.split()
    cmd = cmd.lower().split("@", 1)[0]

    u = user(uid)
    u["last_chat_id"] = chat_id
    save_state()

    try:
        if cmd in ("/start", "/bushelp"):
            return send(chat_id, help_text(), mid)

        if cmd == "/bus":
            if not rest:
                return send(chat_id, "Usage: /bus <StopCode> [ServiceNo]", mid)
            stop = rest[0]
            svc = rest[1] if len(rest) > 1 else None
            ts = datetime.now().astimezone().strftime("%H:%M:%S")
            return send(chat_id, f"Stop {stop} (as at {ts})\n" + "\n".join(arrivals(stop, svc, 8)), mid)

        if cmd == "/vpnlist":
            d = vpn_get("/api/vpn/requests")
            c, p = d.get("counts", {}), d.get("pending", [])
            lines = [f"VPN pending: {c.get('pending', len(p))}"]
            for i, r in enumerate(p[:20], 1):
                lines.append(f"{i}. {r.get('id','-')} • {r.get('name','-')} • {r.get('contact','-')} • {r.get('reason','-')}")
            if not p:
                lines.append("No pending requests.")
            return send(chat_id, "\n".join(lines), mid)

        if cmd == "/vpnstatus":
            if not rest:
                return send(chat_id, "Usage: /vpnstatus <request_id>", mid)
            rid = rest[0]
            d = vpn_get(f"/api/vpn/status/{urllib.parse.quote(rid)}")
            lines = [f"id: {rid}", f"status: {d.get('status','unknown')}"]
            if d.get("download_url"):
                lines.append(f"download: {d['download_url']}")
                if d.get("expires"):
                    lines.append(f"expires: {d['expires']}")
            return send(chat_id, "\n".join(lines), mid)

        if cmd in ("/vpnapprove", "/vpnreject"):
            if not rest:
                return send(chat_id, f"Usage: {cmd} <request_id|index>", mid)
            rid, err = resolve_rid(rest[0])
            if err:
                return send(chat_id, err, mid)
            act = "approve" if cmd == "/vpnapprove" else "reject"
            d = vpn_post(f"/api/vpn/{act}/{urllib.parse.quote(rid)}")
            if not d.get("ok"):
                return send(chat_id, f"failed: {d}", mid)

            if act == "approve":
                for _ in range(90):
                    st = vpn_get(f"/api/vpn/status/{urllib.parse.quote(rid)}")
                    if st.get("download_url"):
                        try:
                            vpn_post(f"/api/vpn/email-ready/{urllib.parse.quote(rid)}")
                        except Exception:
                            pass
                        return send(chat_id, f"approved+ready: {rid}\n{st.get('download_url')}", mid)
                    time.sleep(1)
                return send(chat_id, f"approved: {rid}\nProvision queued. Use /vpnfix {rid} if needed.", mid)

            return send(chat_id, f"{act}d: {rid}", mid)

        if cmd == "/vpnfix":
            if not rest:
                return send(chat_id, "Usage: /vpnfix <request_id|index>", mid)
            rid, err = resolve_rid(rest[0])
            if err:
                return send(chat_id, err, mid)
            # Worker runs every minute; poll for up to 75s and re-send ready email when link exists.
            for _ in range(75):
                st = vpn_get(f"/api/vpn/status/{urllib.parse.quote(rid)}")
                if st.get("download_url"):
                    try:
                        vpn_post(f"/api/vpn/email-ready/{urllib.parse.quote(rid)}")
                    except Exception:
                        pass
                    return send(chat_id, f"vpnfix done: {rid}\n{st.get('download_url')}", mid)
                time.sleep(1)
            return send(chat_id, f"vpnfix queued: {rid}. Try /vpnstatus {rid} in 1 minute.", mid)

        if cmd.startswith("/"):
            return send(chat_id, "Unknown command. Use /bushelp", mid)
    except Exception as e:
        return send(chat_id, f"error: {e}", mid)


def main():
    load_state()
    offset = 0
    while True:
        try:
            r = tg("getUpdates", {"timeout": 50, "offset": offset}, timeout=60)
            for upd in r.get("result", []):
                offset = upd["update_id"] + 1
                m = upd.get("message") or upd.get("edited_message")
                if not m:
                    continue
                chat = m.get("chat", {}).get("id")
                uid = m.get("from", {}).get("id")
                mid = m.get("message_id")
                txt = m.get("text")
                if txt:
                    handle_text(chat, uid, mid, txt)
        except Exception:
            time.sleep(2)


if __name__ == "__main__":
    main()
