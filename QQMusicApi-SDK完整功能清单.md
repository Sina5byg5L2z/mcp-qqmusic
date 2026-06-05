# QQMusicApi SDK 完整功能清单

> 基于 qqmusic-api-python v0.6.1，共 **10 个模块、82 个公开 API 方法**

---

## 模块总览

| 模块 | 方法数 | 当前 MCP 使用 | 未使用 |
|------|--------|--------------|--------|
| search | 5 | 1 (search_by_type) | 4 |
| song | 11 | 2 (get_detail, get_song_urls) | 9 |
| album | 2 | 2 | 0 |
| singer | 9 | 5 | 4 |
| songlist | 5 | 1 (get_detail) | 4 |
| lyric | 1 | 1 | 0 |
| recommend | 5 | 2 | 3 |
| top | 2 | 2 | 0 |
| mv | 2 | 2 | 0 |
| user | 12 | 0 | 12 |
| comment | 7 | 0 | 7 |
| login | 7 | 0 | 7 |
| private_message | 14 | 0 | 14 |

---

## 1. search — 搜索模块 (`client.search`)

### `get_hotkey()` → `dict`
获取热搜关键词列表。

### `complete(keyword: str)` → `dict`
搜索自动补全/联想词。

### `quick_search(keyword: str)` → `dict`
快速搜索，返回原始 JSON 数据（无模型解析）。

### `general_search(keyword: str, page=1, num=15, searchid=None, page_start=None, *, highlight=True)` → `GeneralSearchResponse`
综合搜索，跨所有内容类型，支持分页。

### `search_by_type(keyword: str, search_type=SearchType.SONG, num=10, page=1, searchid=None, *, highlight=True)` → `SearchByTypeResponse`
按类型搜索。`SearchType` 枚举：
- `SONG=0` / `SINGER=1` / `ALBUM=2` / `SONGLIST=3` / `MV=4`
- `LYRIC=7` / `USER=8` / `AUDIO_ALBUM=15` / `AUDIO=18`

---

## 2. song — 歌曲模块 (`client.song`)

### `get_detail(value: int | str)` → `GetSongDetailResponse`
获取单曲详情（ID 或 MID）。

### `get_song_urls(file_info: list[SongFileInfo], file_type=SongFileType.MP3_128)` → `GetSongUrlsResponse`
获取歌曲播放链接。支持音质：
- `MP3_128` / `MP3_320` / `FLAC`
- `OGG_640` / `OGG_320` / `OGG_192` / `OGG_96`
- `ACC_192` / `ACC_96` / `ACC_48`
- `MASTER` / `ATMOS_2` / `ATMOS_51` / `ATMOS_71` / `ATMOS_DB` / `DTS_X` / `NAC`

### `query_song(value: list[int] | list[str])` → `QuerySongResponse`
批量查询歌曲信息（ID 列表或 MID 列表，不可混用）。

### `get_similar_song(songid: int)` → `GetSimilarSongResponse`
获取相似歌曲推荐。

### `get_labels(songid: int)` → `GetSongLabelsResponse`
获取歌曲标签/分类元数据。

### `get_related_songlist(songid: int)` → `GetRelatedSonglistResponse`
获取包含此歌曲的歌单（支持分页刷新）。

### `get_related_mv(songid: int)` → `GetRelatedMvResponse`
获取与此歌曲相关的 MV（支持分页刷新）。

### `get_other_version(value: int | str)` → `GetOtherVersionResponse`
获取歌曲的其他版本/翻唱/改编。

### `get_producer(value: int | str)` → `GetProducerResponse`
获取歌曲制作人/创作团队信息（词曲编录等）。

### `get_sheet(mid: str)` → `GetSheetResponse`
获取歌曲乐谱。

### `get_fav_num(song_ids: list[int])` → `GetFavNumResponse`
批量获取歌曲收藏数量。

### `get_cdn_dispatch()` → `GetCdnDispatchResponse`
获取 CDN 分发信息（音频流地址）。

---

## 3. album — 专辑模块 (`client.album`)

