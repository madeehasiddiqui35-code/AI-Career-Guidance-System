import streamlit as st 

st.sidebar.title("SIDEBAR")

page = st.sidebar.radio(
    "Navigate",[
        "Dashboard"
   ]
    )

if page == "Dashboard":
    st.title("Dashboard")  
    st.subheader("Student Information")  
    name = st.text_input("Name")
    degree = st.text_input("Degree")

    Year = st.selectbox(
        "Year of study", [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

    st.subheader("Career Information")  
    skill = st.text_input("Skills")
    Goal = st.selectbox(
        "Career Goal", [
            "Data Science",
            "AI Engineer",
            "Software Engineer",
            "Web Developer",
            "Other"
        ]
    )

    
    st.subheader("Experience")  
    number = st.number_input(
        "Number of Projects",
            min_value=0,
            max_value=20,
            value=0
    )

    resume = st.selectbox(
        "Resume (Yes/No)", [
            "Yes",
            "No"
        ]
    )


    intern = st.selectbox(
        "Interview Preparation Level",[
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.subheader("Action")  
    if st.button("Generate Preparation Level"):

        score = 0 
        skills_list = [s.strip().lower() for s in skill.split(",")]

        if "python" in skills_list:
            score+=20

        if resume == "Yes":
            score+=20

        if number >=2:
            score+=20

        if intern == "Advanced":
            score+=20

        elif intern == "Intermediate":
            score+=10   

        st.write("Internship Readiness Score:", score)

        if score>=80:
            st.success("Excellent! You are internship ready.")

        elif score>=60:
            st.warning("Good progress. Keep improving!")

        else:
            st.error("You need more preparation before applying.")

        career_skills = {
            "Data Science":[
                "Python",
                "SQL",
                "Machine Learning",
                "Statistics",
                "Data Visualization"
            ],

            "AI Engineer":[
                "Python",
                "Machine Learning",
                "Deep Learning",
                "TensorFlow"
            ],

            "Software Engineer":[
                "Python",
                "Data Structures",
                "Algorithms",
                "Git"
            ],

            "Web Developer":[
                "HTML",
                "CSS",
                "JavaScript",
                "React"
            ]
        }

        required_skills = career_skills.get(Goal, [])
        missing_skills = []
        for s in required_skills:
            if s.lower() not in skills_list:
                missing_skills.append(s)

        #saved data for other pages
        st.session_state.score = score
        st.session_state.goal = Goal
        st.session_state.skills_list = skills_list
        st.session_state.missing_skills = missing_skills
        st.session_state.name = name
        st.session_state.degree = degree
        st.session_state.year = Year
        st.session_state.projects = number

    if "score" in st.session_state:
        st.divider()

        st.header("Career Summary")
        st.write("Name:", st.session_state.name)
        st.write("Degree:", st.session_state.degree)
        st.write("Year:", st.session_state.year)
        st.write("Career Goal:", st.session_state.goal)

        st.write("Internship Readiness Score:",
        st.session_state.score)

        st.write("Projects Completed:",
            st.session_state.projects)

        st.write("Skills Added:",
            len(st.session_state.skills_list))
            
        st.subheader("Missing Skills")

        if st.session_state.missing_skills:
            for skill in st.session_state.missing_skills:
                st.write(skill)
        else:
            st.success("No major skill gaps detected")


     
