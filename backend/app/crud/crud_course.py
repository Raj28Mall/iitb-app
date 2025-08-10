from app.db.session import db

if __name__ == "__main__":
    courses = db.collection("courses").get()
    for course in courses:
        print(course.to_dict())
        break
    print("Total courses:", len(courses))