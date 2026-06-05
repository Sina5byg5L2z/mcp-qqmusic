"""响应格式化 - 紧凑文本输出，节省 LLM 上下文."""

from __future__ import annotations

import re
from typing import Any


def _strip_html(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", str(text))


def _singer_names(singers: list[Any] | None) -> str:
    if not singers:
        return "未知"
    return "/".join(getattr(s, "name", str(s)) or "未知" for s in singers)


def _duration(seconds: int | float | None) -> str:
    if not seconds:
        return ""
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


def _song_line(song: Any, idx: int | None = None) -> str:
    name = _strip_html(getattr(song, "name", None) or getattr(song, "title", None)) or "未知"
    singer = _singer_names(getattr(song, "singer", None))
    album = _strip_html(getattr(getattr(song, "album", None), "name", None)) or "未知"
    dur = _duration(getattr(song, "interval", None))
    prefix = f"{idx}. " if idx else ""
    return f"{prefix}{name} | {singer} | {album}{f' | {dur}' if dur else ''}"


def fmt_songs(songs: list[Any]) -> str:
    if not songs:
        return "无结果"
    return "\n".join(_song_line(s, i + 1) for i, s in enumerate(songs))


def fmt_song_detail(track: Any) -> str:
    if not track:
        return "未找到歌曲"
    lines = [
        f"歌曲: {getattr(track, 'name', '未知')}",
        f"MID: {getattr(track, 'mid', '未知')}",
        f"ID: {getattr(track, 'id', '未知')}",
        f"歌手: {_singer_names(getattr(track, 'singer', None))}",
        f"专辑: {getattr(getattr(track, 'album', None), 'name', None) or '未知'}",
    ]
    interval = getattr(track, "interval", None)
    if interval:
        lines.append(f"时长: {_duration(interval)}")
    pub = getattr(getattr(track, "album", None), "time_public", None)
    if pub:
        lines.append(f"发行: {pub}")
    return "\n".join(lines)


def fmt_album_detail(detail: Any, songs: list[Any] | None = None) -> str:
    if not detail:
        return "未找到专辑"
    album = getattr(detail, "album", detail)
    lines = [
        f"专辑: {getattr(album, 'name', '未知')}",
        f"MID: {getattr(album, 'mid', '未知')}",
        f"歌手: {_singer_names(getattr(detail, 'singer', None) or getattr(album, 'singer', None))}",
    ]
    pub = getattr(album, "time_public", None) or getattr(detail, "pub_time", None)
    if pub:
        lines.append(f"发行: {pub}")
    total = getattr(album, "total", None) or getattr(detail, "total", None)
    if total:
        lines.append(f"曲目数: {total}")
    desc = getattr(detail, "desc", None) or getattr(album, "desc", None)
    if desc:
        lines.append(f"简介: {desc[:200]}")
    if songs:
        lines += ["", "--- 歌曲列表 ---", fmt_songs(songs)]
    return "\n".join(lines)


def fmt_singer_info(info: Any, desc: Any = None) -> str:
    if not info:
        return "未找到歌手"
    singer = getattr(info, "singer", info)
    lines = [
        f"歌手: {getattr(singer, 'name', '未知')}",
        f"MID: {getattr(singer, 'mid', '未知')}",
    ]
    # base_info may be HomepageBaseInfo with name/avatar
    base = getattr(info, "base_info", None)
    if base:
        bname = getattr(base, "name", None)
        if bname:
            lines.append(f"昵称: {bname}")
    # desc: singer_list[0].ex_info or singer_desc list
    ex = None
    if desc:
        sl = getattr(desc, "singer_list", None)
        if sl and len(sl) > 0:
            ex = getattr(sl[0], "ex_info", None)
        if not ex:
            # Try alternate: list of singer desc items
            items = getattr(desc, "singer_desc", None) or (desc if isinstance(desc, list) else None)
            if items and len(items) > 0:
                ex = items[0] if isinstance(items[0], object) else None
    if ex:
        for field, label in [("area", "地区"), ("genre", "流派"), ("birthday", "生日")]:
            val = getattr(ex, field, None)
            if val:
                lines.append(f"{label}: {val}")
        d = getattr(ex, "desc", None) or getattr(ex, "简介", None)
        if d:
            lines.append(f"简介: {d[:300]}")
    return "\n".join(lines)


def fmt_songlist_detail(detail: Any) -> str:
    if not detail:
        return "未找到歌单"
    info = getattr(detail, "info", None) or detail
    title = (getattr(info, "title", None) or getattr(info, "dirname", None)
             or getattr(info, "dissname", None) or "未知")
    tid = getattr(info, "id", None) or getattr(info, "dirid", None) or "未知"
    lines = [
        f"歌单: {title}",
        f"ID: {tid}",
    ]
    num = getattr(info, "songnum", None) or getattr(detail, "total", None)
    if num:
        lines.append(f"歌曲数: {num}")
    listennum = getattr(info, "listennum", None)
    if listennum:
        lines.append(f"播放量: {listennum}")
    creator = getattr(info, "creator", None)
    if creator:
        cname = getattr(creator, "name", None) or getattr(creator, "nickname", None)
        if cname:
            lines.append(f"创建者: {cname}")
    desc = getattr(info, "desc", None)
    if desc:
        lines.append(f"简介: {desc[:200]}")
    songs = getattr(detail, "songs", None) or getattr(detail, "songlist", None)
    if songs:
        lines += ["", "--- 歌曲列表 ---", fmt_songs(songs)]
    return "\n".join(lines)


def fmt_top_detail(detail: Any) -> str:
    if not detail:
        return "未找到排行榜"
    info = getattr(detail, "info", None) or detail
    name = (getattr(info, "name", None) or getattr(info, "title", None)
            or getattr(detail, "title", None) or "未知")
    lines = [f"排行榜: {name}"]
    period = getattr(info, "period", None) or getattr(detail, "update", None)
    if period:
        lines.append(f"更新: {period}")
    listen = getattr(info, "listen_num", None) or getattr(detail, "listenNum", None)
    if listen:
        lines.append(f"播放量: {listen}")
    total = getattr(info, "total_num", None)
    if total:
        lines.append(f"歌曲数: {total}")
    intro = getattr(info, "intro", None)
    if intro:
        lines.append(f"简介: {intro[:200]}")
    songs = getattr(detail, "songs", None) or getattr(info, "songs", None) or getattr(detail, "song", None)
    if songs:
        lines += ["", "--- 歌曲列表 ---", fmt_songs(songs)]
    return "\n".join(lines)


def fmt_top_category(cats: Any) -> str:
    if not cats:
        return "无数据"
    if isinstance(cats, list):
        lines = []
        for g in cats:
            items = getattr(g, "toplist", None) or (g if isinstance(g, list) else [g])
            for t in items:
                tid = getattr(t, "topId", None) or getattr(t, "id", "?")
                title = getattr(t, "title", None) or getattr(t, "label", "未知")
                lines.append(f"{tid}: {title}")
        return "\n".join(lines)
    return str(cats)[:500]


def fmt_lyric(data: Any) -> str:
    if not data:
        return "未找到歌词"
    raw = getattr(data, "lyric", "") or ""
    if not raw:
        return "无歌词"

    def _strip_ts(text: str) -> str:
        lines = []
        for line in text.split("\n"):
            # [mm:ss.xx]content → content
            parts = line.split("]", 1)
            lines.append(parts[-1].strip() if len(parts) > 1 else line.strip())
        return "\n".join(l for l in lines if l)

    parts = [_strip_ts(raw)]
    trans = getattr(data, "trans", None)
    if trans:
        t = _strip_ts(trans)
        if t:
            parts += ["", "--- 翻译 ---", t]
    roma = getattr(data, "roma", None)
    if roma:
        r = _strip_ts(roma)
        if r:
            parts += ["", "--- 罗马音 ---", r]
    return "\n".join(parts)


def fmt_song_urls(data: Any) -> str:
    if not data:
        return "未获取到播放链接"
    items = getattr(data, "data", None) or (data if isinstance(data, list) else [data])
    if not items:
        return "未获取到播放链接"
    lines = []
    for item in items:
        purl = getattr(item, "purl", None)
        mid = getattr(item, "mid", "未知")
        if not purl:
            lines.append(f"{mid}: 无法获取链接 (可能需要VIP)")
            continue
        url = purl if purl.startswith("http") else f"https://dl.stream.qqmusic.qq.com/{purl}"
        vkey = getattr(item, "vkey", None)
        if vkey:
            url = f"{url}?vkey={vkey}"
        lines.append(url)
    return "\n".join(lines)


def fmt_recommend(data: Any, rtype: str) -> str:
    if not data:
        return "无推荐数据"
    if rtype == "song":
        songs = getattr(data, "songs", None)
        if songs:
            return fmt_songs(songs)
    if rtype == "songlist":
        items = getattr(data, "songlists", None)
        if items:
            lines = []
            for i, s in enumerate(items):
                title = _strip_html(getattr(s, "title", None) or getattr(s, "dissname", "")) or "未知"
                creator = (getattr(getattr(s, "creator", None), "name", None)
                          or getattr(s, "creator_nick", None) or getattr(s, "nickname", ""))
                num = getattr(s, "songnum", None) or getattr(s, "total", "")
                lines.append(f"{i+1}. {title} | {creator}{f' | {num}首' if num else ''}")
            return "\n".join(lines)
    return str(data)[:500]
