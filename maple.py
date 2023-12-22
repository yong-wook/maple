import requests
import pandas as pd
import streamlit as st
import datetime
import random


api_key = "live_50138df357699939f3b790093592e8e075fc0519e008653d27fc175e2dc9da5ad961e05fef3f2d19e258e30bf46403b6"
header = {'x-nxopen-api-key': api_key}


def main():
    st.set_page_config(
        page_title="Use Wook`s maplestory",
        page_icon="👍"
    )

    st.header("각종 메이플 정보 검색 공간입니다.")
    st.header("오늘의 종합랭킹")
    s_date = datetime.datetime.today() - datetime.timedelta(days=1)
    s_date = s_date.strftime("%Y-%m-%d") 

    url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={s_date}"
    res = requests.get(url, headers= header).json()
    res= res["ranking"]
    df =pd.DataFrame(res)
    df= df.set_index("ranking")
    df = df.rename(columns={"character_name":"캐릭명", "character_level":"레벨","world_name":"서버", "character_gender":"성별", "character_guild_name":"길드명"})
    
    ci = random.randint(1,200)
    st.session_state["char"] = df["캐릭명"][ci]
    st.dataframe(df, use_container_width=True)

                  


if __name__ == "__main__":
    main()



