import requests
import pandas as pd
import streamlit as st
import datetime


st.set_page_config (
    page_title="Use Wook`s maplestory",
    page_icon="👍"
)



st.header("일단 openapi.nexon.com에 가서 Api 키를 발급 받아야 합니다.")

key = st.text_input('api키 입력', '' , label_visibility= "collapsed")

#key = "live_50138df357699939f3b790093592e8e075fc0519e008653d27fc175e2dc9da5ad961e05fef3f2d19e258e30bf46403b6"
if key =='':
    st.header("api키가 없으면 조회가 안됩니다.")

else:
    date = st.date_input("확인하고 싶은 날짜를 선택하세요.", datetime.datetime.today(), format="YYYY/MM/DD")
    date = date.strftime("%Y%m%d")
    header = {'x-nxopen-api-key':key}

    res = requests.get(f"https://open.api.nexon.com/maplestory/v1/history/cube?count=1000&date_kst={date}", headers=header).json()
    
    if "error" in res:
        st.header(res["error"]["message"])
    
    else:
        res = res["cube_history"]
        
        if len(res) == 0:
            st.header("큐브 사용 내역이 없습니다.")

        else:
            df = pd.DataFrame(res)
            df1 = df[["character_name", "date_create", "cube_type", "target_item", "item_upgrade_result"]]
            st.dataframe(df1)

            dl = []
            for i in range(len(df)):
                dic = df["before_potential_option"][i]
                dls = []
                for j in range(len(dic)):
                    dv = dic[j]
                    dv = dv["value"]
                    dls.append(dv)
                dl.append(dls)

            #print(df.keys())

            df2 = pd.DataFrame(dl)
            df2.columns = ["첫번째","두번째","세번째"]
            st.dataframe(df2)
            