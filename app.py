#1.上传照片数据组
#2.获取照片的exif属性以及文件的创建时间
#3.根据文件的创建时间或文件名对文件排序

#http://cw.hubwiz.com/card/c/streamlit-manual/1/7/3/
## .streamlit/config.toml




import streamlit as st
import pandas as pd
import os
import math
from PIL import Image
from PIL.ExifTags import TAGS
from io import StringIO,BytesIO

#逻辑部分




#  streamlit run webUI.py


#WebUI界面部分
st.title("从照片获取GPS数据")

uploaded_files = st.file_uploader("选择照片数据...", type="jpg",accept_multiple_files=True)
sum = len(uploaded_files)
if sum > 0:
    st.success('成功上传{}张照片!'.format(sum), icon="✅")

col1, col2,col3= st.columns(3)


@st.cache_resource
def calculatedDistance():
    """"计算档距"""
    tower_distance =[] #档距
    #获取上传文件的pillow文件对象
    img_pilow_objs = []
    if uploaded_files is not None:

        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            file_name = uploaded_file.name #照片名称
            img = Image.open(BytesIO(bytes_data))

            img_pilow_objs.append((file_name,img))

   # 按照片的创建时间对上传的照片文件进行重新排序
    if option =="按文件创建时间排序":
        import towerSpace

        photos_obj = towerSpace.sort_photos_by_date(img_pilow_objs)
        coordinates = towerSpace.get_all_coordinates(photos_obj)

        for i in range(len(coordinates) - 1):
            if i ==0:
                coordinates[0].append(0)
            diffs = towerSpace.distance(coordinates[i + 1], coordinates[i])
            coordinates[i+1].append(diffs)

        tower_distance = coordinates
    else:
        st.error('当前暂不支持”按文件名称排序“，请使用默认选项', icon="🚨")

    return tower_distance


tower_distance = []
with col1:
    option = st.selectbox(
        "选择照片的排序方式",
        ("按文件创建时间排序", "按文件名称排序"),
        label_visibility="collapsed",
        disabled=False,
    )


with col3:


    if st.button('计算档距'):
        tower_distance =calculatedDistance()
    else:
        pass


if tower_distance:
    # 二元列表转DataFrame
    df = pd.DataFrame(tower_distance, columns=['照片名称', '经度', '纬度', "高度", "档距"])
    st.dataframe(df)
    st.download_button(label="导出 CSV", data=df.to_csv(index=False), file_name="杆塔档距计算结果表.csv", mime="text/csv")



