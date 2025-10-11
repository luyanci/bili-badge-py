import os
from loguru import logger
from dotenv import load_dotenv
from bilibili_api import Credential,user,sync
from pybadges import badge,_NAME_TO_COLOR

ENV_VAR_BILI_SESSDATA = "BILI_SESSDATA"
ENV_VAR_BILI_UID = "BILI_UID"
ENV_VAR_BILI_JCT = "BILI_JCT"
REQUIRED_ENVS = [
    ENV_VAR_BILI_SESSDATA,
    ENV_VAR_BILI_JCT,
    ENV_VAR_BILI_UID
]

# add some extra colors
_NAME_TO_COLOR["lightgreen"] = "#90ee90"
_NAME_TO_COLOR["lightblue"] = "#add8e6"
_NAME_TO_COLOR["lightorange"] = "#ffcc99"

default_left_color="blue"
default_right_color="grey"
common_whole_link="https://space.bilibili.com/"
default_logo = "https://cdn.simpleicons.org/bilibili/white"

def check_envs():
    logger.info("Checking required environment variables...")
    missing = []
    for env in REQUIRED_ENVS:
        if os.environ.get(env) is None:
            missing.append(env)
    if len(missing) > 0:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
    logger.info("All required environment variables are set.")
    return True

def getneededinfo(info: str,need: str):
    return info[need]

def write_file(filename:str,data:str):
    with open(filename,"wb") as file:
        file.write(data.encode('utf-8'))
    return



def make_info_badge(name:str="luyanci"):
    result = badge(
        left_color=default_left_color,
        right_color=default_right_color,
        logo=default_logo,
        left_text="BiliBili",
        right_text=f"@{name}",
        whole_link=f"{common_whole_link}{os.environ[ENV_VAR_BILI_UID]}",
        embed_logo=True
        )
    write_file("user.svg",result)

def make_follower_badge(number:int = 999):
    result = badge(
        left_color=default_left_color,
        right_color=default_right_color,
        logo=default_logo,
        left_text="BiliBili 粉丝数",
        right_text=str(number),
        whole_link=f"{common_whole_link}{os.environ[ENV_VAR_BILI_UID]}",
        embed_logo=True
        )
    write_file("follower.svg",result)

def make_following_badge(number:int = 999):
    result = badge(
        left_color=default_left_color,
        right_color=default_right_color,
        logo=default_logo,
        left_text="BiliBili 关注数",
        right_text=str(number),
        whole_link=f"{common_whole_link}{os.environ[ENV_VAR_BILI_UID]}",
        embed_logo=True
        )
    write_file("following.svg",result)

def make_level_badge(number:int = 0):
    level_colors = ["inactive","inactive","lightgreen","lightblue","lightorange","orange","red"] # Notes: level 0 and 1 are inactive(grey)
    result = badge(
        left_color=default_left_color,
        right_color=level_colors[number],
        logo=default_logo,
        left_text="BiliBili 等级",
        right_text=str(number),
        whole_link=f"{common_whole_link}{os.environ[ENV_VAR_BILI_UID]}",
        embed_logo=True
        )
    write_file("level.svg",result)

def make_live_status_badge(stat:int=0,url:str="https://live.bilibili.com"):
    live_status = ["Not Live","Live"]
    live_status_color = ["inactive","red"]
    result = badge(
        left_color=default_left_color,
        right_color=live_status_color[stat],
        logo=default_logo,
        left_text="BiliBili 直播间",
        right_text=live_status[stat],
        whole_link=url,
        embed_logo=True
        )
    write_file("liveroom.svg",result)

def make_view_badge(views:str,view_type:str = "video"):
    logger.info(f"Making view badge for {view_type}")
    if view_type == "video":
        left_text="BiliBili 播放数"
        right_text=getneededinfo(views,"archive")["view"]
    elif view_type == "like":
        left_text="BiliBili 获赞数"
        right_text=getneededinfo(views,"likes")
    elif view_type == "article":
        left_text="BiliBili 阅读数"
        right_text=getneededinfo(views,"article")["view"]
    else:
        logger.warning(f"Unknown view type {view_type}, fall back to video")
        make_view_badge(views)
    result = badge(
        left_color=default_left_color,
        right_color=default_right_color,
        logo=default_logo,
        left_text=left_text,
        right_text=str(right_text),
        embed_logo=True
        )
    write_file("views.svg",result)

@logger.catch
def main():
    check_envs()
    uid = os.environ[ENV_VAR_BILI_UID]
    sessdata = os.environ[ENV_VAR_BILI_SESSDATA]
    jct = os.environ[ENV_VAR_BILI_JCT]
    logger.info("Trying to get some info...")
    cedential = Credential(sessdata=sessdata,bili_jct=jct)
    u= user.User(uid,credential=cedential)
    i = sync(u.get_user_info())
    username= getneededinfo(i,"name")
    level = getneededinfo(i,"level")
    live_room = getneededinfo(i,"live_room")
    live_status = getneededinfo(live_room,"liveStatus")
    live_room_url = getneededinfo(live_room,"url")
    follows = sync(u.get_relation_info())
    follower= getneededinfo(follows,"follower")
    following = getneededinfo(follows,"following")
    views = sync(u.get_up_stat())
    logger.info("Making Badge...")
    make_info_badge(username)
    make_level_badge(level)
    make_live_status_badge(live_status,live_room_url)
    make_follower_badge(follower)
    make_following_badge(following)
    make_view_badge(views,view_type)

if __name__== "__main__":
    logger.add(f'./log.log',format='{time} {level} {function} - {message}')
    load_dotenv(dotenv_path="./.env")
    import time
    logger.info("Starting jobs...")
    s = time.perf_counter()
    if os.environ.get("BILI_VIEW_TYPE") is None:
        logger.info("BILI_VIEW_TYPE not set, using video as default")
        view_type="video"
    else:
        logger.info(f"BILI_VIEW_TYPE set to {os.environ.get('BILI_VIEW_TYPE')}")
        view_type=os.environ.get("BILI_VIEW_TYPE")
    main()
    elapsed = time.perf_counter() - s
    logger.info(f"{__file__} executed in {elapsed:0.2f} seconds.")
