import random
from faker import *
import requests
import time
from dotenv import load_dotenv
import os


class Generator:
    def __init__(self, rate=500):
        self.rate = rate
        self.fake = Faker()

    def get_patient_stats_record(self, faulty_records=False):

        record = {
            "patient": random.choice(["Anna", "Beatrice", "Leia", "Nina"]),
            "time": self.fake.date_time_between(
                start_date="-30d", end_date="now"
            ).strftime("%Y-%m-%d %H:%m:%S"),
            "glucose_level": round(self.fake.pyfloat(min_value=140, max_value=150), 2),
            "oxygen_saturation": round(
                self.fake.pyfloat(right_digits=2, min_value=0.92, max_value=1.0), 2
            ),
            "body_temperature": round(
                self.fake.pyfloat(right_digits=2, min_value=35.5, max_value=37.0), 2
            ),
            "respiratory_rate": self.fake.pyint(min_value=10, max_value=11),
            "heart_rate": self.fake.pyint(min_value=90, max_value=100),
            "blood_pressure_systolic": self.fake.pyint(min_value=110, max_value=120),
            "blood_pressure_diastolic": self.fake.pyint(min_value=80, max_value=90),
        }

        if faulty_records and self.fake.pyfloat(min_value=0, max_value=1.0) > 0.9:
            record["blood_pressure_systolic"] = 90
            record["blood_pressure_diastolic"] = 120
            

        return record

    def get_patient_stats_records(self, faulty_records=False):
        return [
            self.get_patient_stats_record(faulty_records=faulty_records)
            for _ in range(self.rate)
        ]


def main():
    load_dotenv()
    api_url = os.environ.get("API_URL", "localhost")
    while time.time() < time.time() + 60 * 10:
        payloads = Generator().get_patient_stats_records(faulty_records=True)
        for payload in payloads:
            response = requests.post(
                url=f"http://{api_url}:8000/patient_stats/", json=payload
            )

            if response.status_code != 200:
                error_payload = {
                    "status_code": response.status_code,
                    "payload": str(payload),
                    "error_message": response.text,
                }
                requests.post(
                    url=f"http://{api_url}:8000/error_message/", json=error_payload
                )


if __name__ == "__main__":
    main()
