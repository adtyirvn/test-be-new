from typing import List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session

from db.db_setup import get_db
from pydantic_schemas.course import Course, CourseCreate, CourseUpdate
from api.utils.courses import get_course, get_courses, create_course, delete_one_course, update_one_course

router = fastapi.APIRouter()


@router.get("/courses", response_model=List[Course])
async def read_courses(db: Session = Depends(get_db)):
    courses = get_courses(db=db)
    return courses


@router.post("/courses", response_model=Course)
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db=db, course=course)


@router.get("/courses/{course_id}")
async def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.patch("/courses/{course_id}", response_model=Course)
async def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    else:
       db_course= update_one_course(db=db, course_id=course_id, course=course)
    return db_course


@router.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = get_course(db=db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    else:
       db_course= delete_one_course(db=db, course_id=course_id)
    return db_course


@router.get("/courses/{course_id}/sections")
async def read_course_sections():
    return {"courses": []}