# -*- coding=utf-8 -*-
import threading as th
import os
import requests

class Song_search_by_lyric():
    # Next Update ++
    class Album():
        def __init__(self):
            self.timg_url = None
            self.intro_url = None


    class Song():
        def __init__(self, where_to_put_albums, songname = None, songid = None, songmid = None, albumname = None, albumid = None, albummid = None, lyric = None):
            # if not os.path.isdir(where_to_put_albums):
            #     raise ValueError("Not valid base folder path!")
            self.where = where_to_put_albums

            self.songname = songname
            self.songid = songid
            self.songmid = songmid
            self.albumname = albumname
            self.albumid = albumid
            self.albummid = albummid
            self.lyric = lyric

            self.song_url = None # 待定
            self.album_timg_url = None
            self.intro_url = None
            self.comment_url = None

            self.album_path = None
            self.song_and_related_items_folder = None


            self._decide_path()


        def set_urls(self, song_url = None, album_timg_url = 'https://y.gtimg.cn/music/photo_new/T002R300x300M000%s', intro_url='', comment_url=''):
            self.song_url = song_url
            self.album_timg_url = album_timg_url % (self.albummid)
            self.intro_url = intro_url % (self.songmid)
            self.comment_url = comment_url % (self.songmid)

    # Song Resources' Paths

        # --
        def _decide_path(self):
            self.album_path = os.path.join(self.where, self.albummid + '|' +self.albumname)
            self.song_and_related_items_folder = os.path.join(self.album_path, self.songmid + '|' + self.songname)

        def get_song_data_path(self, type = 'm4a'):
            return os.path.join( self.song_and_related_items_folder, self.songname + '.%s'%(type))

        def get_album_timg_path(self, type = 'jpg'):
            return os.path.join( self.where, self.albummid + '|' +self.albumname) + '/timg.%s' %(type)


        # Next Update ++++++++
        # All text data in json style
        def get_json_path(self):
            pass

        # Next Update -------
        def get_intro_text_path(self):
            return os.path.join( self.song_and_related_items_folder, 'intro.txt')

        def get_comment_text_path(self):
            return os.path.join( self.song_and_related_items_folder, 'comment.txt')

        def get_lyric_text_path(self):
            return os.path.join( self.song_and_related_items_folder, 'lyric.txt')


        def iter_folders(self):
            yield self.where
            yield self.album_path
            yield self.song_and_related_items_folder

        def make_dirs(self):
            for dir in self.iter_folders():
                if not os.path.isdir(dir):
                    try:
                        os.mkdir(dir)
                    except Exception as e:
                        print("Can't create new folder %s"%(dir))
                        raise e
            return self

        # ?----
        def ego_integrity(self):
            return self


#------------------------------------------分界线----------------------------------------------

    def __init__(self, search, where):
        self.keyword = search


        self._song_download_info_url = "https://u.y.qq.com/cgi-bin/musicu.fcg" \
                                 "?callback=_got_song_download_info_callback" \
                                 "&g_tk=5381" \
                                 "&jsonpCallback=getplaysongvkey35573818353190245" \
                                 "&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8" \
                                 "&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0" \
                                 "&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%227169098396%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%227169098396%22%2C%22songmid%22%3A%5B%22{0}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A20%2C%22cv%22%3A0%7D%7D"

        self._fetch_song_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Host': 'dl.stream.qqmusic.qq.com'
        }

        self._lyric_search_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp" \
                                "?jsonpCallback=_lyric_search_callback" \
                                "&callback=_lyric_search_callback" \
                                "ct=10" \
                                "&t=7" \
                                "&p=1" \
                                "&n=20" \
                                "&w={0}"

        self._fetch_lyric_search_result_headers = {
            "referer": "https://y.qq.com/portal/search.html",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        }

        self._lyric_download_url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=217413935&callback=jsonp1&g_tk=1487699071&jsonpCallback=jsonp1&loginUin=411589954&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"


        # ~.format(songmid)
        # self._song_timg_url =  None # 不存在! 只有专辑才有封面! 歌曲播放时的封面都是跟专辑的!

        # related func:
        # ~.format(albummid)
        self._album_timg_url = 'https://y.gtimg.cn/music/photo_new/T002R300x300M000{0}.jpg?max_age=2592000'

        # ~~~~~~~~~~~~~+
        self._comment_url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg" \
              "?callback=_got_comments_callback" \
              "&jsonpCallback=_got_comments_callback" \
              "&cmd=6" \
              "&biztype=1" \
              "&topid={}" \
              "&pagenum=0" \
              "&pagesize=4" \
              "&format=jsonp" \
              "&outCharset=utf8" \
              "&inCharset=utf8" # 传入歌曲id 而不是mid

        self._intro_url = None

        # song download url is given directly by html response

        self._bucket = None

        self._id2mid = {}

        self.where = where

        self.thrs = None


    def resetKeyword(self, lyric_key):
        self.keyword = lyric_key


    def run(self):
        self._get_lyric_search_list()
        self._prepare_download_threadings()
        self._start_off_threadings()


    def _get_and_exec(self, url, headers=None):
        html = requests.get(url, headers=headers)
        if html.status_code == 200:
            # 执行回调函数
            exec('self.'+html.content.replace('null', 'None'))
        else:
            raise IOError("Not Valid response status code %s" %(html.status_code))

    def _get_album_timg(self, albummid, albumname):
        # ^^^^^^^^^  Check self.where exists at init
        folderpath = os.path.join(self.where, self.keyword)
        if not os.path.isdir(folderpath):
            os.mkdir(folderpath)
        path = folderpath + '/' + albummid + '|' + albumname + '.jpg'
        if not os.path.isfile(path):
            with open(path, "wb") as f:
                jpg = requests.get(self._album_timg_url.format(albummid), stream=True)
                f.write(jpg.raw.read())
        print("got timg of album: %s"%(albumname))


