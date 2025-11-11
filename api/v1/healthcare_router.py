from fastapi import APIRouter, Depends,HTTPException

from dto.patient_DTO import PatientDTO
from service.provider_service import ProviderService, get_provider_service
from service.patient_service import PatientService,get_patient_service
from typing import List
from dto.provider_DTO import ProviderDTO
from dto.patient_DTO import PatientDTO



router = APIRouter(prefix="/api/v1", tags=["Providers"])

# --- GET ALL PROVIDERS ---
@router.get("/providers", response_model=List[ProviderDTO])
async def get_all_providers(service: ProviderService = Depends(get_provider_service)):
    """
    Retrieve all healthcare providers.
    """
    try:
        return service.get_all_providers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching providers: {e}")
# --- GET ALL Patients ---
@router.get("/patients", response_model=List[PatientDTO])
async def get_all_patients(service:PatientService = Depends(get_patient_service)):
    """
    Retrieve all patient.
    """
    try:
        return service.get_all_patients()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching patients: {e}")

