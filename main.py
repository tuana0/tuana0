import customtkinter
import mysql.connector
from mysql.connector import Date, Time
from werkzeug.security import generate_password_hash, check_password_hash

from tkinter import Listbox

import mysql.connector
from werkzeug.security import check_password_hash


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database",
    database="healthcare"
)

mycursor = mydb.cursor()

# users tablosundan verileri çek
mycursor.execute("SELECT user_id, password FROM users")

user_credentials = {}
for (usersid, password) in mycursor:
    user_credentials[usersid] = password


def get_available_times():
    query = "SELECT event_date_time FROM tıme"
    cursor = mydb.cursor()
    cursor.execute(query)
    times = cursor.fetchall()
    cursor.close()
    return [time[0].strftime("%Y-%m-%d %H:%M:%S") if time[0] is not None else 'N/A' for time in times]
 # event_date_time formatını stringe çeviriyoruz


def get_medical_records(patient_id):
    query = "SELECT patient_id, record_id,disease,drugs, date_of_examination FROM healthcare.patient_medical_records WHERE patient_id = %s"
    cursor = mydb.cursor()
    cursor.execute(query, (patient_id,))
    patients = cursor.fetchall()
    cursor.close()
    return patients


def get_patients(doctor_id):
    query = "SELECT Doctor_id,Patient_Id,Name FROM healthcare.doctor_patient_info WHERE Doctor_id = %s"
    cursor = mydb.cursor()
    cursor.execute(query, (doctor_id,))
    patients = cursor.fetchall()
    cursor.close()
    return patients



def get_doctors(hospital_id):
    query = "SELECT Doctor_id, F_name, Specialization FROM healthcare.doctor WHERE hospital_id = %s"
    cursor = mydb.cursor()
    cursor.execute(query, (hospital_id,))
    doctors = cursor.fetchall()
    cursor.close()
    return doctors



def get_doctor():
    query = "SELECT * FROM doctor"
    cursor = mydb.cursor()
    cursor.execute(query)
    doctors = cursor.fetchall()
    cursor.close()
    return doctors


def get_appointments(doctor_id):
    query = "SELECT * FROM healthcare.doctor_patient_info WHERE Doctor_id = %s"
    cursor = mydb.cursor()
    cursor.execute(query, (doctor_id,))
    patients = cursor.fetchall()
    cursor.close()
    return patients

def get_appointment(patient_id):
    query = "SELECT hospital_name, appointment_date_time, doctor_name FROM healthcare.patient_appointments WHERE " \
            "patient_id = %s "

    #doktor ismi view oluştururkne concat ile birleştirilebilir mi
    cursor = mydb.cursor()
    cursor.execute(query, (patient_id,))
    patients = cursor.fetchall()
    cursor.close()
    return patients

def get_hospitals():
    query = "SELECT * FROM hospital"
    cursor = mydb.cursor()
    cursor.execute(query)
    hospitals = cursor.fetchall()
    cursor.close()
    return hospitals


def get_patient(hospital_id):
    query = "SELECT DISTINCT hospital_id,patient_name,Id FROM healthcare.hospital_overview WHERE hospital_id = %s"
    cursor = mydb.cursor()
    cursor.execute(query, (hospital_id,))
    patients = cursor.fetchall()
    cursor.close()
    return patients


def get_appointment_hospital(hospital_id):
    query = "SELECT * FROM healthcare.hospital_overview WHERE hospital_id = %s"


    #doktor ismi view oluştururkne concat ile birleştirilebilir mi
    cursor = mydb.cursor()
    cursor.execute(query, (hospital_id,))
    hospitals= cursor.fetchall()
    cursor.close()
    return hospitals


def get_data(option, user_id=None,):
    if option == "My Medical Record":
        return get_medical_records(user_id)
    elif option == "My Patient List":
        return get_patients(user_id)
    elif option == "Doctor List":
        return get_doctors(user_id)
    elif option == "Appointment List":
        return get_appointments(user_id)
    elif option == "Show My Appointment List":
        return get_appointment(user_id)
    elif option == "Hospital":
        return get_hospitals()
    elif option == "Patient List":
        return get_patient(user_id)
    elif option == "Hospital Appointment List":
        return get_appointment_hospital(user_id)
    else:
        return []


