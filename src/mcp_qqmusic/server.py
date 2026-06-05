"""MCP QQ Music Server - 直接调用 qqmusic_api SDK."""

from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from mcp.server.fastmcp import FastMCP
from qqmusic_api import Client, Credential
from qqmusic_api.modules.search import SearchType
from qqmusic_api.modules.singer import TabType
from qqmusic_api.modules.song import SongFileInfo, SongFileType

from .format import (
    fmt_album_detail,
    fmt_lyric,
    fmt_mv_detail,
    fmt_recommend,
    fmt_singer_info,
    fmt_song_detail,
    fmt_song_urls,
    fmt_songlist_detail,
    fmt_songs,
    fmt_top_category,
    fmt_top_detail,
)

# ── 配置 ──────────────────────────────────────────────

SEARCH_TYPE_MAP = {
    "song": SearchType.SONG,
    "singer": SearchType.SINGER,
    "album": SearchType.ALBUM,
    "songlist": SearchType.SONGLIST,
    "mv": SearchType.MV,
}

QUALITY_MAP = {
    "standard": SongFileType.MP3_128,
    "high": SongFileType.MP3_320,
    "lossless": SongFileType.FLAC,
}


# ── 生命周期 ──────────────────────────────────────────

@dataclass
class AppState:
    client: Client              # 无凭证，公开接口
    auth_client: Client | None  # 有凭证，需登录接口


@asynccontextmanager
async def lifespan(server: FastMCP):
    """管理 Client 生命周期：启动时创建，关闭时清理."""
    cred_path = os.path.join(os.getcwd(), "credential.json")

    credential = None
    if os.path.exists(cred_path):
        with open(cred_path, encoding="utf-8") as f:
            credential = Credential.model_validate(json.load(f))

    client = Client()  # 无凭证，公开请求不携带登录信息
    auth_client = Client(credential=credential) if credential else None
    try:
        yield AppState(client=client, auth_client=auth_client)
    finally:
        await client.close()
        if auth_client:
            await auth_client.close()


# ── MCP Server ────────────────────────────────────────

mcp = FastMCP(
    name="qqmusic",
    instructions="QQ音乐 MCP 服务。可搜索歌曲/歌手/专辑/歌单，查看详情、获取歌词和播放链接。",
    lifespan=lifespan,
)


def _get_client() -> Client:
    """从 lifespan context 获取无凭证 Client."""
    ctx = mcp.get_context()
    state: AppState = ctx.request_context.lifespan_context
    return state.client


def _get_auth_client() -> Client:
    """从 lifespan context 获取有凭证 Client，未登录时抛异常."""
    ctx = mcp.get_context()
    state: AppState = ctx.request_context.lifespan_context
    if not state.auth_client:
        raise RuntimeError("未登录，请先运行 login.py 获取凭证")
    return state.auth_client


def _err(e: Exception) -> str:
    return f"错误: {type(e).__name__}: {e}"


# ── Tools ─────────────────────────────────────────────

@mcp.tool()
async def search(
    keyword: str,
    type: str = "song",
    page: int = 1,
    size: int = 15,
) -> str:
    """搜索QQ音乐。

    Args:
        keyword: 搜索关键词
        type: 搜索类型 - song(歌曲), singer(歌手), album(专辑), songlist(歌单), mv(MV)
        page: 页码
        size: 每页数量(1-50)
    """
    try:
        client = _get_client()
        stype = SEARCH_TYPE_MAP.get(type, SearchType.SONG)
        req = client.search.search_by_type(keyword, search_type=stype, num=min(size, 50), page=page, highlight=False)
        data = await req
        # 根据类型取对应列表
        items = getattr(data, type, None) or getattr(data, "song", None) or []
        total = getattr(data, "total_num", 0) or getattr(data, "estimate_sum", 0)
        has_more = getattr(data, "nextpage", 0) and data.nextpage > 0
        result = fmt_songs(items)
        meta = f"共 {total} 条结果{' (还有更多)' if has_more else ''}"
        return f"{meta}\n{result}"
    except Exception as e:
        return _err(e)


