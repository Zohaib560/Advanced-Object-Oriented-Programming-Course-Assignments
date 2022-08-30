"""
Assignment 0 solution
CSC148, Winter 2020
Michael Liut, Bogdan Simion, and Paul Vrbik.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik, Dan Zingaro
"""

from __future__ import annotations
from typing import List, Tuple, Dict
from collections import defaultdict
import datetime
import loaddata

MONTH_ABBREV = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec']

ABBREV_TO_NUMBER = {month: k + 1 for k, month in enumerate(MONTH_ABBREV)}


class HospitalVisit:
    """An object for storing the medical history for a single visit of a
    patient to a hospital.

    Public Attributes
    =================
    date: The date of the visit.
    doctor_id: The identification number of the doctor who delivered care
        during this visit.
    patient_id: The identification number for the patient associated with this
        visit.
    diagnosis: A human-readable string of the diagnosis (assigned ailment) of
        this patient.
    prognosis: A human-readable string of the prognosis (assigned outcome) by
        the doctor for this patient.
    prescribed: A human-readable string of the medication prescribed during
        this visit.
    followup_date: A date for followup for this patient or None.

    Representation Invariants
    =========================
    - not followup_date or date <= followup_date

    Sample Usage
    ============
    >>> visit = HospitalVisit(\
                datetime.date(2017, 10, 23),\
                99722708,\
                44123123,\
                "Dengue Fever",\
                "very poor",\
                "Sucralfate",\
                datetime.date(2017, 11, 30)\
    )
    >>> visit.doctor_id
    99722708
    >>> visit.patient_id
    44123123
    """

    date: datetime.date
    doctor_id: int
    patient_id: int
    diagnosis: str
    prognosis: str
    prescribed: str
    followup_date: datetime.date

    def __init__(self, date: datetime.date, doctor_id: int, patient_id: int,
                 diagnosis: str, prognosis: str, prescribed: str,
                 followup: datetime) -> None:
        """Initialize this HospitalVisit.
        """
        self.date = date
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.prognosis = prognosis
        self.prescribed = prescribed
        self.followup_date = followup

    def __repr__(self) -> str:
        """Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "{}, {}, {}".format(self.date, self.doctor_id, self.patient_id)

    def __eq__(self, other: HospitalVisit) -> bool:
        """Return True if this HospitalVisit is equal to <other>.
        Hospital visits are equal when their
            date, doctor_id, and patient_id
        attributes are equal.

        Each of these triplets is unique as it is presumed Doctors cannot
        see the same patient twice in one day.
        """
        return (self.date, self.doctor_id, self.patient_id) == \
               (other.date, other.doctor_id, other.patient_id)


class Doctor:
    """An object for storing employment data for a medical doctor.

    Public Attributes
    =================
    name: The name of this doctor in the form 'Firstname Lastname'
    id: A unique integer identification number.
    salary: How much this doctor is paid to work one day.
    schedule: A dictionary object mapping as keys the month abbreviations
        'Jan', ..., 'Dec' to a list of datetime objects representing the days
        when this doctor works in each corresponding month.

    Sample Usage
    ============

    >>> bob = Doctor("Bob Loot", 98765432, 1079.80)
    >>> bob.schedule['Jan'].append(datetime.date(2017, 10, 23))
    >>> bob.schedule['Jan'].append(datetime.date(2017, 10, 24))
    >>> bob.schedule['Jan']
    [datetime.date(2017, 10, 23), datetime.date(2017, 10, 24)]
    >>> bob.schedule['Feb']
    []
    """

    name: str
    id: int
    salary: float
    schedule: Dict[str, List[datetime]]

    def __init__(self, name: str, id_num: int, salary: float) -> None:
        """ Initialize this Doctor with name <name>, identification number
        <id_num>, and salary <salary>.
        """
        self.name = name
        self.id = id_num
        self.salary = salary
        self.schedule = {month_abbrev: [] for month_abbrev in MONTH_ABBREV}

    def __repr__(self) -> str:
        """ Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "Did: {}".format(self.id)

    def __eq__(self, other: Doctor) -> bool:
        """ Return True if this Doctor is equal to <other>.
        Two doctors are equal when their (unique) ids are equal.
        """
        return self.id == other.id