def display_data(option, previous_page, user_id=None):
    data = get_data(option, user_id)
    open_data_display_page(data, previous_page)

def insert_medical_record(Record_Id, Patient_Id, Doctor_id, Date_of_Examination, Drugs, Diseases):
    query = "INSERT INTO medical_record (Record_Id, Patient_Id, Doctor_id, Date_of_Examination, Drugs, Diseases) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (Record_Id, Patient_Id, Doctor_id, Date_of_Examination, Drugs, Diseases)
    cursor = mydb.cursor()
    cursor.execute(query, values)
    mydb.commit()
    cursor.close()


def open_medical_record_form():
    form = customtkinter.CTkToplevel()
    form.geometry(f"{int(400 * SCALE_FACTOR)}x{int(300 * SCALE_FACTOR)}")
    form.title("Fill a Medical Record")

    doctor_id_entry = customtkinter.CTkEntry(master=form, placeholder_text="Doctor ID")
    doctor_id_entry.pack(pady=10)

    record_id_entry = customtkinter.CTkEntry(master=form, placeholder_text="Record ID")
    record_id_entry.pack(pady=10)

    drugs_entry = customtkinter.CTkEntry(master=form, placeholder_text="Drugs")
    drugs_entry.pack(pady=10)

    disease_entry = customtkinter.CTkEntry(master=form, placeholder_text="Diseases")
    disease_entry.pack(pady=10)

    date_of_examination_entry = customtkinter.CTkEntry(master=form, placeholder_text="Date of Examination (YYYY-MM-DD)")
    date_of_examination_entry.pack(pady=10)

    patient_id_entry = customtkinter.CTkEntry(master=form, placeholder_text="Patient ID")
    patient_id_entry.pack(pady=10)

    submit_button = customtkinter.CTkButton(master=form, text="Submit", command=lambda: insert_medical_record(
        record_id_entry.get(),
        patient_id_entry.get(),
        doctor_id_entry.get(),
        date_of_examination_entry.get(),
        drugs_entry.get(),
        disease_entry.get()
    ))
    submit_button.pack(pady=20)

    form.mainloop()


"""def display_data(option):
    data = get_data(option)
    for record in data:
        print(record)"""  # konsola yazdırma işlemi

""""""


