# -*- coding=utf-8 -*-
import threading as th
import os
import requests
from urllib3.exceptions import ProtocolError
from requests.exceptions import ProxyError, ConnectionError, SSLError
from scripts import jpg2png_batch
# from pydub import AudioSegment

Fail = 1
Total_Success = 0
Partial_Success = 2
class Song_search_by_lyric():
    global Fail
    global Total_Success
    global Partial_Success
    # Next Update ++
    class Album():
        def __init__(self):
            self.timg_url = None
            self.intro_url = None


    class Song():
        def __init__(self, where_to_put_albums, songname = None, songid = None, songmid = None, albumname = None, albumid = None, albummid = None, lyric = None):
            # if not os.path.isdir(where_to_put_albums):
            #     raise ValueError("Not valid base folder path!")
            self.albums_folder = where_to_put_albums

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
            self.album_path = os.path.join(self.albums_folder, self.albummid + '-' + self.albumname)
            self.song_and_related_items_folder = os.path.join(self.album_path, self.songmid + '-' + self.songname)

        def get_song_data_path(self, type = 'm4a'):
            return os.path.join( self.song_and_related_items_folder, self.songname + '.%s'%(type))

        def get_album_timg_path(self, type = 'jpg'):
            return self.album_path + '/timg.%s' %(type)


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


        def make_album_folder(self):
            if not os.path.isdir(self.album_path):
                os.mkdir(self.album_path)

        def make_song_folder(self):
            if not os.path.isdir(self.song_and_related_items_folder):
                os.mkdir(self.song_and_related_items_folder)

        def iter_file_paths(self):
            yield self.get_song_data_path()
            yield self.get_album_timg_path()
            # yield self.get_comment_text_path()

        def iter_folders(self):
            yield self.albums_folder
            yield self.album_path
            yield self.song_and_related_items_folder

        # deprecated!
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

    def __init__(self, where="/Users/ChenHaodong/Downloads/music/scrapy/", search = None, total = 20):
        self.keyword = search
        self.total = total

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
                                "&p={1}" \
                                "&n={2}" \
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

        self._bucket = {}

        self._id2mid = {}

        self.where = where

        self.thrs = None

        self._fail_urls = []



    def run(self, search = None, total = None):
        if self._get_lyric_search_list(search, total) is not Fail:
            self._get_folders_ready()
            print(1)
            self._prepare_download_threadings()
            print(2)
            self._start_off_threadings(max_threadings=50)
            print(3)
            self._refetch()
            print(4)
            self._rename_files()
            print(5)
            self.convert_files()
            print(6)
            self._clear_bucket()
        else:
            print("Failed to run.")

# User Utilities
    def get_lyric_search_result(self, search = None, total = None):
        if self._get_lyric_search_list(search, total) is not Fail:
            return self._bucket
        else:
            print("Fail")
            return None

    def print_download_urls(self):
        self._get_lyric_search_list()
        for songmid in self._bucket:
            rq = requests.get(self._song_download_info_url.format(songmid).replace('_got_song_download_info_callback','_print_download_urls'))
            tmp = rq.text
            exec('self.'+tmp)

    def _print_download_urls(self, arg):
        sip = arg["req_0"]["data"]["sip"][0]
        purl = arg["req_0"]["data"]["midurlinfo"][0]["purl"]
        songmid = arg["req_0"]["data"]["midurlinfo"][0]["songmid"]
        song_download_url = os.path.join(sip, purl)
        print(song_download_url)

# Utilities
    def _clear_bucket(self):
        self._bucket = {}


    def resetKeyword(self, lyric_key):
        self.keyword = lyric_key
        return self


    def _get_and_exec(self, url, headers=None):
        try:
            html = requests.get(url, headers=headers)
        except (ProtocolError, ConnectionError, ProxyError, SSLError, IOError) as e:
            print(e.message)
            print("Try refetch later.")
            self._fail_urls += [(None, url, headers)]
        else:
            if html.status_code == 200:
                # 执行回调函数
                exec('self.'+html.content.replace('null', 'None'))
            else:
                raise IOError("Not Valid response status code %s" %(html.status_code))


    @staticmethod
    def _get_tmp_file_path(path):
        basepath, file = os.path.split(path)
        return os.path.join(basepath, '.'+file)

    @staticmethod
    def _get_permanent_file_path(tmp_path):
        path, file = os.path.split(tmp_path)
        if file[0] == '.': 
            file = file[1:]
        return os.path.join(path, file)

