import os
from loguru import logger
from dotenv import load_dotenv
from bilibili_api import Credential,user,sync
from pybadges import badge

ENV_VAR_BILI_SESSDATA = "BILI_SESSDATA"
ENV_VAR_BILI_UID = "BILI_UID"
REQUIRED_ENVS = [
    ENV_VAR_BILI_SESSDATA,
    ENV_VAR_BILI_UID
]

default_left_color="blue"
default_right_color="grey"
default_logo="https://cdn.simpleicons.org/bilibili"
common_whole_link="https://space.bilibili.com/"


def getneededinfo(info: str,need: str):
    return info[need]

def getvideoinfo(num: int,need: str):
    return vist["list"]["vlist"][num][need]

def getvideodate(num: int):
    import datetime
    from pytz import timezone
    tzc = timezone('Asia/Shanghai')
    date= getvideoinfo(num,"created")
    date_time = datetime.datetime.fromtimestamp(date,tz=tzc)
    formated_date = date_time.strftime("%Y年%m月%d日 %H:%M:%S")
    return formated_date

def write_file(filename:str,data:str):
    with open(filename,"wb") as file:
        file.write(data.encode('utf-8'))
    return

def make_follower_badge(number:int = 999):
    result = badge(
        left_color=default_left_color,
        right_color=default_right_color,
        logo=default_logo,
        left_text="BiliBili 粉丝数",
        right_text=str(number),
        whole_link=f"{common_whole_link}{os.environ[ENV_VAR_BILI_UID]}"
        )
    write_file("follower.svg",result)

def make_following_badge(number:int = 999):
    result = badge(
        left_color=default_left_color,
        right_color=default_right_color,
        logo=default_logo,
        left_text="BiliBili 关注数",
        right_text=str(number),
        whole_link=f"{common_whole_link}{os.environ[ENV_VAR_BILI_UID]}"
        )
    write_file("following.svg",result)

def make_level_badge():
    pass

def make_live_status_badge():
    pass

def make_view_badge():
    pass

@logger.catch
def main():
    global vist
    uid = os.environ[ENV_VAR_BILI_UID]
    sessdata= os.environ[ENV_VAR_BILI_SESSDATA]
    logger.info("Trying to get some info...")
    cedential = Credential(sessdata=sessdata)
    u= user.User(uid,credential=cedential)
    i = sync(u.get_user_info())
    follows = sync(u.get_relation_info())
    follower= getneededinfo(follows,"follower")
    following = getneededinfo(follows,"following")
    make_follower_badge(follower)
    make_following_badge(following)


if __name__== "__main__":
    logger.add(f'./log.log',format='{time} {level} {function} - {message}')
    load_dotenv(dotenv_path="./.env")
    import time
    logger.info("Starting jobs...")
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    logger.info(f"{__file__} executed in {elapsed:0.2f} seconds.")
