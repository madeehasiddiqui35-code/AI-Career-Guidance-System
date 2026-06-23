import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from auth import register_user, login_user

if "logged_in" not in st.session_state:

    st.session_state.logged_in=False

try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )
    else:
        client = None

except Exception:
    client = None

st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("SIDEBAR")

if st.session_state.logged_in:

    page = st.sidebar.radio(

        "Navigate",

        [

             "Profile",

        "Dashboard",

        "Skill Gap Analysis",

        "Career Roadmap",

        "Career Match",

        "Resume Analyzer",

        "Interview Coach",

        "Progress Tracker",

        "Job Description Analyzer",

        "Project Recommendations",

        "Certification Tracker",

        "Learning Resources",

        "AI Career Chatbot",

        "Logout"

       

        ]

    )

else:

    page = st.sidebar.radio(

        "Navigate",

        [

        "Login",

        "Register"

        ]

    )

if page=="Register":

    st.title("Register")

    name=st.text_input("Name")

    email=st.text_input("Email")

    password=st.text_input(

        "Password",

        type="password"

    )

    if st.button("Register"):

        success = register_user(

            name,

            email,

            password

        )

        if success:

            st.success("Registration Successful")

        else:

            st.error("Email already exists")

elif page=="Login":

    st.title("Login")

    email=st.text_input("Email")

    password=st.text_input(

        "Password",

        type="password"

    )

    if st.button("Login"):

        user = login_user(

            email,

            password

        )

        if user:

            st.session_state.logged_in=True

            st.session_state.user=user

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Credentials")

elif page=="Logout":

    st.session_state.logged_in=False

    st.session_state.user=None

    st.success("Logged out")

    st.rerun()


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

elif page == "Profile":

    st.title("My Profile")

    user = st.session_state.get("user", ("Not Available", "Not Available"))

    st.write("Name:", user[0])
    st.write("Email:", user[1])

    st.write("Career Goal:", st.session_state.get("goal", "Not Selected"))

    st.write("Internship Score:", st.session_state.get("score", 0))

elif page == "Skill Gap Analysis":
    st.title("Skill Gap Analysis")

    missing_skills=st.session_state.get("missing_skills", [])

    st.subheader("Skill Gap Analysis")
    if missing_skills:
        for skill in missing_skills:
            st.write(skill)
    else:
        st.write("No major skill gaps detected")
                        
elif page == "Career Roadmap":
    st.title("Career Roadmap")

    missing_skills = st.session_state.get("missing_skills", [])
    
    st.subheader("Your Personalized Roadmap")

    for step_number, skill in enumerate(missing_skills, start=1):
        st.write(f"Step {step_number}: Learn {skill}")

    if missing_skills:
        st.write(f"Step {len(missing_skills)+1}: Build portfolio projects")
        st.write(f"Step {len(missing_skills)+2}: Apply for internships")

    else:
        st.write("You are internship-ready")

elif page == "Career Match":
    st.title("Career Match")

    skills_list = st.session_state.get("skills_list", [])
    career_skills = {
    "Data Science": ["python", "sql", "machine learning", "statistics", "data visualization"],
    "AI Engineer": ["python", "machine learning", "deep learning", "tensorflow"],
    "Software Engineer": ["python", "data structures", "algorithms", "git"],
    "Web Developer": ["html", "css", "javascript", "react"]
}
    results = {}

    for role, required_skills in career_skills.items():
        matched = 0

        for skill in required_skills:
            if skill in skills_list:
                matched+=1

        score = int((matched/ len(required_skills))*100)
        results[role] = score

    st.subheader("Your Career Matches")

    sorted_roles = sorted(results.items(), key=lambda x: x[1], reverse=True)

    for role, score in sorted_roles:
        st.write(f"{role} → {score}% match")
        st.progress(score / 100)

        required_skills= career_skills[role]

        matched_skills = []
        missing_skills=[]

        for s in required_skills:
            if s in skills_list:
                matched_skills.append(s)
            else:
                missing_skills.append(s)

        st.subheader("Matched Skills: ")

        for s in matched_skills:
            st.write(s)

        st.subheader("Missing Skills:")

        for s in missing_skills:
            st.write(s)

        st.divider()

    if results:
        best_role = max(results, key=results.get)
        best_score = results[best_role]

        career_advice = {
                    "Data Science": ["Learn SQL and Database Management",
                "Build Data Analysis and Machine Learning Projects",
                "Apply for Data Science Internships"],

                    "AI Engineer": ["Learn Deep Learning and Neural Networks",
                    "Build AI Projects using TensorFlow or PyTorch",
                    "Apply for AI/ML Internships"],

                    "Software Engineer": ["Practice Data Structures and Algorithms",
                    "Build Full-Stack or Backend Projects",
                    "Apply for Software Development Internships"],

                    "Web Developer": [        
                    "Master HTML, CSS, JavaScript, and React",
                    "Build Responsive Web Applications",
                    "Create a Portfolio and Apply for Web Development Internships"
        ]
                }

        st.subheader("Recommended Career")
        st.write(best_role)

        st.write("Match Score:", best_score, "%")

        st.subheader("Next Steps")

        for advice in career_advice[best_role]:
            st.write(advice)
     

