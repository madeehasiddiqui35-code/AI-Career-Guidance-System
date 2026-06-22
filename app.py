import streamlit as st
from PyPDF2 import PdfReader

try:
    from groq import Groq

    if "GROQ_API_KEY" in st.secrets:
        client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )
    else:
        client = None

except:
    client = None
    
st.sidebar.title("SIDEBAR")

page = st.sidebar.radio(
    "Navigate",[
        "Dashboard",
        "Skill Gap Analysis",
        "Career Roadmap",
        "Resume Analyzer",
        "Interview Coach",
         "Certification Tracker",
        "Learning Resources"
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

elif page == "Resume Analyzer":

    st.title("Resume Analyzer")

    st.write("Paste your resume or upload a file")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    resume_text = ""

    if uploaded_file is not None:

        if uploaded_file.type == "application/pdf":

            reader = PdfReader(uploaded_file)

            for page in reader.pages:

                text = page.extract_text()

                if text:

                    resume_text += text

        st.text_area(
            "Resume Content",
            resume_text,
            height=250
        )

    else:

        resume_text = st.text_area(
            "Paste your resume here",
            height=250
        )

    if st.button("Analyze Resume"):

        if resume_text.strip() == "":

            st.warning(
                "Please upload or paste your resume."
            )

        else:

            with st.spinner("Analyzing Resume..."):

                if client is None:

                    st.error(
                        "Groq API Key not found. Please add GROQ_API_KEY in Streamlit Secrets."
                    )

                else:

                    response = client.chat.completions.create(

                        model="llama-3.3-70b-versatile",

                        messages=[

                            {

                                "role":"system",

                                "content":"""

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

                                "role":"user",

                                "content":resume_text

                            }

                        ]

                    )

                    answer = response.choices[0].message.content

                    st.subheader(
                        "AI Resume Analysis"
                    )

                    st.write(answer)

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

    
