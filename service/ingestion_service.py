from neo4j.graph import Relationship

from core.csv_reader import CSVReader
from domain.patient import Patient
from domain.healthcare_provider import HealthcareProvider
from domain.relationships import Relationships
from domain.specialization import Specialization
from domain.location import Location

class IngestionService:
    BATCH_SIZE = 100  # tweak based on performance
    def __init__(self, csv_path,headers,provider_repo, patient_repo,specialization_repo, location_repo,relationships_repo):
        self.csv_path = csv_path
        self.headers = headers
        self.provider_repo = provider_repo
        self.patient_repo = patient_repo
        self.specialization_repo = specialization_repo
        self.location_repo = location_repo
        self.relationships_repo = relationships_repo

    def ingest(self):
        reader = CSVReader(self.csv_path, self.headers)
        total_rows:int = 0

        provider_batch = []
        patient_batch = []
        specialization_batch = []
        location_batch = []
        relationships_batch = []

        for row in reader.read_rows():
            print(f"Row: {row}")
            provider_batch.append(HealthcareProvider(name=row["Provider"], bio=row["Bio"]))
            patient_batch.append(
                Patient(name=row["Patient"], age=row["Patient_Age"], gender= row["Patient_Gender"], condition= row["Patient_Condition"]))
            specialization_batch.append(Specialization(name= row["Specialization"]))
            location_batch.append(Location(name =row["Location"]))
            relationships_batch.append(
                Relationships(row["Provider"], row["Patient"], row["Specialization"], row["Location"]))

            if len(provider_batch) >= self.BATCH_SIZE:
                self._flush_batches(provider_batch, patient_batch, specialization_batch, location_batch,
                                    relationships_batch)
                provider_batch, patient_batch, specialization_batch, location_batch, relationships_batch = [], [], [], [], []
            total_rows += 1

        # flush remaining rows
        if provider_batch:
            self._flush_batches(provider_batch, patient_batch, specialization_batch, location_batch,
                                relationships_batch)

        print("All rows ingested successfully!")

        print(f"\nTotal rows ingested: {total_rows}")

    def _flush_batches(self, provider_batch, patient_batch, specialization_batch, location_batch, relationships_batch):
            self.provider_repo.save_batch(provider_batch)
            print("Provider batch ingested")
            self.patient_repo.save_batch(patient_batch)
            print("Patient batch ingested")
            self.specialization_repo.save_batch(specialization_batch)
            print("Specialization batch ingested")
            self.location_repo.save_batch(location_batch)
            print("Location batch ingested")
            self.relationships_repo.save_batch(relationships_batch)
            print("Relationships batch ingested")