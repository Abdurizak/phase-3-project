import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, Patient, Doctor, Appointment
from lib.db import db

# Setup an in-memory SQLite database for testing
@pytest.fixture
def test_session():
    engine = create_engine('sqlite:///:memory:')  # In-memory database
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()

def test_create_patient(test_session):
    patient = Patient(name="John Doe", age=30, status="admitted")
    test_session.add(patient)
    test_session.commit()

    # Verify the patient was added
    added_patient = test_session.query(Patient).filter_by(name="John Doe").first()
    assert added_patient is not None
    assert added_patient.name == "John Doe"
    assert added_patient.age == 30
    assert added_patient.status == "admitted"

def test_create_doctor(test_session):
    doctor = Doctor(name="Dr. Smith", specialty="Cardiology")
    test_session.add(doctor)
    test_session.commit()

    # Verify the doctor was added
    added_doctor = test_session.query(Doctor).filter_by(name="Dr. Smith").first()
    assert added_doctor is not None
    assert added_doctor.name == "Dr. Smith"
    assert added_doctor.specialty == "Cardiology"

def test_create_appointment(test_session):
    # Add a doctor and a patient
    doctor = Doctor(name="Dr. Smith", specialty="Cardiology")
    patient = Patient(name="John Doe", age=30, status="admitted")
    test_session.add(doctor)
    test_session.add(patient)
    test_session.commit()

    # Create an appointment
    appointment = Appointment(doctor_id=doctor.id, patient_id=patient.id, date="2024-12-25")
    test_session.add(appointment)
    test_session.commit()

    # Verify the appointment was added
    added_appointment = test_session.query(Appointment).filter_by(doctor_id=doctor.id).first()
    assert added_appointment is not None
    assert added_appointment.doctor_id == doctor.id
    assert added_appointment.patient_id == patient.id
    assert str(added_appointment.date) == "2024-12-25 00:00:00"

def test_relationships(test_session):
    # Create a doctor and a patient
    doctor = Doctor(name="Dr. Smith", specialty="Cardiology")
    patient = Patient(name="John Doe", age=30, status="admitted")
    doctor.patients.append(patient)

    test_session.add(doctor)
    test_session.commit()

    # Verify relationships
    added_doctor = test_session.query(Doctor).filter_by(name="Dr. Smith").first()
    assert added_doctor is not None
    assert len(added_doctor.patients) == 1
    assert added_doctor.patients[0].name == "John Doe"

    added_patient = test_session.query(Patient).filter_by(name="John Doe").first()
    assert added_patient is not None
    assert len(added_patient.doctors) == 1
    assert added_patient.doctors[0].name == "Dr. Smith"
