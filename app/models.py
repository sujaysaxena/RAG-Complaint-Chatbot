from pydantic import BaseModel

class Complaint(BaseModel):
    name: str
    phone_number: str
    email: str
    complaint_details: str
