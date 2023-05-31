from abc import ABC, abstractmethod
from pydantic import BaseModel, validator
from typing import Optional, Union


class SourceABC(ABC, BaseModel):
    @property
    @abstractmethod
    def execution_json(self) -> dict:
        ...

    @validator('*', pre=True, allow_reuse=True)
    def empty_str_to_none(cls, value, field):
        if value == '':
            return field.default
        return value

    class Config:
        fields = {
            'repo_branch': 'branch',
            'repo_user': 'username',
            'report_pass': 'password',
            'repo_key': 'private_key'
        }
        allow_population_by_field_name = True


class SourceGitSSH(SourceABC):
    repo: str
    repo_key: str
    repo_branch: Optional[str] = 'main'
    report_pass: Optional[str]

    @property
    def execution_json(self):
        return {'git': self.dict(exclude_none=True)}


class SourceGitHTTPS(SourceABC):
    repo: str
    repo_branch: Optional[str] = 'main'
    repo_user: Optional[str]
    report_pass: Optional[str]

    @property
    def execution_json(self):
        return {'git': self.dict(exclude_none=True)}


class SourceArtifact(SourceABC):
    file_meta: Optional[dict]
    file: Union[str, dict]

    @property
    def execution_json(self):
        return {
            'artifact': {'file': self.file, 'file_meta': self.file_meta}
        }


class SourceLocal(SourceABC):
    path: str

    @property
    def execution_json(self):
        return {
            'local_path': self.path
        }


class SourceContainer(SourceABC):
    image_name: str

    @property
    def execution_json(self):
        return {
            'image_name': self.image_name
        }

