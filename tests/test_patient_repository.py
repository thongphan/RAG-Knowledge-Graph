import pytest

def test_patient_repository_insert_and_read(executor):
    """
    Test inserting a Patient node using executor.
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
