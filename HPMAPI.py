# Fast Api Demonstration : Hospital Patient Management API
# Scenario : a Hospital wants to develop an API to manage the patients information. The API should allow users to add patients, 
# view all patients,search patients by name,delete patients by ID and update patient details . 
# The API should also allow users to update patient information. 


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app =FastAPI(
title="Hospital Patient Management API",
    description="API for managing patient information in a hospital",
    version="1.0.0"
)

#pydantic model for patient information
class Patient(BaseModel):
   patient_id: int
   name: str
   age: int
   disease: str
   phone: Optional[str] = None


# In-memory database to store patient information
patients = []

#HOME API
@app.get("/")
def home():
    return {"message": "Welcome to the Hospital Patient Management API"}


#ADD PATIENT API
@app.post("/patients")
def add_patient(patient: Patient):
    # check duplicate patient_id
    for p in patients:
        if p.patient_id == patient.patient_id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    patients.append(patient)
    return {"message": "Patient added successfully", "patient": patient}


#Get All Patients API
@app.get("/patients")
def get_all_patients ():

    return {
        "total_patients": len(patients),
        "patients": patients
        }

#Get Patient by Id API
app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for patient in patients:
        if patient.patient_id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")


#Update Patient API
@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, upadate_patient: Patient):
    for index, patient in enumerate(patients): # enumerate is used to get the index of the patient in the list
        if patient.patient_id == patient_id:
            patients[index] = upadate_patient
            return {"message": "Patient updated successfully", "patient": upadate_patient}
    raise HTTPException(status_code=404, detail="Patient not found")

#Delete Patient API
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for index, patient in enumerate(patients):
        if patient.patient_id == patient_id:
            del patients[index]
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")