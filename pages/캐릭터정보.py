import requests
import pandas as pd
import streamlit as st
import datetime


api_key = "live_50138df357699939f3b790093592e8e075fc0519e008653d27fc175e2dc9da5ad961e05fef3f2d19e258e30bf46403b6"
header = {'x-nxopen-api-key': api_key}
if "char" not in st.session_state:
    st.session_state["char"] = "마하방패"


char_name = st.session_state["char"]
character_name = st.text_input('캐릭터명을 입력하세요', f"{char_name}")
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
    df2 = df1.set_index("캐릭명")


    c_img = df["character_image"][0]
    st.markdown(f'<img src="{c_img}">', unsafe_allow_html= True)
    st.dataframe(df2, use_container_width=True)

    # 무릉도장 정보 조회
    url = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid}&date={s_date}"
    res = requests.get(url, headers= header).json()
    best_record = res["dojang_best_floor"]
    best_date = res["date_dojang_record"]
    best_time = res["dojang_best_time"]
    if best_date == None:
        best_date = "기록없음"
    st.markdown(f"# 무릉도장 기록:  {best_record}층 / {best_time}초")
    
    #유니온 정보 조회
    url = f"https://open.api.nexon.com/maplestory/v1/user/union?ocid={ocid}&date={s_date}"
    res = requests.get(url, headers= header).json()
    union_level =res["union_level"]
    union_grade =res["union_grade"]
    st.markdown(f"# 유니온: {union_level}레벨 /{union_grade}")

    #상세 스탯 정보 조회
    url = f'https://open.api.nexon.com/maplestory/v1/character/stat?ocid={ocid}&date={s_date}'
    res = requests.get(url, headers= header).json()
    res = res["final_stat"]
    df = pd.DataFrame(res)
    df = df.rename(columns={"stat_name":"스탯명", "stat_value":"값"})
    cobat_point = df[df["스탯명"]=="전투력"]["값"]
    combat_point = '{:,}'.format(int(cobat_point))
    df = df.set_index("스탯명")
    
    

            
    st.markdown(f"# 전투력 : {combat_point}")
    
    st.dataframe(df, use_container_width=True)




else:
    st.header(f"{character_name}: 해당 캐릭터의 기록이 없어요")



    