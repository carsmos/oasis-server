from pydantic import BaseModel, Field


class ControllerModel(BaseModel):
    name: str
    desc: str = ''
    type: str = 'controller'


class VersionModel(BaseModel):
    type: str = 'version'
    parent_id: int
    version: str
    setup_file_name: str
    config_file_name: str = ''
    data_flow_file_name: str