import streamlit as st
import json
import pandas as pd
import plotly.express as px
import mysql.connector 
import plotly.io as pio
from decimal import Decimal
pio.renderers.default='browser'
st.set_page_config(layout='wide')
st.title('PHONEPE PULSE ')
phone_pe=mysql.connector.connect(host='localhost',user='root',password='Sandy@1630',auth_plugin='mysql_native_password')
mycursor=phone_pe.cursor(buffered=True)
mycursor.execute('USE phonepe')
Year=st.selectbox('kindly Select Year:',("2018","2019","2020","2021","2022"))
st.write('You Selected Year:',Year)
Quater=st.selectbox('Kindly Select Quater:',('1','2','3','4'))
st.write('1=Jan to Mar')
st.write('2= Apr to Jun')
st.write('3= Jul to Sep')
st.write('4= Oct to Dec')
st.write('You Selected Quater:',Quater)
Type=st.selectbox('Kindly Select The Payment:',('Recharge & bill payments','Peer to peer payment','Merchant payments','Financial Services','Others'))
st.write('You Selected:',Type)
Details=st.selectbox('Kindly Required Deatils:',('Aggregated Transaction','Registered Users'))
st.write('You Selected Details:',Details)
display_values={"Aggregated Transaction": 
                {"table_name":"ATransaction",
                "color":"Transaction_amount",
                "hover_name":"State",
                "hover_data":"Transaction_type",
                "title":"india phonepe transaction"},
                "Registered Users":
                {"table_name":"map_users",
                 "color":"id",
                 "hover_name":"State",
                 "hover_data":"RegisteredUserSum",
                 "title":"india phonepe Registered Users"},}
if Details=='Aggregated Transaction':
    mycursor.execute(f"SELECT * FROM {display_values[Details]['table_name']} WHERE Year={Year} AND Quater = {Quater} AND Transaction_type= '{Type}'")
elif Details == "Registered Users":
    mycursor.execute(f"SELECT State,Year,Quater,SUM(RegisteredUsers) as RegisteredUsersSum FROM {display_values[Details]['table_name']} WHERE Year={Year} AND Quater={Quater} Group By State,Year,Quater")
response=mycursor.fetchall()
phone_pe.commit()
response_list=[]
if Details=='Registered Users':
    print('Registered')
    response_list=[list(x) for x in response]
    for index,r in enumerate(response_list):
        if type(r[-1])== Decimal:
            response_list[index]=[r[0],r[1],r[2],int(r[3])]
        response=response_list

india_states=json.load(open('C:\\Users\\Admin\\Desktop\\pulse\\states_india.geojson','r'))
state_id_map = {}
for feature in india_states["features"]:
    feature['id']=feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']]=feature['id']
                                                         
                                                         
df=pd.DataFrame(response)


mycursor.execute(f"show columns FROM {display_values[Details]['table_name']};")
columns = mycursor.fetchall()
column_names=[details[0] for details in columns]
if Details == 'Registered Users':
    column_names.remove('MyIndex')
    column_names.remove('RegisteredUsers')
    column_names.remove('District')
    column_names.append('RegisteredUserSum')

df.columns=column_names

df['State']=df['State'].replace({'telangana':'Telangana', 
                                        'andaman-&-nicobar-islands':'Andaman & Nicobar Island',
                                    'andhra-pradesh':'Andhra Pradesh',
                                    'arunachal-pradesh':'Arunanchal Pradesh', 
                                    'assam':'Assam', 
                                    'bihar':'Bihar', 
                                    'chhattisgarh' :'Chhattisgarh', 
                                    'dadra-&-nagar-haveli-&-daman-&-diu':'Daman & Diu', 
                                    'goa':'Goa', 
                                    'gujarat':'Gujarat', 
                                    'haryana':'Haryana',
                                    'himachal-pradesh':'Himachal Pradesh', 
                                    'jammu-&-kashmir':'Jammu & Kashmir', 
                                    'jharkhand':'Jharkhand',
                                    'karnataka':'Karnataka', 
                                    'kerala':'Kerala', 
                                    'lakshadweep':'Lakshadweep', 
                                    'madhya-pradesh':'Madhya Pradesh', 
                                    'maharashtra':'Maharashtra', 
                                    'manipur':'Manipur', 
                                    'chandigarh':'Chandigarh', 
                                    'puducherry':'Puducherry', 
                                    'punjab':'Punjab', 
                                    'rajasthan':'Rajasthan', 
                                    'sikkim':'Sikkim', 
                                    'tamil-nadu':'Tamil Nadu', 
                                    'tripura':	'Tripura', 
                                    'uttar-pradesh':'Uttar Pradesh', 
                                    'uttarakhand':'Uttarakhand', 
                                    'west-bengal':'West Bengal', 
                                    'odisha':'Odisha', 
                                    'dadra-&-nagar-haveli-&-daman-&-diu':'Dadara & Nagar Havelli', 
                                    'meghalaya':'Meghalaya', 
                                    'mizoram': 'Mizoram', 
                                    'nagaland':'Nagaland',
                                    'ladakh':'Jammu & Kashmir',
                                    'delhi':'NCT of Delhi'})


df['id']=df['State'].apply(lambda x: state_id_map[x])

fig=px.choropleth(df,
                  locations='id',
                  geojson=india_states,
                  color=display_values[Details]["color"],
                  hover_name=display_values[Details]["hover_name"],
                  hover_data=[display_values[Details]['hover_data']],
                  title=display_values[Details]["title"])
fig.update_geos(fitbounds="locations",visible= False)

st.plotly_chart(fig,theme=None, use_container_width=True)
        