# Lyric Search
    def _get_lyric_search_list(self, keyword = None, total = None):
        if keyword is None:
            keyword = self.keyword
        if keyword is None:
            print("You should set keyword before you try to search something.")
            return Fail
        if total is None:
            total = self.total

        print("total is %s"%total)
        assert isinstance(total, int) and total > 0
        assert ""+keyword == keyword
        if total < 20:
            numperpage = total
        else:
            numperpage = 20
        curpage = 1
        while self._bucket is None or len(self._bucket) < total:
            html = requests.get(self._lyric_search_url.format(keyword, curpage, numperpage), headers = self._fetch_lyric_search_result_headers)
            # run callback: _lyric_search_callback
            # print html.text
            # print '\n\n'
            num = eval('self.'+html.text)
            print("Received %s"%num)
            # print("current total in bucket: "%self._bucket)
            if num > 0:
                curpage += 1
            else:
                print("No more! Currently got %s songs. You wished for %s" % (len(self._bucket), total))
                return Partial_Success
        return Total_Success

    # def _old_get_lyric_search_list(self, keyword = None, total = None):
    #     if keyword is None:
    #         keyword = self.keyword
    #     if keyword is None:
    #         print("You should set keyword before you try to search something.")
    #         return Fail
    #     curpage = 1000 # test for empty response
    #     numperpage = 20
    #     html = requests.get(self._lyric_search_url.format(keyword, curpage, numperpage), headers = self._fetch_lyric_search_result_headers)
    #     # run callback: _lyric_search_callback
    #     print html.text
    #     print '\n\n'
    #     exec('self.'+html.text)
    #     return Total_Success

    def _lyric_search_callback(self, arg):
        # self._bucket = {}
        # !!! if do this line up, what was received last time will be eliminated!!!
        list = arg['data']['lyric']['list']
        self.thrs = []
        for item in list:
            songname = item["songname"].replace('/',':')
            songmid = item["songmid"]
            songid = item["songid"]
            albumname = item['albumname'].replace('/',':')
            albummid =item["albummid"]
            albumid =item["albumid"]
            lyric = item["content"]
            self._bucket[songmid] = self.Song(self._get_keyword_folder(), songname, songid, songmid, albumname, albumid, albummid, lyric)
            print("%s %s"%(len(self._bucket), songname.replace(':','/')))
            self._id2mid[songid] = songmid
        # print(len(list))
        return len(list)
        #Used: self._prepare_download_threadings()
        #Prefer: separated steps.


# Prepare the related folder(s)
    def _get_keyword_folder(self):
        return os.path.join(self.where, self.keyword)

    def _get_folders_ready(self):
        base = self._get_keyword_folder()
        if not os.path.isdir(base):
            os.mkdir(base)
        for songmid in self._bucket:
            self._bucket[songmid].make_album_folder()
        for songmid in self._bucket:
            self._bucket[songmid].make_song_folder()


# Download Threadings
    def _prepare_download_threadings(self):
        albummids = set()
        # 开线程对每个list中的歌曲请求下载信息, 并执行回应的回调函数以提取下载地址进行下载
        for songmid in self._bucket:
            self.thrs += [th.Thread(target=self._get_and_exec, args=[self._song_download_info_url.format(songmid)])]
                # thread receive response => run _got_song_download_info_callback
        # 开线程抓取和保存歌曲的评论信息
            song = self._bucket[songmid]
            self.thrs += [th.Thread(target=self._get_and_exec, args=[self._comment_url.format(song.songid)])]
        # 开线程直接下载保存专辑的timg文件
            if song.albummid not in albummids:
                albummids.add(song.albummid)
                self.thrs += [th.Thread(target=self._get_album_timg, args=(self._album_timg_url.format(song.albummid),song.get_album_timg_path()))]


    def _start_off_threadings(self, max_threadings = 10):
        start = 0
        end = len(self.thrs)
        cur = 0
        step = max_threadings
        while cur < end:
            next = cur + step
            for thr in self.thrs[cur:next]:
                thr.start()
            for thr in self.thrs[cur:next]:
                thr.join()
            cur = next
        print("All threads joined!")