### `get_detail(value: int | str)` → `GetAlbumDetailResponse`
获取专辑详情（ID 或 MID）。

### `get_song(value: int | str, num=10, page=1)` → `GetAlbumSongResponse`
获取专辑歌曲列表，支持分页。

---

## 4. singer — 歌手模块 (`client.singer`)

### `get_info(mid: str)` → `HomepageHeaderResponse`
获取歌手主页信息（需要 MID）。

### `get_desc(mids: list[str])` → `SingerDetailResponse`
批量获取歌手描述/简介。

### `get_tab_detail(mid: str, tab_type: TabType, page=1, num=10)` → `HomepageTabDetailResponse`
获取歌手主页标签页详情。`TabType` 枚举：
- `WIKI` — 百科简介
- `ALBUM` — 专辑列表
- `SONG` — 歌曲列表
- `COMPOSER` / `LYRICIST` / `PRODUCER` / `ARRANGER` / `MUSICIAN` — 创作身份作品
- `VIDEO` — 视频/MV 列表

### `get_songs_list(mid: str, num=10, page=1)` → `SingerSongListResponse`
获取歌手歌曲列表，支持分页。

### `get_album_list(mid: str, num=10, page=1)` → `SingerAlbumListResponse`
获取歌手专辑列表，支持分页。

### `get_mv_list(mid: str, num=10, page=1)` → `SingerMvListResponse`
获取歌手 MV 列表，支持分页。

### `get_similar(mid: str, number=10)` → `SimilarSingerResponse`
获取相似歌手推荐。

### `get_singer_list(area=AreaType.ALL, sex=SexType.ALL, genre=GenreType.ALL)` → `SingerTypeListResponse`
按地区/性别/流派筛选歌手列表。

筛选枚举：
- `AreaType`: `ALL` / `CHINA` / `TAIWAN` / `AMERICA` / `JAPAN` / `KOREA`
- `SexType`: `ALL` / `MALE` / `FEMALE` / `GROUP`
- `GenreType`: `ALL` / `POP` / `RAP` / `CHINESE_STYLE` / `ROCK` / `ELECTRONIC` / `FOLK` / `R_AND_B` / `JAZZ` / `CLASSICAL` 等

### `get_singer_list_index(area, sex, genre, index=IndexType.ALL, page=1, num=80)` → `SingerIndexPageResponse`
按首字母索引的歌手列表，支持多条件筛选。

---

## 5. songlist — 歌单模块 (`client.songlist`)

### `get_detail(songlist_id: int, dirid=0, num=10, page=1, *, onlysong=False, tag=True, userinfo=True)` → `GetSonglistDetailResponse`
获取歌单详情和歌曲列表，支持分页。

### `create(dirname: str)` → `CreateDeleteSonglistResp`
创建新歌单。需要登录。

### `delete(dirid: int)` → `CreateDeleteSonglistResp`
删除歌单。需要登录。

### `add_songs(dirid: int, song_info: list[tuple[int, int]])` → `bool`
向歌单添加歌曲。`song_info` 为 `(song_id, song_type)` 元组列表。需要登录。

### `del_songs(dirid: int, song_info: list[tuple[int, int]])` → `bool`
从歌单删除歌曲。需要登录。

---

## 6. lyric — 歌词模块 (`client.lyric`)

### `get_lyric(value: int | str, *, qrc=False, trans=False, roma=False)` → `GetLyricResponse`
获取歌词（ID 或 MID）。选项：
- `qrc` — 逐字歌词（QRC 格式）
- `trans` — 翻译歌词
- `roma` — 罗马音歌词

---

## 7. recommend — 推荐模块 (`client.recommend`)

### `get_recommend_newsong()` → `RecommendNewSongResponse`
获取推荐新歌。

### `get_recommend_songlist(page=1, num=25)` → `RecommendSonglistResponse`
获取推荐歌单，支持分页。

### `get_home_feed(page=1, direction=0, s_num=0, v_cache=None)` → `RecommendFeedCardResponse`
获取首页推荐信息流，支持续传分页。