# Lyric Search
    def _get_lyric_search_list(self):
        html = requests.get(self._lyric_search_url.format(self.keyword), headers = self._fetch_lyric_search_result_headers)
        # run callback: _lyric_search_callback
        print html.text
        exec('self.'+html.text)

    def _lyric_search_callback(self, arg):
        self._bucket = {}
        list = arg['data']['lyric']['list']
        self.thrs = []
        for item in list:
            songname = item["songname"]
            songmid = item["songmid"]
            songid = item["songid"]
            albumname = item['albumname']
            albummid =item["albummid"]
            albumid =item["albumid"]
            lyric = item["content"]
            self._bucket[songmid] = self.Song(os.path.join(self.where, self.keyword), songname, songid, songmid, albumname, albumid, albummid, lyric).make_dirs()
            self._id2mid[songid] = songmid
        # self._prepare_download_threadings()

# Prepare the related folder(s)
    def _get_folders_ready(self):
        for songmid in self._bucket:
            self._bucket[songmid].make_dirs()

# Download Threadings
    def _prepare_download_threadings(self):
        albumnames = {}
        # 开线程对每个list中的歌曲请求下载信息, 并执行回应的回调函数以提取下载地址进行下载
        for songmid in self._bucket:
            self.thrs += [th.Thread(target=self._get_and_exec, args=[self._song_download_info_url.format(songmid)])]
                # thread receive response => run _got_song_download_info_callback
        # 开线程抓取和保存歌曲的评论信息
            song = self._bucket[songmid]
            self.thrs += [th.Thread(target=self._get_and_exec, args=[self._comment_url.format(song.songid)])]
            albumnames[song.albummid]=song.albumname
        # 开线程直接下载保存专辑的timg文件
        for albummid in albumnames:
            self.thrs += [th.Thread(target=self._get_album_timg, args=(albummid, albumnames[albummid]))]


    def _start_off_threadings(self):
        for thr in self.thrs:
            thr.start()
        for thr in self.thrs:
            thr.join()


# Download songs and related information
    def _got_song_download_info_callback(self, arg):
        sip = arg["req_0"]["data"]["sip"][0]
        purl = arg["req_0"]["data"]["midurlinfo"][0]["purl"]
        songmid = arg["req_0"]["data"]["midurlinfo"][0]["songmid"]
        song_download_url = os.path.join(sip, purl)
        # ??-----
        # self._bucket[songmid].set_urls(song_url = song_download_url)
        # ------------------
        m4a_html = requests.get(song_download_url, headers=self._fetch_song_headers, stream = True)

        # ------
        # 不行, 必须在lyricSearch的回调中获取图标, 因为歌曲下载信息里不包括albummid
        # thr_get_albumtimg=th.Thread(target=requests.get(self._album_timg_url.format(albummid)))

        try:
            song=self._bucket[songmid]
        except Exception as e:
        # 1. response中的songmid 和 search结果中的songmid不一致
        # 2. 其他情况
            raise e
        else:
            # Later Update +++ => singername
            path = song.get_song_data_path()
            try:
                with open(path, 'wb') as f:
                    f.write(m4a_html.raw.read())
            except IOError as e:
                print(e.message)
                raise IOError('Folder not created already! '
                              'Check @class Song(): def make_dirs(self):. '
                              'Or check whether it is called in the previous process.')
            else:
                print("got song file: %s"%(os.path.split(path)[1]))

    def _got_comments_callback(self, arg):
        id = arg['topid']
        # lst= arg['comment']['commentlist']
        # comment = lst[0]['rootcommentcontent']
        # print comment
        if arg['comment']['commentlist'] is not None:
            comments = [i['rootcommentcontent'] for i in arg['comment']['commentlist']]
            text = ''
            for c in comments:
                text += c
                text += '\n\n'
            song = self._bucket[self._id2mid[int(id)]]
            with open(song.get_comment_text_path(), 'w') as f:
               f.write(text)
            print("got comment on song %s"%(song.songname))


def main():
    search = input("Type in your keywords of music in desire.")
    where = input("Where to save your result?")
    if os.path.isdir(where):
        s = Song_search_by_lyric(search, where)
        s.run()
    else:
        print("Not valid folder path.")

if __name__ == "__main__":
    main()
