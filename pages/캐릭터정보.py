import requests
import pandas as pd
import streamlit as st
import datetime

api_key = "live_50138df357699939f3b790093592e8e075fc0519e008653d27fc175e2dc9da5ad961e05fef3f2d19e258e30bf46403b6"
header = {'x-nxopen-api-key': api_key}
char_name = st.session_state["char"]
character_name = st.text_input('캐릭터명을 입력하세요', char_name,)
#ocid 발급
url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={character_name}"
res = requests.get(url, headers= header).json()
if "ocid" in res.keys():
    ocid = res["ocid"]
    
    #기본정보 조회
    s_date = datetime.datetime.today() - datetime.timedelta(days=1)
    s_date = s_date.strftime("%Y-%m-%d")
    url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={s_date}"
    res = requests.get(url, headers= header).json()

    df = pd.DataFrame.from_dict([res])
    df1 = df[["character_name","character_level", "world_name", "character_gender", "character_class", "character_class_level", "character_guild_name"]] 
    df1 = df1.rename(columns={"character_name":"캐릭명", "character_level":"레벨","world_name":"서버", "character_gender":"성별", "character_class":"직업", "character_class_level":"달성전직", "character_guild_name":"길드명"})


    c_img = df["character_image"][0]
    st.markdown(f'<img src="{c_img}">', unsafe_allow_html= True)
    st.dataframe(df1)

    # 무릉도장 정보 조회
    url = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid}&date={s_date}"
    res = requests.get(url, headers= header).json()
    best_record = res["dojang_best_floor"]
    best_date = res["date_dojang_record"]
    best_time = res["dojang_best_time"]

    st.header(f"무릉도장 최고층수: {best_record}")
    st.header(f"무릉도장 달성일: {best_date[:10]}")
    st.header(f"무릉도장 소요시간(초): {best_time}")


else:
    st.header(f"{character_name}: 해당 캐릭터의 기록이 없어요")



    