@mcp.tool()
async def detail(
    type: str,
    id: str,
    page: int = 1,
    size: int = 20,
) -> str:
    """查看资源详情。

    Args:
        type: 资源类型 - song(歌曲), album(专辑), singer(歌手), songlist(歌单), top(排行榜)
        id: 资源ID或MID
        page: 页码(歌单/排行榜翻页用)
        size: 每页数量
    """
    try:
        client = _get_client()
        if type == "song":
            data = await client.song.get_detail(id)
            return fmt_song_detail(getattr(data, "track", data))

        if type == "album":
            ac = _get_auth_client()
            detail_data = await ac.album.get_detail(id)
            songs_data = await ac.album.get_song(id, num=size, page=page)
            songs = getattr(songs_data, "song_list", None) or []
            return fmt_album_detail(detail_data, songs)

        if type == "singer":
            try:
                info = await client.singer.get_info(id)
            except Exception:
                info = None
            try:
                desc = await client.singer.get_desc([id])
            except Exception:
                desc = None
            # 获取歌手百科简介
            wiki_intro = ""
            try:
                wiki = await client.singer.get_tab_detail(id, TabType.WIKI, num=10)
                intro_tabs = getattr(wiki, "introduction_tab", None) or []
                if intro_tabs:
                    singer_info_list = intro_tabs[0].get("SingerInfoList") or []
                    if singer_info_list:
                        wiki_intro = singer_info_list[0].get("Content", "")
            except Exception:
                pass
            try:
                songs_data = await client.singer.get_songs_list(id, num=size)
                songs = getattr(songs_data, "song_list", None) or songs_data if isinstance(songs_data, list) else None
            except Exception:
                songs = None
            try:
                albums_data = await client.singer.get_album_list(id, num=size)
                albums = getattr(albums_data, "album_list", None) or albums_data if isinstance(albums_data, list) else None
            except Exception:
                albums = None
            return fmt_singer_info(info, desc, songs=songs, albums=albums, wiki=wiki_intro)

        if type == "songlist":
            ac = _get_auth_client()
            data = await ac.songlist.get_detail(songlist_id=int(id), num=size, page=page)
            return fmt_songlist_detail(data)

        if type == "top":
            data = await client.top.get_detail(top_id=int(id), num=size, page=page)
            return fmt_top_detail(data)

        return f"未知类型: {type}"
    except Exception as e:
        return _err(e)


@mcp.tool()
async def lyric(
    id: str,
    trans: bool = False,
    roma: bool = False,
) -> str:
    """获取歌曲歌词。

    Args:
        id: 歌曲ID或MID
        trans: 是否返回翻译歌词
        roma: 是否返回罗马音
    """
    try:
        client = _get_client()
        data = await client.lyric.get_lyric(id, trans=trans, roma=roma)
        return fmt_lyric(data.decrypt())
    except Exception as e:
        return _err(e)


@mcp.tool()
async def url(
    mid: str,
    quality: str = "high",
) -> str:
    """获取歌曲播放链接⚠️。

    Args:
        mid: 歌曲MID
        quality: 音质 - standard(128k), high(320k), lossless(FLAC)
    """
    try:
        client = _get_auth_client()
        ftype = QUALITY_MAP.get(quality, SongFileType.MP3_320)
        data = await client.song.get_song_urls(
            file_info=[SongFileInfo(mid=mid)],
            file_type=ftype,
        )
        return fmt_song_urls(data)
    except Exception as e:
        return _err(e)


@mcp.tool()
async def recommend(
    type: str = "song",
) -> str:
    """获取QQ音乐推荐内容。

    Args:
        type: 推荐类型 - song(推荐新歌), songlist(推荐歌单)
    """
    try:
        client = _get_client()
        if type == "song":
            data = await client.recommend.get_recommend_newsong()
        elif type == "songlist":
            data = await client.recommend.get_recommend_songlist()
        else:
            return f"未知推荐类型: {type}"
        return fmt_recommend(data, type)
    except Exception as e:
        return _err(e)


@mcp.tool()
async def mv(
    vid: str,
) -> str:
    """获取MV详情和播放链接。

    Args:
        vid: MV的VID（搜索结果中的MV:xxx）
    """
    try:
        client = _get_client()
        detail = await client.mv.get_detail([vid])
        urls = await client.mv.get_mv_urls([vid])
        return fmt_mv_detail(detail, urls)
    except Exception as e:
        return _err(e)


# ── 入口 ──────────────────────────────────────────────

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
