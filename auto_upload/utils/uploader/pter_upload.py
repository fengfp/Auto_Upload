from loguru import logger
import time
import os
from selenium.webdriver.common.keys import Keys
from auto_upload.utils.uploader.upload_tools import *
from selenium.webdriver.support.select import Select

def pter_upload(web,file1,record_path,qbinfo):

    if (file1.pathinfo.type=='anime' or file1.pathinfo.type=='tv') and file1.pathinfo.collection==0:
        fileinfo=file1.chinesename+'在'+web.site.sitename+'第'+file1.episodename+'集'
    else:
        fileinfo=file1.chinesename+'在'+web.site.sitename

    web.driver.get(web.site.uploadurl)
    logger.info('正在'+web.site.sitename+'发布种子...')
    try:
        web.driver.find_element_by_class_name('file').send_keys(file1.torrentpath);
    except Exception as r:
        logger.warning('上传种子文件发生错误，错误信息: %s' %(r))
        return False,fileinfo+'上传种子文件发生错误'
    logger.info('已成功上传种子')

    try:
        if len(web.driver.find_elements_by_name('name'))<=0:
            web.driver.execute_script("window.scrollBy(0,300)")
        #web.driver.find_elements_by_name('name')[0].click()
        web.driver.find_elements_by_name('name')[0].send_keys(Keys.CONTROL, "a")
        web.driver.find_elements_by_name('name')[0].send_keys(Keys.BACKSPACE)
        web.driver.find_elements_by_name('name')[0].send_keys(Keys.BACKSPACE)
        web.driver.find_elements_by_name('name')[0].send_keys(file1.uploadname)
        logger.info('已成功填写主标题')
    except Exception as r:
        logger.warning('填写主标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写主标题发生错误'
    try:
        #web.driver.find_elements_by_name('small_descr')[0].click()
        web.driver.find_elements_by_name('small_descr')[0].send_keys(file1.small_descr)
        logger.info('已成功填写副标题')
    except Exception as r:
        logger.warning('填写副标题发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写副标题发生错误'
    try:
        #web.driver.find_elements_by_name('douban')[0].click()
        web.driver.find_elements_by_name('douban')[0].send_keys(file1.doubanurl)
        logger.info('已成功填写豆瓣链接')
    except Exception as r:
        logger.warning('填写豆瓣链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写豆瓣链接发生错误'

    try:
        #web.driver.find_elements_by_name('url')[0].click()
        web.driver.find_elements_by_name('url')[0].send_keys(file1.imdburl)
        logger.info('已成功填写IMDb链接')
    except Exception as r:
        logger.warning('填写IMDb链接发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写IMDb链接发生错误'

    try:
        #web.driver.find_elements_by_name('descr')[0].click()
        web.driver.find_elements_by_name('descr')[0].send_keys(file1.content)
        logger.info('已成功填写简介')
    except Exception as r:
        logger.warning('填写简介发生错误，错误信息: %s' %(r))
        return False,fileinfo+'填写简介发生错误'

    try:
        select_type = web.driver.find_element('name','type')  
        select_type = Select(select_type)
        if file1.pathinfo.type=='anime':
            select_type.select_by_value('403')
        elif file1.pathinfo.type=='tv':
            select_type.select_by_value('404')
        elif file1.pathinfo.type=='movie':
            select_type.select_by_value('401')
        else:
            select_type.select_by_value('403')

        logger.info('已成功选择类型为'+file1.pathinfo.type)
    except Exception as r:
        logger.warning('选择类型发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择类型发生错误'

    #选择质量
    try:
        select_source_sel = web.driver.find_element('name','source_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_source_sel_ob = Select(select_source_sel)    #生成下拉框的实例对象
        select_source_sel_ob.select_by_value('5')
        if file1.type=='WEB-DL':
            select_source_sel_ob.select_by_value('5')
        elif file1.type=='WEBRip':
            select_source_sel_ob.select_by_value('6')
        else:
            select_source_sel_ob.select_by_value('5')
        logger.info('已成功选择质量为'+file1.type)
    except Exception as r:
        logger.warning('选择质量发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择质量发生错误'

    #选择地区
    try:
        select_team_sel = web.driver.find_element('name','team_sel')    #定位到id为browsecat的下拉框并起名为select_ele
        select_team_sel_ob = Select(select_team_sel)    #生成下拉框的实例对象
        if not file1.country=='':
            if '大陆' in file1.country:
                select_team_sel_ob.select_by_value('1')
                logger.info('国家信息已选择'+file1.country)
            elif '香港' in file1.country:
                select_team_sel_ob.select_by_value('2')
                logger.info('国家信息已选择'+file1.country)
            elif '台湾' in file1.country:
                select_team_sel_ob.select_by_value('3')
                logger.info('国家信息已选择'+file1.country)
            elif '美国' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '英国' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '法国' in file1.country:
                select_team_sel_ob.select_by_value('4')
                logger.info('国家信息已选择'+file1.country)
            elif '韩国' in file1.country:
                select_team_sel_ob.select_by_value('5')
                logger.info('国家信息已选择'+file1.country)
            elif '日本' in file1.country:
                select_team_sel_ob.select_by_value('6')
                logger.info('国家信息已选择'+file1.country)
            elif '印度' in file1.country:
                select_team_sel_ob.select_by_value('7')
                logger.info('国家信息已选择'+file1.country)
            else:
                select_team_sel_ob.select_by_value('6')
                logger.info('未找到资源国家信息，已默认日本')
        else:
            select_team_sel_ob.select_by_value('6')
            logger.info('未找到资源国家信息，已默认日本')
    except Exception as r:
        logger.warning('选择地区发生错误，错误信息: %s' %(r))
        return False,fileinfo+'选择地区发生错误'

    try:
        if not file1.sublan=='' and ('简' in file1.sublan or '繁' in file1.sublan or '中' in file1.sublan):
            checkbox=web.driver.find_elements_by_name('zhongzi')[0]
            if not checkbox.is_selected():
                checkbox.click()
            logger.info('已选择中字')
    except Exception as r:
        logger.warning('选择中字发生错误，错误信息: %s' %(r))

    try:
        if web.site.uplver==1:
            checkbox=web.driver.find_elements_by_name('uplver')[0]
            if not checkbox.is_selected():
                checkbox.click()
            logger.info('已选择匿名发布')
    except Exception as r:
        logger.warning('选择匿名发布发生错误，错误信息: %s' %(r))


    
    String_url = web.driver.current_url;
    try:
        web.driver.find_elements_by_id('qr')[0].click()
    except Exception as r:
        logger.warning('发布种子发生错误，错误信息: %s' %(r))
        return False,fileinfo+'发布种子发生错误'

    logger.info('已发布成功')

    String_url =finduploadurl(web.driver)

    downloadurl=finddownloadurl(driver=web.driver,elementstr='/html/body/table[2]/tbody/tr[2]/td/table[1]/tbody/tr[9]/td[2]/a')
    
    recordupload(os.path.join(record_path,web.site.sitename+'_torrent.csv'),file1,String_url,downloadurl)
    if not downloadurl =='':
        res=qbseed(url=downloadurl,filepath=file1.path,qbinfo=qbinfo)
        if res:
            return True,fileinfo+'种子发布成功,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
        else:
            return True,fileinfo+'添加种子失败,种子链接:'+downloadurl+',当前网址:'+web.driver.current_url
    else:
        return False,fileinfo+'未找到下载链接,当前网址:'+web.driver.current_url

    





