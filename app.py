import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
import sys
import requests 
import json
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

class Doctor:
    def __init__(self, email, name, surname, salary, phone, cname, degree, id):
        self.email = email
        self.name = name
        self.surname = surname
        self.salary = salary
        self.phone = phone
        self.cname = cname
        self.degree = degree
        self.id = id

class Disesase:
    def __init__(self, code, pathogen, description, id, disease_type):
        self.code = code
        self.pathogen = pathogen
        self.description = description
        self.id = id
        self.disease_type = disease_type


session = requests.Session()

def click(email: str):
    print(email)

def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

def post(url, obj):
    try:
        resp = requests.post(url, json = obj)
        obj = json.loads(resp.text)
        if resp.status_code != 200:
            st.warning(str(obj['code']) + ":" + str(obj['message']))
        else:
            st.success('Success')
        return obj
    except Exception:
        return {}

def put(url, obj):
    try:
        resp = requests.put(url, json = obj)
        obj = json.loads(resp.text)
        if resp.status_code != 200:
            st.error(str(obj['code']) + ":" + str(obj['message']))
        else:
            st.success('Success')
        return obj
    except Exception:
        return {}

def delete(url):
    try:
        resp = requests.delete(url)
        if resp.status_code != 200:
            st.error(str(obj['code']) + ":" + str(obj['message']))
        else:
            st.success('Success')

    except Exception:
        return {}


def crud_box():
    return st.selectbox("Choose operation:",["Create", "Read", "Update", "Delete"])



def main_page():
    st.markdown("# Main Page")
    st.sidebar.markdown("# Main Page")

def disease():
    st.markdown("# Disease")
    st.sidebar.markdown("# Disease")
    
    code = ""
        
    resp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/all")

    df = pd.DataFrame.from_records(resp)

    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    options.configure_selection("single")

    grid_return = AgGrid(df, gridOptions=options.build())
    # print(grid_return)
    if len(grid_return['selected_rows']) > 0:
        code = grid_return['selected_rows'][0]["code"]

    selected_box = crud_box()
    if selected_box == "Create":    
        form = st.form("Create Disease")
        code = form.text_input(label='Disease Code')
        pathogen = form.text_input(label='pathogen')
        description = form.text_input(label='description')
        id = form.number_input(label='id')
        submit_button = form.form_submit_button(label='Submit')
        if submit_button:
            d = Disesase(code, pathogen, description, int(id))
            createDoctorResp = post("https://disease-api-roland.herokuapp.com/disease/create", d.__dict__), 
            print(createDoctorResp)
            resp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/all")
    elif selected_box == "Read":
        form = st.form("Read Disease")
        code = form.text_input(label='Disease Code')
        submit = form.form_submit_button()

        if submit:
            getDoctorResp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/" + code)
            st.json(getDoctorResp)

    elif selected_box == "Update" and code != "":
        getDoctorResp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/" + code)
        
        form = st.form("Update Disease")
        code = form.text_input(label='Disease Code', value=getDoctorResp['code'])
        pathogen = form.text_input(label='pathogen', value=getDoctorResp['pathogen'])
        description = form.text_input(label='description', value=getDoctorResp['description'])
        id = form.number_input(label='id', value=getDoctorResp['id'])
        submit_button = form.form_submit_button(label='Submit')

        if submit_button:
            d = Disesase(code, pathogen, description, int(id), 'type')
            updateDoctorResp= put("https://disease-api-roland.herokuapp.com/disease/" + str(d.code), d.__dict__), 
            print(updateDoctorResp)
            resp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/all")
    elif selected_box == "Delete" and code != "":
        getDoctorResp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/" + code)
        
        form = st.form("Delete Doctor")
        submit_button = form.form_submit_button(label='Delete')

        if submit_button:
            deleteDoctorResp= delete("https://disease-api-roland.herokuapp.com/disease/" + str(code)), 
            print(deleteDoctorResp)
            resp = fetch(session, "https://disease-api-roland.herokuapp.com/disease/all")

def disease_type():
    st.markdown("# Disease Type")
    st.sidebar.markdown("# Disease Type")
    resp = fetch(session, "https://disease-api-roland.herokuapp.com/disease_type/all")
    st.dataframe(resp)

