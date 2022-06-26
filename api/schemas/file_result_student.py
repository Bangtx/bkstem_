from schemas.schema import Schema


class FileResultStudentBase(Schema):
    msg: str = None
    name: str
    url: str
    student: int
    class_room: int


class FileResultStudentCreate(FileResultStudentBase):
    home_work_file: int


class FileResultStudentUpdate(FileResultStudentCreate):
    pass