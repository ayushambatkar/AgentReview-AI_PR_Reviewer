from pydantic import BaseModel

class Repository(BaseModel):
    full_name: str


class Installation(BaseModel):
    id: int


class User(BaseModel):
    login: str


class PullRequest(BaseModel):
    number: int
    title: str
    body: str | None = None
    user: User
    

class PullRequestEvent(BaseModel):
    action: str
    number: int
    repository: Repository
    installation: Installation
    pull_request: PullRequest
    
class PullRequestFile(BaseModel):
    filename: str
    status: str
    patch: str | None = None