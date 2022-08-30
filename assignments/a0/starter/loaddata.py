from __future__ import annotations
from typing import List, Tuple, TypeVar
import hospital
import csv
import datetime


def load_doctors(hosp: Hospital, file_name: str) -> None:
    """
    Updates <hosp> doctors attribute to include doctors from <file_name>.

    <file_name> is a csv with lines that look like:
        99064054,Brian Hazlett,1070.33
        id-number,First-name Last-name,salary-per-day
    """
    # Name, ID, and salary
    doctors = list()
    with open(file_name, 'r') as file:
        for row in csv.reader(file, delimiter=','):
            id_number, name, salary = row
            id_number = int(id_number)
            salary = float(salary)

            new_doctor = hospital.Doctor(name, id_number, salary)
            doctors.append(new_doctor)

    for doc in doctors:
        hosp.hire_doctor(doc)


def load_patients(hosp: Hospital, file_name: str) -> None:
    """
    Updates <hosp> patients attribute to include patients from <file_name>.

    <file_name> is a csv with lines that look like:
        44276583,Amalia Box
        id-number,First-name Last-name
    """
    patients = list()
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            patient_id, patient_name = row
            patients.append(hospital.Patient(patient_name, int(patient_id)))

    for pat in patients:
        hosp.admit_patient(pat)


def load_admissions(hosp: Hospital, file_name: str) -> None:
    """
    Reads admissions data from <file_name> into Hospital <hosp>.

    <file_name> is a csv file with HospitalVisit records of this format:
         visit date, doctor id, patient id, diagnosis, prognosis, drug, followup
    For instance:
         04/20/2017, 99722708, 44398694, Cold, poor, Advil, 2.5, 04/29/2017
    """
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            # Sample:
            # 04/20/2017, 99722708, 44398694, Cold, poor, Advil, 2.5, 04/29/2017
            intake, dr_id, patient_id, diagnosis = row[:4]
            prognosis, prescribed, followup = row[4:]
            intake = datetime.datetime.strptime(intake, '%m/%d/%Y').date()

            if followup != "None":
                followup = datetime.datetime.\
                    strptime(followup, '%m/%d/%Y').date()
            else:
                followup = None

            hosp_visit = hospital.HospitalVisit(
                intake,
                int(dr_id),
                int(patient_id),
                diagnosis,
                prognosis,
                prescribed,
                followup
            )

            hosp.admissions[intake].append(hosp_visit)

    # Use admissions to load patient history.
    id_to_object = {patient.id: patient for patient in hosp.patients}

    for date in hosp.admissions.keys():  # for every day of year
        for visit in hosp.admissions[date]:
            id_to_object[visit.patient_id].history.append(visit)


def load_attendance(hosp: Hospital, file_name: str) -> None:
    """
    Reads the attendance record into <hosp> from <file_name>.
    """
    with open(file_name, 'r') as file:
        # File looks like: MO/DA/YEAR,Doctor Name,Doctor Name,...
        for line in file:
            line = line[:-1].split(",")  # remove a newline
            month, day, year = map(int, line[0].split("/"))
            doctors = line[1:]
            hosp.attendance[datetime.date(year, month, day)] = doctors


def read_hospital(hosp: Hospital, path: str) -> None:
    """
    Updates <hosp> in place from files inside a <path> containing
        1/  admissions.csv
        2/  attendance.dat
        3/  doctors.csv
        4/  patients.csv
        5/  schedule.dat
    with the appropriate data formatting.
    """

    # load and setup doctors (with empty schedule)
    hosp.load_doctors(path + 'doctors.csv')

    # load and setup patients (with empty visits)
    hosp.load_patients(path + 'patients.csv')

    # LOADS MUST BE DONE IN THIS ORDER
    hosp.load_attendance(path + 'attendance.dat')
    hosp.load_admissions(path + 'admissions.csv')
    hosp.load_schedules(path + 'schedule.dat')
