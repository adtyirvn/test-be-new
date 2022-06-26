import sqlalchemy

from sqlalchemy.orm import Session

from db.models.course import Course
from pydantic_schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session):
    return db.query(Course).all()


def get_user_courses(db: Session, user_id: int):
    courses = db.query(Course).filter(Course.user_id == user_id).all()
    return courses


def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        title=course.title,
        description=course.description,
        user_id=course.user_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_one_course(db: Session, course_id: int):
    courses = db.query(Course).filter(Course.id == course_id).first()
    db.delete(courses)
    db.commit()
    db.commit()
    db.refresh(courses)
    return courses

def update_one_course(db: Session, course_id: int, course: CourseUpdate):
    courses = db.query(Course).filter(Course.id == course_id).first()
    courses_data = course.dict(exclude_unset=True)
    for key, value in courses_data.items():
        setattr(courses, key, value)
    db.add(courses)
    db.commit()
    db.refresh(courses)
    return courses
    