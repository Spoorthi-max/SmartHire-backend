import json
from database import SessionLocal, Base, engine

from models.user import User
from models.job import Job
from models.candidate import Candidate
from models.question import Question


# Make sure tables exist
Base.metadata.create_all(bind=engine)


def seed_database():
    db = SessionLocal()

    try:
        # Load JSON dataset
        with open("data/Input_Data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # --------------------------------------------------
        # 1. USERS
        # --------------------------------------------------

        for user_data in data["users"]:
            existing_user = (
                db.query(User)
                .filter(User.username == user_data["username"])
                .first()
            )

            if not existing_user:
                user = User(
                    username=user_data["username"],
                    role=user_data["role"],
                    password=user_data["password"]
                )

                db.add(user)

        # --------------------------------------------------
        # 2. JOB DESCRIPTIONS
        # --------------------------------------------------

        for jd_data in data["job_descriptions"]:
            existing_jd = (
                db.query(Job)
                .filter(Job.id == jd_data["id"])
                .first()
            )

            if not existing_jd:
                job = Job(
                    id=jd_data["id"],
                    role=jd_data["title"],
                    location=jd_data["location"],
                    experience_years=jd_data["experience_years"],
                    education=jd_data["education"],
                    must_have=jd_data["must_have"],
                    nice_to_have=jd_data["nice_to_have"],
                    weights=jd_data["weights"],
                    pass_threshold=jd_data["pass_threshold"],
                    confidence_cutoff=jd_data["confidence_cutoff"],
                    summary=jd_data["summary"]
                )

                db.add(job)

        # --------------------------------------------------
        # 3. CANDIDATES
        # --------------------------------------------------

        for candidate_data in data["candidates"]:
            existing_candidate = (
                db.query(Candidate)
                .filter(Candidate.id == candidate_data["id"])
                .first()
            )

            if not existing_candidate:
                candidate = Candidate(
                    id=candidate_data["id"],
                    user=candidate_data["user"],
                    name=candidate_data["name"],
                    email=candidate_data["email"],
                    applied_jd=candidate_data["applied_jd"],
                    experience_years=candidate_data["experience_years"],
                    education=candidate_data["education"],
                    location=candidate_data["location"],
                    profile_type=candidate_data["profile_type"],
                    resume=candidate_data["resume"]
                )

                db.add(candidate)

        # --------------------------------------------------
        # 4. QUESTIONS
        # --------------------------------------------------

        for question_data in data["questions"]:
            existing_question = (
                db.query(Question)
                .filter(Question.id == question_data["id"])
                .first()
            )

            if not existing_question:
                question = Question(
                    id=question_data["id"],
                    jd_id=question_data["jd_id"],
                    text=question_data["text"],
                    reference_answer=question_data["reference_answer"],
                    rubric=question_data["rubric"]
                )

                db.add(question)

        # Save everything
        db.commit()

        print("===================================")
        print("Database seeded successfully!")
        print("===================================")

        print(f"Users: {db.query(User).count()}")
        print(f"Jobs: {db.query(Job).count()}")
        print(f"Candidates: {db.query(Candidate).count()}")
        print(f"Questions: {db.query(Question).count()}")

    except Exception as e:
        db.rollback()
        print("ERROR while seeding database:")
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()