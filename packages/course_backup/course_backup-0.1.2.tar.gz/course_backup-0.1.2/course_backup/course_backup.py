#!/usr/bin/env python
# encoding: utf-8

import requests
import bs4
import schedule
from tomorrow import threads
import time
import os
import sys
import click
from ConfigParser import SafeConfigParser
import datetime

class StudioConnection(object):
    '''
    >>> x=StudioConnection(sessionid="aaa", studio="cms.studio.com", csrftoken="bbb")
    >>> print x.studio
    cms.studio.com
    '''
    def __init__(self,
                 sessionid="",
                 studio="",
                 csrftoken=""):
        '''
        Initialize a connection to an edX studio instance. The key parameter is
        session_id. This must be picked out from the network console
        in developer tools in your web browser.
        '''
        self.sessionid = sessionid
        self.studio = studio
        self.csrftoken = csrftoken
        self.data_path="/tmp"
    def __str__(self):
        return '''
        studio:{0}
        csrftoken:{1}
        sessionid:{2}
        data_path:{3}
    '''.format(self.studio,self.csrftoken,self.sessionid,self.data_path)
    def compile_header(self):
        '''
        This will compile both header and cookies necessary to
        access an studio server as if this were a web browser. The
        key things needed are the session ID cookie. This can
        be grabbed from your browser in the developer tools.
        '''

        header = {}
        cookies = {}
        cookies["csrftoken"] = self.csrftoken
        cookies["sessionid"] = self.sessionid
        return (header, cookies)
    def _get_course_ids(self):
        header, cookies = self.compile_header()
        #import ipdb;ipdb.set_trace()
        courses_home_url = self.studio+"/home"
        studio_html = requests.get(courses_home_url,cookies=cookies)
        if studio_html.status_code == 200:
                studio_content = studio_html.content
        else:
            raise Exception("status_code is not 200")
        bs = bs4.BeautifulSoup(studio_content,"html5lib")
        course_items = bs.find_all("li",class_="course-item")
        course_ids = [course_item.get("data-course-key","") for course_item in course_items if course_item.get("data-course-key","")]
        return course_ids

    def get_course_id_and_download_urls(self):
        course_ids = self._get_course_ids()
        download_url_format = self.studio+"/export/{}?_accept=application/x-tgz"
        course_id_and_urls = [(course_id,download_url_format.format(course_id)) for course_id in course_ids]
        return course_id_and_urls

    @threads(5)
    def download_url(self,url,local_filename):
        header, cookies = self.compile_header()
        r = requests.get(url,cookies=cookies, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename

    def format_course_file_name(self,course_id):
        return course_id.split(":")[1].replace("+","_")+".tar.gz"

    def course_backup(self):
        course_id_and_download_urls = self.get_course_id_and_download_urls()
        #birch
        #courses = [self.download_url(url,id.replace("/","_")) for (id,url) in course_id_and_download_urls]
        #dogwood
        courses = [self.download_url(url,os.path.join(self.data_path,self.format_course_file_name(id))) for (id,url) in course_id_and_download_urls]
        print courses
        return courses

@click.command()
@click.option('--studio',default=None, help='The url of edx studio.')
@click.option('--sessionid',default=None, help='The sessionid of cookies.')
@click.option('--csrftoken',default=None, help='The csrftoken of cookies.')
@click.option('--courses_data_path',default="/tmp", help='The path to store course data. default: /tmp/{datetime}')
@click.option('--config_file',default=None, help='The path to config file. default: ~/.backup_course.ini')
@click.option('--start', is_flag=True)
@click.option('--night', is_flag=True)
def main(studio,sessionid,csrftoken,courses_data_path,config_file,start,night):
    if not start:
        print "backup_course --help"
        sys.exit(0)
    #首先显示help
    if not config_file:
        HOME = os.path.expanduser('~')
        default_config_file = os.path.join(HOME,".backup_course.ini")
        #check exists
        if not os.path.exists(default_config_file):
            #不存在则创建，不要报错
            open(default_config_file, 'w').close()
            #raise Exception("缺乏配置文件 ~/.backup_course.ini")
        config_file = default_config_file

    config = SafeConfigParser()
    config.read(default_config_file)
    config_file_studio = config.get('main', 'studio')
    config_file_sessionid = config.get('main', 'sessionid')
    config_file_csrftoken = config.get('main', 'csrftoken')

    #return "main exit"
    studioConn = StudioConnection()
    if not os.path.exists(courses_data_path):
        raise Exception(u"指定目录不存在，请创建")
    download_dir = os.path.join(courses_data_path,datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if not os.path.exists(download_dir):
            os.makedirs(download_dir)
    #检验是否存在不存在则创建
    studioConn.data_path = download_dir
    studioConn.studio = studio or config_file_studio #短路原则
    studioConn.sessionid = sessionid or config_file_sessionid
    studioConn.csrftoken = csrftoken or config_file_csrftoken
    #print studioConn.studio
    #sys.exit(0) #正常退出脚本
    print u"任务参数:"
    print studioConn
    if night:
        click.echo("将于夜里两点备份")
        schedule.every().day.at("02:00").do(studioConn.course_backup)
    else:
        print u"正在备份..."
        studioConn.course_backup()
    #schedule.every().day.at("02:00").do(studioConn.course_backup)
    #ApplicationInstance()  # 保证脚本单例运行
    #schedule 抽离出来写,直接手写而不是配置
    while True:
          schedule.run_pending()
          time.sleep(1)

if __name__ == '__main__':
    main()