if st.button("Analyze Resume"):

    if resume_text.strip() == "":
        st.warning("Please upload or paste your resume.")

    elif client is None:
        st.error(
            "Groq API Key not found. Add GROQ_API_KEY in Streamlit Secrets."
        )

    else:

        with st.spinner("Analyzing Resume..."):

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are an expert Resume Reviewer.

Analyze the resume and give:

1. Overall Score out of 100
2. Strengths
3. Weaknesses
4. Missing Skills
5. Suggestions to improve

Keep the response simple.
"""
                        },
                        {
                            "role": "user",
                            "content": resume_text
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.subheader("AI Resume Analysis")
                st.write(answer)

            except Exception as e:
                st.error(f"Error while analyzing resume: {e}")
                
elif page == "Interview Coach":
    st.title("Interview Coach")

    role = st.selectbox(
        "Select Role", [
        "Data Science",
        "AI Engineer",
        "Software Engineer",
        "Web Developer"
            ])

    if st.button("Generate Questions"):

        questions = {
            "Data Science": ["What is overfitting?",
            "Explain mean vs median",
            "What is SQL join?"
            ],
            "AI Engineer":[
            "What is neural network?",
            "What is backpropagation?",
            "What is deep learning?"
            ],
            "Software Engineer": [
                "What is OOP?",
                "What is recursion?",
                "What is Git?"
            ],
            "Web Developer": [
                "What is HTML vs CSS?",
                "What is React?",
                "What is DOM?"
            ] }
        
        for q in questions[role]:
            st.write(q)

elif page == "Progress Tracker":
    st.title("Progress Tracker")

    skills_list = st.session_state.get("skills_list",[])
    score = st.session_state.get("score",0)
    goal = st.session_state.get("goal","")

    total_skills = [
    "python",
    "sql",
    "machine learning",
    "github",
    "projects"
]    
    matched_skills = 0

    for skill in total_skills:
        if skill in skills_list:
            matched_skills += 1

    progress = matched_skills / len(total_skills)

    st.subheader("Skill Progress")
    st.progress(progress)
    st.write(f"Progress: {int(progress*100)}%")
    
    st.subheader("Internship readiness Score")
    st.write(score)

    if score >= 80:
        st.success("Excellent Progress")
    elif score >= 60:
        st.warning("Good Progress")
    else:
        st.error("Needs Improvement")

elif page == "Job Description Analyzer":
    st.title("Job Description Analyzer")
   
    descriptive_text= st.text_area("Paste your job description here")

    skills_list = st.session_state.get("skills_list",[])

    if st.button("Analyze Job Description"):
        job_text = descriptive_text.lower()

        missing_skills=[]

        job_skills = [
            "python",
            "sql",
            "git",
            "machine learning",
            "docker"
        ]
        
        for s in job_skills:
            if s in job_text and s not in skills_list:
                missing_skills.append(s)
            
        st.subheader("Missing Skills")

        if missing_skills:
            for s in missing_skills:
                st.write(f" {s}")

        else:
            st.success("You already have all the detected skills!")

elif page == "Project Recommendations":
    st.title("Project Recommendations")

    goal = st.session_state.get("goal", "")
    
    if not goal:
        st.warning("Please complete Dashboard first.")
    else:
        projects = {
        "Data Science": [
        "Student Performance Analysis",
        "Sales Dashboard",
        "House Price Prediction"
    ],

    "AI Engineer": [
        "Chatbot",
        "Image Classifier",
        "Resume Screening AI"
    ],

    "Software Engineer": [
        "Library Management System",
        "Expense Tracker",
        "Student Portal"
    ],

    "Web Developer": [
        "E-commerce Website",
        "Portfolio Website",
        "Task Manager App"
    ]
}

        recommended_projects = projects.get(goal, [])
        st.subheader(f"Projects for {goal}")

        for r in recommended_projects:
            st.write(r)

elif page == "Learning Resources":
    st.title("Learning Resources")

    goal = st.session_state.get("goal", "")

    if not goal:
        st.warning("No goal exists")

    else:
        resources = {

    "Data Science": [
        {
            "name": "Python for Data Science",
            "type": "Course",
            "description": "Learn Python fundamentals for data analysis and machine learning."
        },
        {
            "name": "SQL Tutorial",
            "type": "Course",
            "description": "Learn database querying and data management using SQL."
        },
        {
            "name": "Machine Learning Specialization",
            "type": "Course",
            "description": "Understand supervised and unsupervised machine learning concepts."
        }
    ],

    "AI Engineer": [
        {
            "name": "Deep Learning Specialization",
            "type": "Course",
            "description": "Learn neural networks, CNNs, and deep learning fundamentals."
        },
        {
            "name": "TensorFlow Documentation",
            "type": "Documentation",
            "description": "Official guide for building AI applications with TensorFlow."
        },
        {
            "name": "Prompt Engineering Guide",
            "type": "Learning Guide",
            "description": "Learn how to effectively interact with Large Language Models."
        }
    ],

    "Software Engineer": [
        {
            "name": "Data Structures & Algorithms",
            "type": "Course",
            "description": "Master problem-solving and coding interview concepts."
        },
        {
            "name": "Git & GitHub",
            "type": "Course",
            "description": "Learn version control and collaborative software development."
        },
        {
            "name": "System Design Basics",
            "type": "Course",
            "description": "Understand scalable software architecture and design principles."
        }
    ],

    "Web Developer": [
        {
            "name": "HTML & CSS Fundamentals",
            "type": "Course",
            "description": "Learn the foundations of web development."
        },
        {
            "name": "JavaScript Tutorial",
            "type": "Course",
            "description": "Master JavaScript for interactive web applications."
        },
        {
            "name": "React Documentation",
            "type": "Documentation",
            "description": "Official React guide for building modern front-end applications."
        }
    ]
}
        recommended_resources = resources.get(goal, [])

        for resource in recommended_resources:
            st.write("Resource:", resource["name"])
            st.write("Type:", resource["type"])
            st.write(resource["description"])
            st.divider()

elif page == "Certification Tracker":
    st.title("Certification Tracker")

    goal = st.session_state.get("goal", "")

    certification = st.text_input("Enter completed certifications")
    
    certification_list = [
        c.strip().lower()
        for c in certification.split(",")
        if c.strip()
    ]
        
    st.subheader("Completed Certifications")

    for cert in certification_list:
        st.write(cert)

    st.write("Total Certifications:", len(certification_list))

    recommended_certs = {
        "Data Science": [
            "google data analytics",
            "ibm data science",
            "microsoft data analyst"
        ],

        "AI Engineer": [
            "tensorflow developer",
            "deep learning specialization",
            "generative ai certification"
        ],

        "Software Engineer": [
            "aws cloud practitioner",
            "github foundations",
            "oracle java certification"
        ],

        "Web Developer": [
            "meta front-end developer",
            "javascript certification",
            "responsive web design"
        ]
    }    

    goal_recommendations = recommended_certs.get(goal, [])

    st.subheader("Recommended Certifications")

    for c in goal_recommendations:
        if c not in certification_list:
            st.write(c)

elif page == "AI Career Chatbot":

    st.title("AI Career Chatbot")

    question = st.text_input(
        "Ask a career question..."
    )

    if st.button("Get Answer"):

        if question.strip() == "":
            st.warning("Please enter a question")

        elif client is None:
            st.error(
                "Groq API Key not found. Add GROQ_API_KEY in Streamlit Secrets."
            )

        else:

            with st.spinner("Thinking..."):

                try:

                    response = client.chat.completions.create(

                        model="llama-3.3-70b-versatile",

                        messages=[

                            {
                                "role": "system",

                                "content": """
You are an AI Career Guidance Assistant.

Help students with:
- Career advice
- Resume tips
- Interview preparation
- Skill recommendations
- Career roadmaps
- Internship guidance

Keep answers simple and beginner friendly.
"""
                            },

                            {
                                "role": "user",
                                "content": question
                            }

                        ]

                    )

                    answer = response.choices[0].message.content

                    st.subheader("AI Response")
                    st.write(answer)

                except Exception as e:
                    st.error(f"Error: {e}")