### `get_guess_recommend()` → `GuessRecommendResponse`
获取"猜你喜欢"推荐。

### `get_radar_recommend(page=1)` → `RadarRecommendResponse`
获取雷达/发现推荐，支持分页。

---

## 8. top — 排行榜模块 (`client.top`)

### `get_category()` → `TopCategoryResponse`
获取所有排行榜分类。

### `get_detail(top_id: int, num=10, page=1, *, tag=True)` → `TopDetailResponse`
获取排行榜详情和歌曲列表，支持分页。

---

## 9. mv — MV模块 (`client.mv`)

### `get_detail(vids: list[str])` → `GetMvDetailResponse`
批量获取 MV 详情（VID 列表）。

### `get_mv_urls(vids: list[str])` → `GetMvUrlsResponse`
批量获取 MV 播放链接（VID 列表）。

---

## 10. user — 用户模块 (`client.user`) ⚠️ 全部未接入

### `get_homepage(euin: str)` → `UserHomepageResponse`
获取用户主页信息和统计数据。

### `get_vip_info()` → `UserVipInfoResponse`
获取当前登录账号的 VIP 会员信息。需要登录。

### `get_fav_song(euin: str, page=1, num=10)` → `GetSonglistDetailResponse`
获取用户收藏的歌曲，支持分页。

### `get_fav_album(euin: str, page=1, num=10)` → `UserFavAlbumResponse`
获取用户收藏的专辑，支持分页。

### `get_fav_mv(euin: str)` → `UserFavMvResponse`
获取用户收藏的 MV。需要登录。

### `get_fav_songlist(euin: str, page=1, num=10)` → `UserFavSonglistResponse`
获取用户收藏的歌单，支持分页。

### `get_follow_singers(euin: str, page=1, num=10)` → `UserRelationListResponse`
获取用户关注的歌手列表。需要登录。

### `get_follow_user(euin: str, page=1, num=10)` → `UserRelationListResponse`
获取用户关注的用户列表。需要登录。

### `get_fans(euin: str, page=1, num=10)` → `UserRelationListResponse`
获取用户的粉丝列表。需要登录。

### `get_friend(page=1, num=10)` → `UserFriendListResponse`
获取登录用户的好友列表。需要登录。

### `get_created_songlist(uin: int)` → `UserCreatedSonglistResponse`
获取用户创建的歌单。

### `get_music_gene(euin: str)` → `UserMusicGeneResponse`
获取用户的音乐基因/听歌偏好画像。

---

## 11. comment — 评论模块 (`client.comment`) ⚠️ 全部未接入

### `get_comment_count(biz_id: int)` → `CommentCountResponse`
获取歌曲评论数量。

### `get_hot_comments(biz_id: int, page_num=1, page_size=15)` → `CommentListResponse`
获取热门评论，支持分页。

### `get_new_comments(biz_id: int, page_num=1, page_size=15)` → `CommentListResponse`
获取最新评论，支持分页。

### `get_recommend_comments(biz_id: int, page_num=1, page_size=15)` → `CommentListResponse`
获取推荐评论，支持分页。

### `get_moment_comments(biz_id: int, page_size=15)` → `MomentCommentResponse`
获取歌曲时间节点评论（歌词对应时刻的评论），支持游标分页。

### `add_comment(biz_id: int, content: str, reply_cmt_id=None)` → `AddCommentResponse`
发表评论，可回复其他评论。需要登录。

### `delete_comment(cm_id: str)` → `bool`
删除评论。需要登录。

---

## 12. login — 登录模块 (`client.login`) ⚠️ 通过外部 login.py 使用

### `get_qrcode(login_type: QRLoginType)` → `QR`
生成登录二维码。`QRLoginType`: `QQ` / `WX`(微信) / `MOBILE`(手机App扫码)。

### `check_qrcode(qrcode: QR)` → `QRLoginResult`
轮询二维码扫码状态。

### `checking_mobile_qrcode(qrcode: QR)` → `QRLoginResult` (异步生成器)
流式监听手机 App 扫码登录事件。

