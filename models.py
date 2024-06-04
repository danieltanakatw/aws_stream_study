from datetime import datetime
from pydantic import BaseModel, Field, NonNegativeFloat, model_validator
import json

patient_stats_example = {
    "patient": "Nina",
    "time": "2024-05-14 12:05:30",
    "glucose_level": 120,
    "oxygen_saturation": 0.9,
    "body_temperature": 36.5,
    "respiratory_rate": 12,
    "heart_rate": 120,
    "blood_pressure_systolic": 190,
    "blood_pressure_diastolic": 130,
}

error_example = {"status_code": 422, "payload": "error", "error_message": "error"}


class PatientStats(BaseModel):
    model_config = {
        "title": "Blood Pressure Pair - Systolic and Diastolic",
        "json_schema_extra": {"examples": [patient_stats_example]},
    }

    patient: str = Field(description="Name of the patient")
    time: datetime
    glucose_level: NonNegativeFloat
    oxygen_saturation: NonNegativeFloat
    body_temperature: NonNegativeFloat
    respiratory_rate: NonNegativeFloat
    heart_rate: NonNegativeFloat
    blood_pressure_systolic: NonNegativeFloat
    blood_pressure_diastolic: NonNegativeFloat

    @model_validator(mode="after")
    def validate_pressure(self):
        if self.blood_pressure_diastolic > self.blood_pressure_systolic:
            raise ValueError("Diastolic pressure should be smaller than systolic")
        return self


class ErrorMessage(BaseModel):
    model_config = {
        "title": "Error repository - All data with error should be routed here",
        "json_schema_extra": {"examples": [error_example]},
    }
    status_code: int
    payload: str
    error_message: str
