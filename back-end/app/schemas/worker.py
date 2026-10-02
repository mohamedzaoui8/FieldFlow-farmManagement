from pydantic import BaseModel, Field


class WorkerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    chef_id: int
    job_id: int


class WorkerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    chef_id: int | None = None
    job_id: int | None = None
    status: str | None = None


class WorkerResponse(BaseModel):
    id: int
    name: str
    chef_id: int
    job_id: int
    status: str

    class Config:
        from_attributes = True

class ReassignWorkers(BaseModel):
    from_chef_id: int
    to_chef_id: int