### `send_authcode(phone, country_code=86)` → `PhoneAuthCodeResult`
发送短信验证码。

### `phone_authorize(phone, auth_code)` → `Credential`
手机验证码登录。

### `check_expired(credential=None)` → `bool`
检查凭证是否过期。

### `refresh_credential(credential=None)` → `Credential`
刷新过期凭证。

---

## 13. private_message — 私信模块 (`client.private_message`) ⚠️ 全部未接入

### `get_sessions(...)` → `PrivateSessionListResponse`
获取私信会话列表。

### `get_messages(session_id=..., user_id=..., ...)` → `PrivateMessageListResponse`
获取会话消息列表。

### `send_message(user_id, msg_type, ...)` → `PrivateSendMessageResponse`
发送私信。

### `delete_message(session_id, msg_id)` → `PrivateOperationResponse`
删除单条消息。

### `delete_session(session_id)` → `PrivateOperationResponse`
删除整个会话。

### `clear_session(session_id)` → `PrivateOperationResponse`
清空会话消息。

### `mark_all_messages_read(cmd_flag, encrypt_uin)` → `PrivateOperationResponse`
标记会话全部已读。

### `get_media_message_details(session_id, msg_ids)` → `PrivateMediaMessageDetailsResponse`
获取图片/视频消息详情和 URL。

### `get_musician_message_card(enc_uin)` → `PrivateMusicianCardResponse`
获取音乐人私信卡片。

### `get_chat_entries(scenes)` → `PrivateChatEntriesResponse`
获取聊天页功能入口。

### `get_safety_hint(enc_uin)` → `PrivateSafetyHintResponse`
获取私信安全/防诈骗提示。

### `get_friendship_badge(target_enc_uin)` → `dict`
获取好友互动徽章。

### `set_config(config_type, config_value)` → `PrivateOperationResponse`
设置私信配置。

### `get_config(config_type)` → `PrivateConfigResponse`
读取私信配置。

---

## Client 级别工具方法

### `client.gather(requests, batch_size=20)` → `list`
并发执行多个请求，自动批量合并兼容请求。

### `client.request(method, url, ...)` → `Response`
发送原始 HTTP 请求。

### `client.request_api(data, ...)` → `Response`
发送底层 QQ 音乐 API 请求。

---

## 当前 MCP Server 未使用的能力汇总

| 类别 | 未使用的方法 | 用途 |
|------|------------|------|
| 搜索联想 | `search.complete()`, `search.get_hotkey()` | 搜索建议、热搜榜 |
| 综合搜索 | `search.general_search()` | 跨类型一次性搜索 |
| 歌曲扩展 | `song.get_similar_song()`, `song.get_other_version()` | 相似歌曲、其他版本 |
| 歌曲元数据 | `song.get_producer()`, `song.get_labels()` | 制作团队、标签 |
| 歌曲关联 | `song.get_related_songlist()`, `song.get_related_mv()` | 关联歌单/MV |
| 歌曲统计 | `song.get_fav_num()` | 收藏数量 |
| 歌曲乐谱 | `song.get_sheet()` | 乐谱 |
| 歌手筛选 | `singer.get_singer_list()`, `singer.get_singer_list_index()` | 按条件浏览歌手 |
| 相似歌手 | `singer.get_similar()` | 相似歌手推荐 |
| 歌单管理 | `songlist.create/delete/add_songs/del_songs()` | 创建/编辑歌单 |
| 推荐扩展 | `recommend.get_home_feed()`, `recommend.get_guess_recommend()`, `recommend.get_radar_recommend()` | 首页信息流、猜你喜欢、雷达推荐 |
| 用户信息 | `user.*` (12 个方法) | VIP信息、收藏、关注、粉丝、音乐基因 |
| 评论 | `comment.*` (7 个方法) | 热门/最新/推荐评论、时间节点评论、发评论 |
| 私信 | `private_message.*` (14 个方法) | 私信会话、消息收发 |
| 高级音质 | `SongFileType` 中的 `MASTER`/`ATMOS`/`DTS_X` 等 | 臻品音质 |
