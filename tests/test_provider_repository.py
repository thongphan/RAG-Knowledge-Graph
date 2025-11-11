import pytest

# -------------------------------
# Tests for HealthcareProvider repository
# -------------------------------
def test_provider_repository_insert_and_read(provider_repository):
    """
    Test inserting and reading HealthcareProvider nodes via repository.
    """
    # Insert providers
    batch = [
        {"name": "Dr. Jessica Lee", "bio": "Cardiology"},
        {"name": "Dr. John Smith", "bio": "Neurology"},
    ]
    provider_repository.add_providers(batch)

    # Read back
    providers = provider_repository.get_all_providers()
    names = [p["name"] for p in providers]

    assert "Dr. Jessica Lee" in names
    assert "Dr. John Smith" in names
    print("✅ HealthcareProvider batch insert and read successful")


# -------------------------------
# Tests for Patient repository
# -------------------------------
def test_patient_repository_insert_and_read(executor):
    """
    Test inserting a Patient node using executor (or PatientRepository if available).
    """
    # Insert a patient
    executor.execute_write(
        "CREATE (p:Patient {name:$name})",
        {"name": "Alice Nguyen"}
    )

    # Read back
    result = executor.execute_read(
        "MATCH (p:Patient) RETURN p.name AS name"
    )
    names = [r["name"] for r in result]

    assert "Alice Nguyen" in names
    print("✅ Patient insert and read successful")


# -------------------------------
# Optional: Parametrized read test for providers
# -------------------------------
@pytest.mark.parametrize("expected_count", [2])
def test_provider_count(provider_repository, expected_count):
    providers = provider_repository.get_all_providers()
    assert len(providers) >= expected_count
