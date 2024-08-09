import sys, os
import toml

sys.dont_write_bytecode = True

def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def ask_users_options():
    clear_console()
    if not os.path.exists("imformation.toml"):
        with open("imformation.toml", "w", encoding="utf-8") as f:
            toml.dump({'ID_NUMBER': '身分證字號', 'BIRTH': 'YYYMMDD', 'NAME': '中文姓名', 'PHONE': '手機電話', 'EMAIL': '電子郵件'}, f)
            print("請先至imformation.toml 填妥個人資料")
            input("按Enter 結束...")
            sys.exit()

    data = toml.load("keywords.toml")

    for index, (key, value) in enumerate(data.items()):
        print(str(index+1) + " " + value["name"])

    MVO_index = int(input("選擇監理所: ")) - 1
    print("\n")
    if not 0 <= MVO_index < len(data):
        print("\n不合理的選擇")
        input("按Enter 結束...")
        sys.exit()
    clear_console()

    # Motor Vehicle Office
    MVO = list(data.keys())[MVO_index] 

    # 打印監理所轄下的監理站
    sub_keys = [sub_key for sub_key in data[MVO] if isinstance(data[MVO][sub_key], dict)]
    for index, sub_key in enumerate(sub_keys):
        sub_value = data[MVO][sub_key]
        print(f"{index+1}. {sub_value['Station']}")

    # Prompt user to choose from Station options
    station_index = int(input("請選擇監理站: ")) - 1
    print("\n")
    if not 0 <= station_index < len(sub_keys):
        print("\n不合理的選擇")
        input("按Enter 結束...")
        sys.exit()
    clear_console()

    selected_station = data[MVO][sub_keys[station_index]]

    print("是否重考:")
    print("1. 初次考試")
    print("2. 重考")
    option = input("請選擇: ")
    print("\n")
    Retake, keyword = None, None
    match option:
        case "1":
            Retake = False
            keyword = selected_station["First"]
        case "2":
            Retake = True
            keyword = selected_station["Retake"]
        case _:
            print("不合理的選擇")
            input("按Enter 結束...")
            sys.exit()
    clear_console()

    imformation = toml.load("imformation.toml")


    print("資料如下：")
    print(data[MVO]["name"])
    print(selected_station["Station"])
    print(f"重考：{Retake}")
    for key, value in imformation.items():
        print(f"{key}：{value}")
    quit = input("\n確認後請按Enter繼續或打ｑ退出： ")
    if quit.lower() == "q":
        sys.exit()
    clear_console()

    return {"MVO" : MVO, "Station" : selected_station["ID"], "Retake" : Retake, "Keywords" : keyword}

if __name__ == "__main__":
    print(ask_users_options())