# Download songs and related information
    def _got_song_download_info_callback(self, arg):
        sip = arg["req_0"]["data"]["sip"][0]
        purl = arg["req_0"]["data"]["midurlinfo"][0]["purl"]
        songmid = arg["req_0"]["data"]["midurlinfo"][0]["songmid"]
        song_download_url = os.path.join(sip, purl)
        # ??-----
        # self._bucket[songmid].set_urls(song_url = song_download_url)
        # ------------------

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
            path = self._get_tmp_file_path(song.get_song_data_path())
            try:
                with open(path, 'wb') as f:
                    m4a_html = requests.get(song_download_url, headers=self._fetch_song_headers, stream = True)
                    f.write(m4a_html.raw.read())
            except (ProtocolError, ConnectionError, ProxyError, SSLError, IOError) as e:
                print(e.message)
                print("Try refetch later.")
                self._fail_urls += [(path, song_download_url, self._fetch_song_headers)]
            except Exception as e:
                print("###\nUnexpected Error. Please contact the writer!\n###")
                raise e
            else:
                self._rename_hidden_file(path)
                print("got song file: %s"%(os.path.split(path)[1]))


    def _get_album_timg(self, url, path):
        # ^^^^^^^^^  Check self.where exists at init
        folderpath = self._get_keyword_folder()
        if not os.path.isdir(folderpath):
            os.mkdir(folderpath)
        path = self._get_tmp_file_path(path)
        if not os.path.isfile(path):
            try:
                with open(path, "wb") as f:
                    jpg = requests.get(url, stream=True)
                    f.write(jpg.raw.read())
            except (ProtocolError, ConnectionError, ProxyError, SSLError, IOError) as e:
                print(e.message)
                print("Try refetch later.")
                self._fail_urls += [(path, url, None)]
            except Exception as e:
                print("###  Unexpected Error. Please contact the writer!  ###")
                raise e
            else:
                print("got timg of album: %s"%(os.path.split(path)[1]))

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
            path = song.get_comment_text_path()
            with open(path, 'w') as f:
                f.write(text)
            print("got comment on song %s"%(song.songname))

    def _refetch(self):
        for path, url, headers in self._fail_urls:
            try:
                if path is not None:
                    with open(path,'wb') as f:
                        f.write(requests.get(url, headers = headers, stream=True).content)
                else:
                    self._get_and_exec(url, headers=headers)
            except Exception as e:
                print(e.message)
                print("Fail again.. HOW? Abandon. %s, %s"%(path, url))
                if os.path.isfile(path):
                    os.remove(path)

# More Handles on Downloaded files
    def _rename_files(self):
        for songmid in self._bucket:
            for path in self._bucket[songmid].iter_file_paths():
                tmpfilepath = self._get_tmp_file_path(path)
                if os.path.isfile(tmpfilepath):
                    if os.path.getsize(tmpfilepath) > 0:
                        os.rename(tmpfilepath, path)
                    else:
                        print("Fail to get file %s"%path)
                        os.remove(tmpfilepath)

    def _rename_hidden_file(self, filepath):
        if os.path.isfile(filepath):
            if os.path.getsize(filepath) > 0:    
                os.rename(filepath, self._get_permanent_file_path(filepath))
                return True
            else:
                print("Hidden file %s not complete, deleted."%filepath)
                os.remove(filepath)
                return False

    @staticmethod
    def joinext(f,e):
        if e[0] == '.':
            return f+e
        else:
            return f+'.'+e

    def convert_files(self, music_type='mp3', img_type='png'):
        for songmid in self._bucket:
            song = self._bucket[songmid]
            songpath = song.get_song_data_path()
            if os.path.isfile(songpath):
                f,e = os.path.splitext(songpath)
                # AudioSegment.from_file(songpath)[0:60*1000].export(self.joinext(f,music_type),format='mp3')
                os.rename(songpath, f+'.mp3')
        jpg2png_batch(self._get_keyword_folder())
# need 搜索结果文件夹, 迭代所有歌对象

def main():
    s = Song_search_by_lyric(where=raw_input("Where to save? "), search='歌剧')
    # s.run()
    s.print_download_urls()

if __name__ == "__main__":
    main()
