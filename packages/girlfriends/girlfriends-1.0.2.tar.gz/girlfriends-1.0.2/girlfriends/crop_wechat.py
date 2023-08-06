#!/usr/bin/python
# -*- encoding:utf8 -*-
import requests
import logging
import json
from config import CROP_ID, CROP_SECRET

logger = logging.getLogger('crop_wechat');
logger.setLevel(logging.DEBUG);
ch = logging.StreamHandler();
ch.setLevel(logging.DEBUG);
formatter = logging.Formatter("[%(asctime)s]%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch);


class CropWeChat(object):
    """微信企业号API"""

    def __init__(self, crop_id=None, crop_secret=None):
        self.CROP_ID = crop_id;
        self.CROP_SECRET = crop_secret;
        if not self.CROP_ID:
            self.CROP_ID=CROP_ID;
            self.CROP_SECRET=CROP_SECRET;
        self.access_token = self.__get_access_token();


    """
    AccessToken是企业号的全局唯一票据，调用接口时需携带AccessToken。
    AccessToken需要用CorpID和Secret来换取，不同的Secret会返回不同的AccessToken。正常情况下AccessToken有效期为7200秒，有效期内重复获取返回相同结果；有效期内有接口交互（包括获取AccessToken的接口），会自动续期。

    请求说明
    Https请求方式: GET
    https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=id&corpsecret=secrect
    参数说明
    参数	必须	说明
    corpid	是	企业Id
    corpsecret	是	管理组的凭证密钥
    权限说明
    每个secret代表了对应用、通讯录的不同权限；不同的管理组拥有不同的secret。
    返回说明
    a)正确的Json返回结果:

    {
       "access_token": "accesstoken000001",
       "expires_in": 7200
    }
    """

    def __get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (self.CROP_ID, self.CROP_SECRET);
        logger.info(url)
        res = requests.get(url);
        # logger.info(res.text)
        access_token = res.json().get("access_token");
        logger.info("access_token=%s" % access_token);
        return access_token;

    def sendTextMsg(self,content):
        url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"%self.access_token;
        data={
               "touser": "rocyuan",
               #"toparty": " PartyID1 | PartyID2 ",
               #"totag": " TagID1 | TagID2 ",
               "msgtype": "text",
               "agentid": 1,
               "text": {
                   "content": content
               },
               "safe":"0"
        }
        result = requests.post(url,data=json.dumps(data).decode('unicode-escape').encode("utf-8")).json();
        logger.info(result)


if __name__ == "__main__":
    logger.info("main test begin :");
    cropWeChat = CropWeChat();
    cropWeChat.sendTextMsg("hi hello message");
    logger.info("main test end :");