class Patient:
    """An object for storing medical history for a patient.

    Public Attributes
    =================
    name: The name of this patient in the form 'Firstname Lastname'
    id: A unique identification number.
    history: A list of HospitalVisit entries when this patient visited the
        hospital.

    Sample Usage
    ============
    >>> carol = Patient("Carol Loot", 44021721)
    >>> carol.id
    44021721
    """

    name: str
    id: int
    history: List[HospitalVisit]

    def __init__(self, name: str, id_num: int) -> None:
        """ Initialize this Patient with name <name> and identification number
        <id_num>.
        """
        self.name = name
        self.id = id_num
        self.history = []

    def __repr__(self) -> str:
        """ Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "Pid: {}".format(self.id)

    def __eq__(self, other: Patient) -> bool:
        """ Return True if this Patient is equal to <other>.
        Two patients are equal when their (unique) ids are equal.
        """
        return self.id == other.id

    def is_prescribed(self, medication: str) -> bool:
        """
        Return True only when this Patient has been prescribed <medication>
        during a hospital visit.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visit = HospitalVisit(\
            datetime.date(2017, 10, 23),\
            99722708,\
            44123123,\
            "Dengue Fever",\
            "very poor",\
            "Sucralfate",\
            datetime.date(2017, 11, 30)\
        )
        >>> carol.history.append(visit)
        >>> carol.is_prescribed("Sucralfate")
        True
        >>> carol.is_prescribed("Lithium")
        False
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> hosp.patients[0].is_prescribed("Propofol")
        True
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> hosp.patients[3].is_prescribed("Propofol")
        True
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def followups(self, month: str) -> List[datetime]:
        """ Return a list of days (i.e. datetime objects) when patient
        has followups during the month <month>.
        The <month> is represented using the abbreviations: {'Jan',...,'Dec'}.

        No particular list order is required.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visit = HospitalVisit(\
            datetime.date(2017, 10, 23),\
            99722708,\
            44021721,\
            "Dengue Fever",\
            "very poor",\
            "Sucralfate",\
            datetime.date(2017, 11, 30)\
        )
        >>> carol.history.append(visit)
        >>> carol.followups('Nov')
        [datetime.date(2017, 11, 30)]
        >>> carol.followups('Aug')
        []
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> hosp.patients[0].followups('Feb')
        [datetime.date(2017, 2, 6)]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> hosp.patients[1].followups('Sep')
        [datetime.date(1997, 9, 26), datetime.date(1997, 9, 11)]
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def prescribed_after(self, date: datetime.date) -> List[str]:
        """Return the list of medications (strings) prescribed after (inclusive)
        <date>.

        This list may include duplicates if a medication is prescribed during
        multiple visits.  No particular list order is required.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visit = HospitalVisit(\
            datetime.date(2017, 10, 23),\
            99722708,\
            44021721,\
            "Dengue Fever",\
            "very poor",\
            "Sucralfate",\
            datetime.date(2017, 11, 30)\
        )
        >>> carol.history.append(visit)
        >>> carol.prescribed_after(datetime.date(2017, 10, 22),)
        ['Sucralfate']
        >>> carol.prescribed_after(datetime.date(2017, 12, 1))
        []
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> hosp.patients[0].prescribed_after(datetime.date(1900,1,1))
        ['Amiodarone HCl', 'Propofol']
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> hosp.patients[0].prescribed_after(datetime.date(1900,1,1)) \
            #doctest: +NORMALIZE_WHITESPACE
        ['Miconazole Powder', 'Acetaminophen', 'Sucralfate', 'sodium bicarb',
         'Hydrochlorothiazide']
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def missed_followups(self) -> Tuple[int, int]:
        """ Return the number of missed and kept followups for this Patient.

        >>> carol = Patient("Carol Loot", 44021721)
        >>> visits = []
        >>> visits.append(HospitalVisit(\
                datetime.date(2017, 10, 23),\
                99722708,\
                44021721,\
                "Dengue Fever",\
                "very poor",\
                "Sucralfate",\
                datetime.date(2017, 11, 30)\
            ))
        >>> visits.append(HospitalVisit(\
                datetime.date(2017, 11, 30),\
                99722708,\
                44021721,\
                "Dengue Fever",\
                "very poor",\
                "Sucralfate",\
                datetime.date(2017, 12, 2)\
            ))
        >>> carol.history.extend(visits)
        >>> carol.missed_followups()
        (1, 1)
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/janonly/")
        >>> hosp.patients[3].missed_followups()
        (1, 0)
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, "data/year97/")
        >>> hosp.patients[66].missed_followups()
        (10, 2)
        """

        # ===== #
        # TO DO #
        # ===== #

        pass


