# -*- coding: utf-8 -*-
import json
import subprocess

# import pyperclip
import yt_dlp


class VideoDL:
    """这是一个用来下载网络视频的类
    cookies:用电脑里的火狐的目录,加了以后就能下载b站的视频了,火狐老工具人了!!!
    默认是下载并嵌入封面的,如果不想的话,请把self.option['writethumbnail'] = True注释掉

    查看可供下载的字幕


    """

    def __init__(self, *video_url):
        self.option = {'cookiesfrombrowser': ('firefox',
                                              'C:\\Users\\98357\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\mj3ny6p9.default-release',
                                              None,
                                              None)}
        if video_url == ():
            self.video_url = None
        else:
            self.video_url = video_url[0]

        self.option['outtmpl'] = "%(title)s.%(ext)s"
        # 下载封面
        # 这里产生一个重大bug的原因竟然是因为我把赋值的语句的=号写成了:号
        self.option['writethumbnail'] = True
        self.option['postprocessors'] = [{'already_have_thumbnail': True, 'key': 'EmbedThumbnail'}]

    def set_format(self, format):
        """
        你应该使用这样的格式(在使用的时候注意不能只写视频的这一边,否则没有声音):
        bestvideo[height = 720]+bestaudio / best[height = 720]
        最好的音频:140,m4a\
        视频格式设置:
        bestvideo[height=720,ext=mp4]
        bestaudio[ext=m4a]
        """
        self.option['format'] = format
        return self

    def set_name(self, name):
        self.option['outtmpl'] = name
        return self

    def set_url(self, url):
        self.video_url = url
        return self

    # 判断是否要跳过视频

    def do_convert_to_mp4(self):
        self.option['postprocessors'].append({
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        })

    def is_skip_download(self, is_jump):
        self.option['skip_download'] = is_jump
        return self

    def is_embed_subtitles(self, is_wirte):
        ##请配合下载字幕使用
        self.option['postprocessors'].append({'already_have_subtitle': False,
                                              'key': 'FFmpegEmbedSubtitle'})
        return self

    # 判断是否要跳过视频设置是否要下载字幕并且设定语言(第一个值是用flag)
    def is_write_subtitles(self, write_subtitles, *lang):
        self.option['writesubtitles'] = write_subtitles
        self.option['subtitleslangs'] = list(lang)
        return self

    def is_write_automaticsub(self, write_subtitles, *lang):
        self.option['writeautomaticsub'] = write_subtitles
        self.option['subtitleslangs'] = list(lang)
        return self

    def start_download(self):
        ydl = yt_dlp.YoutubeDL(self.option)
        ydl.extract_info(self.video_url, download=True)

    def get_video_info(self):
        if 'bilibili' in self.video_url:
            cookiepath = r'C:\Users\98357\AppData\Roaming\Mozilla\Firefox\Profiles\mj3ny6p9.default-release'

            command = f'yt-dlp --cookies-from-browser firefox:"{cookiepath}" -F {self.video_url}'
            # print("请自己用管理权限的cmd窗口输入")
            # print(command)
            # pyperclip.copy(command)
            # print("命令已复制到剪切板")
            subprocess.run('start cmd /k ' + command + ' && pause', shell=True)
        else:
            command = f'yt-dlp  -F {self.video_url}'
            subprocess.run('echo ' + command, shell=True)
            subprocess.run('start cmd /k ' + command + ' && pause', shell=True)

    def get_subtitles_info(self):
        ydl = yt_dlp.YoutubeDL(self.option)
        info_dict = ydl.extract_info(self.video_url, download=False)
        subtitles = info_dict.get('subtitles', {})
        # 打印字幕信息
        for lang, subs in subtitles.items():
            print(f"Language: {lang}, Subtitles available: {len(subs)}")


class AudioDL(VideoDL):
    def __init__(self, *video_url):
        super().__init__(*video_url)
        # 设定下载的音频会变为mp3,下载的字幕会变为lrc格式
        ## 用了下面的这个设定以后发现好像会自动下载视频,所以重写了
        self.option['postprocessors'] = [
            # 音频转化为mp3:
            {
                'key': 'FFmpegExtractAudio',  # 使用正确的键
                'preferredcodec': 'mp3',  # 选择音频格式，可以是 'best', 'aac', 'mp3', 等等
                'preferredquality': '192',
            },
            # 字幕转化为lrc:
            {'key': 'FFmpegSubtitlesConvertor',
             'format': 'lrc'},
        ]
        # 设定音频的命名格式
        self.option['outtmpl'] = "%(title)s.%(ext)s"
        self.option['format'] = 'bestaudio / best'
        # self.option['skip_download'] =True


def get_video_formats(video_url):
    # 使用 subprocess 调用 yt-dlp 命令行来获取视频信息
    command = ["yt-dlp", "--format", "best", "--dump-json", video_url]
    result = subprocess.run(command, capture_output=True, text=True)

    # 将命令输出解析为 JSON 格式
    video_info = json.loads(result.stdout)

    # 打印视频可用的格式
    formats = video_info.get('formats', [])
    for format_entry in formats:
        print(f"Format ID: {format_entry['format_id']}")
        print(f"Resolution: {format_entry.get('height', 'N/A')}")
        print(f"Extension: {format_entry.get('ext', 'N/A')}")
        print(f"Filesize: {format_entry.get('filesize', 'N/A')}")
        print("------------")

# 使用方式
# dl = VideoDL()
# url = "https://www.youtube.com/watch?v=ZsNtwhOJINE&ab_channel=Kendra%27sLanguageSchool"
# dl.set_format('bestaudio/best').set_write_subtitles(True, "zh-CN").set_url(url)


# 现在发现只有在下载音视频的时候,才会把字母转化为lrc,而其他情况下却不会


# 有下面这些关键词
#     id
# title
# formats
# thumbnails
# thumbnail
# description
# channel_id
# channel_url
# duration
# view_count
# average_rating
# age_limit
# webpage_url
# categories
# tags
# playable_in_embed
# live_status
# release_timestamp
# _format_sort_fields
# automatic_captions
# subtitles
# comment_count
# chapters
# heatmap
# like_count
# channel
# channel_follower_count
# uploader
# uploader_id
# uploader_url
# upload_date
# availability
# original_url
# webpage_url_basename
# webpage_url_domain
# extractor
# extractor_key
# playlist
# playlist_index
# display_id
# fulltitle
# duration_string
# release_year
# is_live
# was_live
# requested_subtitles
# _has_drm
# epoch
# asr
# filesize
# format_id
# format_note
# source_preference
# fps
# audio_channels
# height
# quality
# has_drm
# tbr
# url
# width
# language
# language_preference
# preference
# ext
# vcodec
# acodec
# dynamic_range
# container
# downloader_options
# protocol
# resolution
# aspect_ratio
# http_headers
# audio_ext
# video_ext
# vbr
# abr
# format
