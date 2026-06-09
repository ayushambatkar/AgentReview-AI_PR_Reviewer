from pydantic import BaseModel

class Repository(BaseModel):
    full_name: str


class Installation(BaseModel):
    id: int


class PullRequest(BaseModel):
    number: int
    title: str
    body: str | None = None


class User(BaseModel):
    login: str
    

class PullRequestEvent(BaseModel):
    action: str
    repository: Repository
    installation: Installation
    number: int
    pull_request: PullRequest
    user: User
    
class PullRequestFile(BaseModel):
    filename: str
    status: str
    patch: str | None = None