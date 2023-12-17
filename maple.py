import requests
import pandas as pd
import streamlit as st
import datetime



def get_cube_history(api_key, date):
    date_str = date.strftime("%Y%m%d")
    header = {'x-nxopen-api-key': api_key}
    url = f"https://open.api.nexon.com/maplestory/v1/history/cube?count=1000&date_kst={date_str}"
    response = requests.get(url, headers=header).json()

    if "error" in response:
        st.header(response["error"]["message"])
        return None
    elif len(response["cube_history"]) !=0 :
        return response["cube_history"]
    elif len(response["cube_history"]) ==0:
        st.header("큐브 사용 내역이 없습니다.")
        return  None

def display_cube_information(cube_history):
    if not cube_history:
        return

    count_cube = len(cube_history)
   
    if count_cube == 1000:
        count_cube = "1000번 넘도록"
    else:
        count_cube = f"{count_cube}번"
    st.write(f"당신은 이날 {count_cube} 큐브질을 했습니다.")
    df = pd.DataFrame(cube_history)

    st.write("큐브 등업 결과")
    df0 = df["item_upgrade_result"].value_counts().reset_index()
    df0.columns = ["item_upgrade_result", "count"]
        
    df0_style = df0.style.apply(lambda x: ['background-color: tan' if x["item_upgrade_result"] == '성공' else '' for _ in df0.columns], axis=1)
    st.dataframe(df0_style, use_container_width=True)

    

    df1 = df[["character_name", "world_name", "cube_type", "target_item", "date_create"]]
    
    st.dataframe(df1, use_container_width=True)       

    dl = []
    for i in range(len(df)):
        dic = df["after_potential_option"][i]
        dls = []
        for j in range(len(dic)):
            dv = dic[j]
            dv = dv["value"]
            dls.append(dv)
        dl.append(dls)

    df2 = pd.DataFrame(dl)
    df2.columns = ["첫번째", "두번째", "세번째"]
    df2["등급"] = df["potential_option_grade"]
    
    df2_style = df2.style.apply(
        lambda x:[
        'background-color: green' if x["등급"] == '레전드리' else
        'background-color: yellow' if x["등급"] == '유니크' else
        'background-color: blue' if x["등급"] == '에픽' else
        'background-color: purple' if x["등급"] == '레어' else ''
        for _ in df2.columns],
        axis=1
    )



    st.dataframe(df2_style, use_container_width=True)

def main():
    st.set_page_config(
        page_title="Use Wook`s maplestory",
        page_icon="👍"
    )

    st.header("일단 openapi.nexon.com에 가서 Api 키를 발급 받아야 합니다.")

    key = st.text_input('api키 입력', '', type="password")

    if key == '':
        st.header("api키가 없으면 조회가 안됩니다.")
    else:
        date = st.date_input("확인하고 싶은 날짜를 선택하세요.", datetime.datetime.today(), format="YYYY/MM/DD")
        cube_history = get_cube_history(key, date)
        
        if cube_history:
            display_cube_information(cube_history)
                  


if __name__ == "__main__":
    main()