def doctor():
    email = ""
    st.markdown("# Doctor")
    st.sidebar.markdown("# Doctor")
    resp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/all")
    print(type(resp))

    df = pd.DataFrame.from_records(resp)

    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    options.configure_selection("single")

    grid_return = AgGrid(df, gridOptions=options.build())
    # print(grid_return)
    if len(grid_return['selected_rows']) > 0:
        email = grid_return['selected_rows'][0]["email"]

    selected_box = crud_box()
    if selected_box == "Create":    
        form = st.form("Create Doctor")
        email = form.text_input(label='Email')
        name = form.text_input(label='Name')
        surname = form.text_input(label='Surname')
        salary = form.number_input(label='Salary')
        phone = form.text_input(label='Phone')
        cname = form.text_input(label='Country')
        degree = form.text_input(label='Degree')
        id = form.number_input(label='Disease ID')
        submit_button = form.form_submit_button(label='Submit')
        if submit_button:
            d = Doctor(email, name, surname, int(salary), phone, cname, degree, int(id))
            createDoctorResp = post("https://disease-api-roland.herokuapp.com/doctor/create", d.__dict__), 
            print(createDoctorResp)
            resp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/all")
    elif selected_box == "Read":
        form = st.form("Read Doctor")
        email = form.text_input(label='Email')
        submit = form.form_submit_button()

        if submit:
            getDoctorResp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/" + email)
            st.json(getDoctorResp)

    elif selected_box == "Update" and email != "":
        getDoctorResp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/" + email)
        
        form = st.form("Update Doctor")
        email = form.text_input(label='Email', value=getDoctorResp['email'])
        name = form.text_input(label='Name', value=getDoctorResp['name'])
        surname = form.text_input(label='Surname', value=getDoctorResp['surname'])
        salary = form.number_input(label='Salary', value=getDoctorResp['salary'])
        phone = form.text_input(label='Phone', value=getDoctorResp['phone'])
        cname = form.text_input(label='Country', value=getDoctorResp['cname'])
        degree = form.text_input(label='Degree', value=getDoctorResp['degree'])
        id = form.number_input(label='Disease ID', value = getDoctorResp['id'])
        submit_button = form.form_submit_button(label='Submit')

        if submit_button:
            d = Doctor(email, name, surname, int(salary), phone, cname, degree, int(id))
            updateDoctorResp= put("https://disease-api-roland.herokuapp.com/doctor/" + str(d.email), d.__dict__), 
            print(updateDoctorResp)
            resp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/all")
    elif selected_box == "Delete" and email != "":
        getDoctorResp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/" + email)
        
        form = st.form("Delete Doctor")
        submit_button = form.form_submit_button(label='Delete')

        if submit_button:
            deleteDoctorResp= delete("https://disease-api-roland.herokuapp.com/doctor/" + str(email)), 
            print(deleteDoctorResp)
            resp = fetch(session, "https://disease-api-roland.herokuapp.com/doctor/all")


        st.snow()

def public_servant():
    st.markdown("# Public Servant")
    st.sidebar.markdown("# Public Servant")
    resp = fetch(session, "https://disease-api-roland.herokuapp.com/public_servant/all")
    st.dataframe(resp)

def country():
    st.markdown("# Country")
    st.sidebar.markdown("# Country")
    resp = fetch(session, "https://disease-api-roland.herokuapp.com/country/all")
    st.dataframe(resp)

def record():
    st.markdown("# Record")
    st.sidebar.markdown("# Record")
    resp = fetch(session, "https://disease-api-roland.herokuapp.com/record/filter")
    st.dataframe(resp)

page_names_to_funcs = {
    "Main Page": main_page,
    "Disease": disease,
    "Disease Type": disease_type,
    "Doctor": doctor,
    "Public Servant": public_servant,
    "Country": country,
    "Record": record
}

def main():
    selected_page = st.sidebar.selectbox(
        "Choose table",
        page_names_to_funcs.keys()
    )
    page_names_to_funcs[selected_page]()



if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())