class Hospital:
    """ An object for modelling the daily operation of a hospital with doctors
    and patients.

    Public Attributes
    =================
    address: A human readable hospital's address.
    doctors: Doctors working at this hospital.
    patients: Patients who have visited this hospital.
    attendance: A daily record of doctors who showed up for work.
    admissions: A daily record of hospital visits to the hospital.
    load_schedules: Updates doctors schedules from a file.
    load_admissions: Update admissions from a file.
    load_attendance: Updates attendance from a file.

    Sample Usage
    ============
    >>> hosp = Hospital('123 Fake St.')
    >>> hosp.address
    '123 Fake St.'
    """

    address: str
    doctors: List[Doctor]
    patients: List[Patient]
    attendance: Dict[datetime, List[str]]
    admissions: Dict[datetime, List[HospitalVisit]]


    def __init__(self, address: str) -> None:
        """ Create a new Hospital with the given parameters."""
        self.address = address

        self.doctors = []
        self.patients = []

        self.attendance = {}
        self.admissions = defaultdict(lambda: [])

    def __repr__(self) -> str:
        """ Return a human-readable representation of this object.
        Do not modify this! This is not to be used to reconstruct the object.
        """
        return "Hospital on "+self.address

    def load_doctors(self, file_name: str) -> None:
        """
        Update this Hospital's doctors attribute to include the doctors from the
        file <file_name>.

        <file_name> is a csv with lines that look like:
            99064054,Brian Hazlett,1070.33
            id-number,First-name Last-name,salary-per-day

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        """
        return loaddata.load_doctors(self, file_name)

    def load_patients(self, file_name: str) -> None:
        """
        Update this Hospital's patients attribute to include the patients from
        the file <file_name>.

        <file_name> is a csv where each line has the following format:
            id-number,First-name Last-name,salary-per-day
        For instance:
            99064054,Brian Hazlett,1070.33

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_patients("data/year97/patients.csv")
        """
        return loaddata.load_patients(self, file_name)

    def load_schedules(self, file_name: str) -> None:
        """
        Update the schedules for all the doctors from this Hospital, using the
        dates specified in the file <file_name>.

        The content of <file_name> has the following format:
            Firstname Lastname
            MM/DD/YYYY

        That is, <first name> <last name> followed by a NON-EMPTY sequence of
        dates in the form MM/DD/YYYY, followed by an empty line after each
        doctor's schedule dates.

        For instance:
            Alice Liddle
            01/22/2017
            03/19/2017

            Mikhail Varshavski
            01/23/2017
            04/03/2018

        Names and schedules that do not correspond to doctors from self.doctors
        are ignored. Otherwise, those doctors' schedule attributes are updated.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        >>> hosp.load_schedules("data/year97/schedule.dat")
        """

        # ======================
        # TO DO : DO THIS FIRST
        # ======================

        x = True  # checks if the date is not associated with a doctor
        curr_doc = ''  # may or may not need this
        with open(file_name, 'r') as file:
            for line in file:
                info = line.strip()
                if x:
                    for doc in self.doctors:
                        if doc.name == info:
                            curr_doc = doc
                            x = False
                if line != '':
                    month, day, year = info.split(',')
                    month, day, year = int(month), int(day), int(year)
                    # force convert month, day, year to int
                    curr_doc.schedule[MONTH_ABBREV[month - 1]].append(
                        datetime.date(year, month, day))
                elif line == '':
                    x = True
        return None

    def load_attendance(self, file_name: str) -> None:
        """
        Update the attendance records for this Hospital from <file_name>, a csv
        file.

        Lines of <file_name> have the following format:
            DD/MM/YYYY,firstname lastname,firstname lastname,...
        For example:
            01/08/2019,Alice Liddle,Bob Loot
            02/08/2019,Carol Bitter
        which indicates that on 01/08/2019, Dr. Alice Liddle and Dr. Bob Loot
        showed up for work, and on 02/08/2019 only Dr. Carol Bitter was working
        at the hospital on that day.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        >>> hosp.load_attendance("data/year97/attendance.dat")
        """
        loaddata.load_attendance(self, file_name)

    def load_admissions(self, file_name: str) -> None:
        """
        Update this Hospital and patient visits with dates from <file_name>, a
        csv with lines
         visit date, doctor id, patient id, diagnosis, prognosis, drug, followup
        where intake and followup are dates in the form MM/DD/YYYY.

        NOTE: This also updates the patients' visit history.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> hosp.load_doctors("data/year97/doctors.csv")
        >>> hosp.load_patients("data/year97/patients.csv")
        >>> hosp.load_admissions("data/year97/admissions.csv")
        """
        loaddata.load_admissions(self, file_name)

    def admit_patient(self, patient: Patient) -> None:
        """
        Add the <patient> to this Hospital's list of patients.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> carol = Patient("Carol Loot", 44021721)
        >>> hosp.admit_patient(carol)
        >>> hosp.patients
        [Pid: 44021721]
        """
        self.patients.append(patient)

    def hire_doctor(self, doctor: Doctor) -> None:
        """
        Add the <doctor> to this Hospital's list of doctors.

        >>> hosp = Hospital("123 Welks Rd, Letterkenny ON, K0J-2E0, Canada")
        >>> bob = Doctor("Bob Loot", 99021721, 1.0)
        >>> hosp.hire_doctor(bob)
        >>> hosp.doctors
        [Did: 99021721]
        """
        self.doctors.append(doctor)

    def projected_expenses(self) -> float:
        """
        Return the total expenses projected based on doctor schedules
        (not actual attendance!) and their daily pay.
        Namely:
        (number of days when the doctor is scheduled to work) * (daily salary)

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> round(hosp.projected_expenses(), 0)
        38630.0
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> round(hosp.projected_expenses(), 0)
        622622.0
        """

        # ===== #
        # TO DO #
        # ===== #

        expenses = 0.0
        for doc in self.doctors:
            wage = doc.salary
            work_days = 0
            for month in doc.schedule:
                work_days += len(doc.schedule[month])
            expenses += work_days * wage
        return expenses

    def actual_expenses(self) -> float:
        """
        Return the total cost of paying doctors for all the shifts they worked.
        That is to say, the cost of paying doctors according to the attendance
        rather than their schedules.

        Namely: return (number of days the doctor attended) * (daily salary)

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> hosp.actual_expenses()
        36851.56
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> hosp.actual_expenses()
        623485.81
        """

        # ===== #
        # TO DO #
        # ===== #
        expenses = 0.0
        for doc in self.doctors:
            wage = doc.salary
            days_worked = 0
            for date in self.attendance:
                if doc.name in self.attendance[date]:
                    days_worked += 1
            expenses += days_worked * wage
        return expenses

    def reminders(self, date: datetime.date, delta: int) -> List[Patient]:
        """
        Return a list of patients that have follow-up days scheduled within
        <delta>-days of <date>.

        For instance: Wednesday and Thursday are within 2-days from Tuesday.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> hosp.reminders(datetime.date(2017,1,1), 20)
        [Pid: 44276583, Pid: 44926521, Pid: 44077293]
        >>> hosp.reminders(datetime.date(2018,11,1), 300)
        []
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> hosp.reminders(datetime.date(1997,10,17), 3)
        [Pid: 44065518, Pid: 44522886, Pid: 44228524, Pid: 44888118]
        """

        # ===== #
        # TO DO #
        # ===== #
        followup_list = []
        followup_date = date + datetime.timedelta(delta)
        for patient in self.patients:
            for visit in patient.history:
                if visit.followup_date <= followup_date:
                    followup_list.append(patient)
        return followup_list

    def patients_seen(self, doctor: Doctor, start_date: datetime.date,
                      end_date: datetime.date) -> int:
        """
        Return the NUMBER of unique patients who visited <doctor> during
        <start_date> to <end_date> (inclusive).

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> d1 = datetime.date(2017, 1, 1)
        >>> d2 = datetime.date(2017, 1, 31)
        >>> bob = hosp.doctors[0]
        >>> hosp.patients_seen(bob, d1, d2)
        1
        >>> alice = hosp.doctors[2]
        >>> hosp.patients_seen(alice, d1, d2)
        0
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> d1 = datetime.date(1997, 1, 1)
        >>> d2 = datetime.date(1997, 2, 1)
        >>> bob = hosp.doctors[0]
        >>> hosp.patients_seen(bob, d1, d2)
        5
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def busiest_doctors(self, start_date: datetime.date,
                        end_date: datetime.date) -> List[Doctor]:
        """
        Return the list of doctors (in any order) who have ATTENDED TO the most
        UNIQUE patients during <start_date> to <end_date> inclusive.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> d1 = datetime.date(2017, 1, 1)
        >>> d2 = datetime.date(2017, 1, 31)
        >>> hosp.busiest_doctors(d1, d2)
        [Did: 99262168]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> d1 = datetime.date(1997, 1, 1)
        >>> d2 = datetime.date(1997, 2, 1)
        >>> hosp.busiest_doctors(d1, d2)
        [Did: 99366005]
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def coverage(self, bob: Doctor, alice: Doctor) -> List[datetime]:
        """
        Return the dates where Dr <bob> covered for Dr <alice>.

        Definition (Covered):
        <bob> COVERED FOR <alice"> on day X if and only if
           1/  <bob> was not scheduled to work on day X, and
           2/  <bob> is on the attendance roll for day X, and
           3/  <alice> was sick on day X.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> bob = hosp.doctors[6]
        >>> alice = hosp.doctors[2]
        >>> hosp.coverage(bob, alice)
        [datetime.date(2017, 1, 28), datetime.date(2017, 1, 24)]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> bob = hosp.doctors[1]
        >>> alice = hosp.doctors[3]
        >>> hosp.coverage(bob, alice)
        [datetime.date(1997, 10, 17), datetime.date(1997, 11, 30)]
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def sick_days(self, doctor: Doctor) -> List[datetime]:
        """
        Return the days <doctor> was sick.

        Definition (Sick):
        <doctor> is SICK on a day X when
           1/  <doctor> is scheduled to work on day X, and
           2/  <doctor> is NOT on attendance roll.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> alice = hosp.doctors[0]
        >>> hosp.sick_days(alice)
        []
        >>> bob = hosp.doctors[1]
        >>> sorted(hosp.sick_days(bob))
        [datetime.date(2017, 1, 25), datetime.date(2017, 1, 26)]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> bob = hosp.doctors[0]
        >>> sorted(hosp.sick_days(bob)) #doctest: +NORMALIZE_WHITESPACE
        [datetime.date(1997, 1, 20), datetime.date(1997, 3, 13),
         datetime.date(1997, 5, 23), datetime.date(1997, 6, 13),
         datetime.date(1997, 6, 24), datetime.date(1997, 6, 25),
         datetime.date(1997, 9, 28), datetime.date(1997, 10, 1),
         datetime.date(1997, 10, 13), datetime.date(1997, 10, 29),
         datetime.date(1997, 12, 7)]
        """

        # ===== #
        # TO DO #
        # ===== #

        pass

    def attended_to(self, patient: Patient) -> List[Doctor]: # Compare sorted lst
        """
        Return a list of the unique doctors who have attended to <patient>.

        Definition (Attended):
        Supposing
           1/  visit is from <patient>.history, and
           2/  Dr Bob's ID number is visit.doctor_id
        then Dr Bob has ATTENDED TO Alice.

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> hosp.attended_to(hosp.patients[0])
        [Did: 99262168, Did: 99628500]
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> hosp.attended_to(hosp.patients[0]) #doctest: +NORMALIZE_WHITESPACE
        [Did: 99679013, Did: 99055562, Did: 99103117, Did: 99093432,
        Did: 99106844]
        """
        # ===== #
        # TO DO #
        # ===== #

        pass

    def prescribed_rate(self, doctor: Doctor, medication: str) -> float:
        """
        Return the prescription rate for <doctor> given <medication>.

        Definition (Prescription Rate):
        For visits among all patients histories the PRESCRIPTION RATE for
        <doctor> is:
           number of visits where <medication> was prescribed
           ----------------------------------------------------- * 100
           number of visits where ANY medication was prescribed

        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/janonly/')
        >>> hosp.prescribed_rate(hosp.doctors[3], 'Amiodarone HCl')
        50.0
        >>> hosp.prescribed_rate(hosp.doctors[3], 'Lithium')
        0.0
        >>> hosp = Hospital("123 Fake St.")
        >>> loaddata.read_hospital(hosp, 'data/year97/')
        >>> hosp.prescribed_rate(hosp.doctors[1], 'Amiodarone HCl')
        3.125
        """

        # ===== #
        # TO DO #
        # ===== #

        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': [
            'loaddata.load_doctors',
            'loaddata.load_patients',
            'loaddata.load_admissions',
            'loaddata.load_attendance',
            'loaddata.read_hospital',
            'load_schedules'
            ],
        'allowed-import-modules': [
            'loaddata',
            'doctest',
            'python_ta',
            'datetime',
            'typing',
            'collections',
            '__future__'
        ],
        'max-attributes': 15,
        'max-nested-blocks': 4,
        'max-args': 8,
    })
