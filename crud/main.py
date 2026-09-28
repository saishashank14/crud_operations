from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Student(BaseModel):
    name: str
    email: EmailStr
    course: str
    age: int
    id:int
students = []

next_id = 1

@app.post("/students")
def create_student(student: Student):

    global next_id

    for existing_student in students:

        if existing_student["email"] == student.email:

            raise HTTPException(
                status_code=404,
                detail="Student already exists"
            )
        
    new_student = {
        "id": next_id,
        "name": student.name,
        "email": student.email,
        "course": student.course,
        "age": student.age
    }

    students.append(new_student)

    next_id = next_id + 1

    return new_student

@app.get("/students")
def get_students():

    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:

        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student
):

    for student in students:

        if student["id"] == student_id:

            student["name"] = updated_student.name
            student["email"] = updated_student.email
            student["course"] = updated_student.course
            student["age"] = updated_student.age

            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students:

        if student["id"] == student_id:

            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

