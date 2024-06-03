from function import xxmh, feishu  # 函数库
import time
import json
import os


if __name__ == "__main__":
    # 准备工作
    os.chdir(os.path.dirname(__file__))
    # 读取数据
    with open("./config/bupt.json", "r") as file:
        config = json.load(file)
    with open("./url/bupt.json", "r") as file:
        url = json.load(file)
    xxmh.login(url["cas"], url["xxmh"]["tongzhi"], config["username"], config["password"])
    notice_storages = xxmh.get_notice_list(url["xxmh"]["tongzhi"])

    # 爬取信息
    while True:
        notices = xxmh.get_notice_list(url["xxmh"]["tongzhi"])
        has_new = False
        print(time.strftime("%Y-%m-%d %H:%M"))

        for item in notices:
            if any(item["title"] == archive["title"] for archive in notice_storages):
                continue
            # 如果是新消息就存档并发送
            notice_storages.append(item)
            if len(notice_storages) > 100:
                notice_storages.pop(0)
            has_new = True
            print(item["title"])
            messages = feishu.send_to_group(item, xxmh.get_content(item["url"]))
            for item in messages:
                print(f"{item['name']}: 通知{item['message']['notice']}, 内容{item['message']['content']}")

        if not has_new:
            print("没有新通知")
        time.sleep(60)