def insert_appointment(doctor_name, hospital_name, patient_id, selected_datetime):
    cursor = mydb.cursor()

    # Doktorun bilgilerini bulalım
    cursor.execute("SELECT Doctor_id, Room, Specialization FROM doctor WHERE F_name = %s", (doctor_name,))
    doctor_info = cursor.fetchone()

    # Hastanenin bilgilerini bulalım
    cursor.execute("SELECT contact_info, address FROM hospital WHERE hospital_name = %s", (hospital_name,))
    hospital_info = cursor.fetchone()

    if doctor_info and hospital_info:
        doctor_id, doctor_room, specialization = doctor_info
        contact_info, address = hospital_info

        # Appointment tablosuna veriyi ekleme
        date, time = selected_datetime.split()  # selected_datetime'i tarih ve saat olarak ayırıyoruz
        query = """INSERT INTO appointment 
                   (Doctor_id, HospitalName, Patient_Id,event_date_time, DoctorRoom, Specialization, ContactInfo, Adress) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
        doctor_id, hospital_name, patient_id, selected_datetime, doctor_room, specialization, contact_info, address)
        cursor.execute(query, values)
        mydb.commit()

    cursor.close()


def open_appointment_form():
    form = customtkinter.CTkToplevel()
    form.geometry(f"{int(600 * SCALE_FACTOR)}x{int(300 * SCALE_FACTOR)}")
    form.title("Create an Appointment")

    # Fetch doctors and hospitals from the database
    doctors = get_doctor()
    hospitals = get_hospitals()

    # Add doctor names and hospital names to lists
    doctor_names = [doctor[1] for doctor in
                    doctors]  # Doctor names, the second column in the doctor table should be the doctor name by default
    hospital_names = [hospital[1] for hospital in
                      hospitals]  # Hospital names, the second column in the hospital table should be the hospital name by default

    doctor_name_label = customtkinter.CTkLabel(master=form, text="Doctor Name:")
    doctor_name_label.pack(pady=10)

    # Display doctor names in a ComboBox
    doctor_name_combobox = ttk.Combobox(master=form, values=doctor_names)
    doctor_name_combobox.pack(pady=5)

    hospital_name_label = customtkinter.CTkLabel(master=form, text="Hospital Name:")
    hospital_name_label.pack(pady=10)

    # Display hospital names in a ComboBox
    hospital_name_combobox = ttk.Combobox(master=form, values=hospital_names)
    hospital_name_combobox.pack(pady=5)

    # Select Date and Time ComboBox
    select_date_label = customtkinter.CTkLabel(master=form, text="Select Date and Time :")
    select_date_label.pack(pady=10)

    available_times = get_available_times()
    select_date_combobox = ttk.Combobox(master=form, values=available_times)
    select_date_combobox.pack(pady=5)

    patient_id_entry = customtkinter.CTkEntry(master=form, placeholder_text="Patient ID")
    patient_id_entry.pack(pady=10)

    submit_button = customtkinter.CTkButton(master=form, text="Submit", command=lambda: insert_appointment(
        doctor_name_combobox.get(),
        hospital_name_combobox.get(),
        patient_id_entry.get(),
        select_date_combobox.get()  # Pass the selected date and time
    ))
    submit_button.pack(pady=20)

    form.mainloop()


def userlogin(username, password, user_role, login_page):
    if username.lower() in user_credentials and user_credentials[username.lower()] == password:
        login_page.withdraw()  # Hide the login page
        open_main_panel(username, user_role, username.lower(), login_page)
    else:
        print("Invalid username or password")



SCALE_FACTOR = 1.5


def open_main_panel(username, user_role, user_id, previous_page=None):
    main_panel = customtkinter.CTkToplevel()
    main_panel.geometry(f"{int(600 * SCALE_FACTOR)}x{int(400 * SCALE_FACTOR)}")
    main_panel.title("Health is the greatest wealth")

    welcome_label = customtkinter.CTkLabel(master=main_panel, text=f"Welcome {username}",
                                           font=("Roboto", int(18 * SCALE_FACTOR)))
    welcome_label.pack(pady=20 * SCALE_FACTOR)

    if user_role == "Doctor":
        buttons_text = ["Appointment List", "Fill a Medical Record", "My Patient List"]
    elif user_role == "Patient":
        buttons_text = ["Create an Appointment", "Show My Appointment List", "My Medical Record"]
    elif user_role == "Hospital":
        buttons_text = ["Patient List", "Hospital Appointment List", "Doctor List"]

    for text in buttons_text:
        if text == "Fill a Medical Record":
            button = customtkinter.CTkButton(master=main_panel, text=text, height=int(40 * SCALE_FACTOR),
                                             width=int(200 * SCALE_FACTOR), corner_radius=int(10 * SCALE_FACTOR),
                                             command=open_medical_record_form)
        elif text == "Create an Appointment":
            button = customtkinter.CTkButton(master=main_panel, text=text, height=int(40 * SCALE_FACTOR),
                                             width=int(200 * SCALE_FACTOR), corner_radius=int(10 * SCALE_FACTOR),
                                             command=open_appointment_form)
        else:
            button = customtkinter.CTkButton(master=main_panel, text=text, height=int(40 * SCALE_FACTOR),
                                             width=int(200 * SCALE_FACTOR), corner_radius=int(10 * SCALE_FACTOR),
                                             command=lambda t=text: display_data(t, main_panel, user_id))
        button.pack(pady=10 * SCALE_FACTOR)

    if previous_page is not None:
        back_button = customtkinter.CTkButton(master=main_panel, text="Back", command=lambda: [main_panel.destroy(),
                                                                                               previous_page.deiconify()])  # Show the previous page
        back_button.pack(pady=10)

    main_panel.mainloop()



def open_login_page(user_role, root, previous_page=None):
    root.withdraw()  # Hide the main login page
    login_page = customtkinter.CTkToplevel()
    login_page.geometry(f"{int(400 * SCALE_FACTOR)}x{int(300 * SCALE_FACTOR)}")
    login_page.title(f"{user_role} Login Page")

    label = customtkinter.CTkLabel(master=login_page, text=f"{user_role} Login",
                                   font=("Roboto", int(18 * SCALE_FACTOR)))
    label.pack(pady=20 * SCALE_FACTOR)

    username_entry = customtkinter.CTkEntry(master=login_page, placeholder_text="Username")
    username_entry.pack(pady=10)

    password_entry = customtkinter.CTkEntry(master=login_page, placeholder_text="Password", show="*")
    password_entry.pack(pady=10)

    login_button = customtkinter.CTkButton(master=login_page, text="Login",
                                           command=lambda: userlogin(username_entry.get(), password_entry.get(),
                                                                     user_role, login_page))
    login_button.pack(pady=20)

    # Add a "Back" button
    back_button = customtkinter.CTkButton(master=login_page, text="Back", command=lambda: [login_page.destroy(),
                                                                                           root.deiconify()])  # Show the main login page
    back_button.pack(pady=10)

    login_page.mainloop()


from tkinter import ttk
from tkinter import PhotoImage

from tkinter import Canvas, PhotoImage
from tkinter.ttk import Treeview

from tkinter import ttk, Canvas, PhotoImage, PanedWindow
import customtkinter

SCALE_FACTOR = 1.5


def open_data_display_page(data, previous_page):
    previous_page.withdraw()  # Hide the previous page
    data_display_page = customtkinter.CTkToplevel()
    data_display_page.geometry(f"{int(600 * SCALE_FACTOR)}x{int(400 * SCALE_FACTOR)}")
    data_display_page.title("Data Display")

    paned_window = PanedWindow(data_display_page, orient="vertical")
    paned_window.pack(fill="both", expand=True)

    # Create a Treeview widget inside the paned_window
    tree = ttk.Treeview(paned_window)

    # Assuming that data is a list of tuples, where each tuple represents a row
    if data:
        # Create columns
        tree["columns"] = [f"column{i}" for i in range(len(data[0]))]

        # Define column
        for i in range(len(data[0])):
            tree.column(f"column{i}", width=int(100 * SCALE_FACTOR))

        # Define headings
        for i in range(len(data[0])):
            tree.heading(f"column{i}", text=f"Column {i}")

        # Insert data
        for row in data:
            tree.insert('', 'end', values=row)

    # Create a Canvas widget inside the paned_window
    canvas = Canvas(paned_window)
    image = PhotoImage(file="Healthcare database system (1).png")
    canvas.create_image(0, 0, image=image, anchor="nw")

    paned_window.add(tree)
    paned_window.add(canvas)

    back_button = customtkinter.CTkButton(master=data_display_page, text="Back",
                                          command=lambda: [data_display_page.destroy(),
                                                           previous_page.deiconify()])  # Show the previous page
    back_button.pack(pady=10)

    data_display_page.mainloop()





# BURDA YANLIŞ YOK
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("500x500")
root.title("Healthcare Login System")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=30, padx=90, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Healthcare Login System", font=("Roboto", 24))
label.pack(pady=24, padx=20)

doctor_login_button = customtkinter.CTkButton(master=frame, text="Doctor Login",
                                              command=lambda: open_login_page("Doctor", root))
doctor_login_button.pack(pady=10)

patient_login_button = customtkinter.CTkButton(master=frame, text="Patient Login",
                                               command=lambda: open_login_page("Patient", root))
patient_login_button.pack(pady=10)

hospital_login_button = customtkinter.CTkButton(master=frame, text="Hospital Login",
                                                command=lambda: open_login_page("Hospital", root))
hospital_login_button.pack(pady=10)

root.mainloop()
