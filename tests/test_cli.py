import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from phase_3_project.cli import manage_patients, add_patient, delete_patient, list_patients, admit_patient, release_patient, schedule_appointment
from phase_3_project.models import Patient, Appointment

@pytest.fixture
def runner():
    return CliRunner()

def test_add_patient(runner):
    with patch('cli.session') as mock_session, \
         patch('cli.Patient') as MockPatient:
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        MockPatient.return_value = MagicMock()

        # Simulate CLI input
        result = runner.invoke(manage_patients, input="1\nJohn Doe\n30\n7\n")

        assert result.exit_code == 0
        assert 'has been added' in result.output
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

def test_delete_patient(runner):
    with patch('cli.session') as mock_session:
        mock_patient = MagicMock(name="John Doe")
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.delete = MagicMock()
        mock_session.commit = MagicMock()

        result = runner.invoke(manage_patients, input="2\n1\n7\n")

        assert result.exit_code == 0
        assert 'has been deleted' in result.output
        mock_session.delete.assert_called_once_with(mock_patient)
        mock_session.commit.assert_called_once()

def test_list_patients(runner):
    with patch('cli.session') as mock_session:
        mock_patient = MagicMock(id=1, name="John Doe", age=30, status="admitted")
        mock_session.query.return_value.all.return_value = [mock_patient]

        result = runner.invoke(manage_patients, input="3\n7\n")

        assert result.exit_code == 0
        assert 'John Doe' in result.output

def test_admit_patient(runner):
    with patch('cli.session') as mock_session:
        mock_patient = MagicMock(name="John Doe", status="discharged")
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.commit = MagicMock()

        result = runner.invoke(manage_patients, input="4\n1\n7\n")

        assert result.exit_code == 0
        assert 'admitted' in result.output
        assert mock_patient.status == "admitted"
        mock_session.commit.assert_called_once()

def test_release_patient(runner):
    with patch('cli.session') as mock_session:
        mock_patient = MagicMock(name="John Doe")
        mock_session.query.return_value.get.return_value = mock_patient
        mock_session.commit = MagicMock()

        result = runner.invoke(manage_patients, input="5\n1\nParacetamol\n7\n")

        assert result.exit_code == 0
        assert 'released' in result.output
        assert mock_patient.status == "released"
        assert mock_patient.prescription == "Paracetamol"
        mock_session.commit.assert_called_once()

def test_schedule_appointment(runner):
    with patch('cli.session') as mock_session:
        mock_doctor = MagicMock(id=1, name="Dr. Smith")
        mock_patient = MagicMock(id=2, name="John Doe")
        mock_session.query.return_value.filter_by.side_effect = lambda name: [mock_doctor] if "Dr. Smith" in name else [mock_patient]
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()

        result = runner.invoke(manage_patients, input="6\nDr. Smith\nJohn Doe\n2024-12-25\n7\n")

        assert result.exit_code == 0
        assert 'Appointment scheduled' in result.output
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
