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
    s_date = datetime.datetime.today() - datetime.timedelta(days=1)
    s_date = s_date.strftime("%Y-%m-%d") 

    ri = random.randint(1,3)

    if  ri == 1:
        st.header("오늘의 종합랭킹")
        url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={s_date}"
    if ri == 2:
        st.header("오늘의 유니온랭킹")
        url = f"https://open.api.nexon.com/maplestory/v1/ranking/union?date={s_date}"
    if ri == 3:
        st.header("오늘의 무릉랭킹")
        url = f"https://open.api.nexon.com/maplestory/v1/ranking/dojang?date={s_date}&difficulty=1"
        
    res = requests.get(url, headers= header).json()
    res= res["ranking"]
    if len(res) == 0:
        st.write("랭킹이 조회되지 않습니다.")
    else:
        df =pd.DataFrame(res)
        df.drop("date", axis = 1, inplace= True)
        df= df.set_index("ranking")
        df = df.rename(columns={"character_name":"캐릭명", "character_level":"레벨","world_name":"서버", "character_popularity":"인기도", "character_guildname":"길드명"})
       
        
        ci = random.randint(1,200)
        st.session_state["char"] = df["캐릭명"][ci]
        st.dataframe(df,height=1000, use_container_width=True)

    st.markdown('''<script src="https://utteranc.es/client.js" 
                repo="[https://github.com/yong-wook/maple]" 
                issue-term="pathname" theme="github-light" 
                crossorigin="anonymous" async>
                </script>''', unsafe_allow_html= True)            


if __name__ == "__main__":
    main()



