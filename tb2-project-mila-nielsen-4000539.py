import streamlit as st
import random
import time
from PIL import Image

st.set_page_config(page_title="Knitting Journal", layout="wide")


if "users" not in st.session_state:
    st.session_state.users = {}
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# add a home page
def home_page():
    st.header("", divider="rainbow")
    st.markdown(f"<h4 style='text-align: center; color:#8CC1E1; '> WELCOME TO YOUR</h4>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color:#01466F; '>⭐️KNITTING JOURNAL⭐️</h1>", unsafe_allow_html=True)
    st.write(" ")
    st.markdown(f"<h5 style='text-align: center; color:#257CB0; '>IN THIS JOURNAL YOU CAN TRACK YOUR OWN PROJECTS AND LOOK AT ALL OF YOUR PREVIOUS KNITS</h5>",
                unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color:#257CB0; '>YOU CAN ALSO GET NEW INSPIRATION AND USEFUL TIPS FOR KNITTING OR TRY OUR PROJECTS GENERATOR!</h5>",
        unsafe_allow_html=True)

    # use columns to adjust button placement
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
    with col5:
        if st.button("LOG IN"):
            st.session_state.page = "Log In"
            st.rerun()

    st.header("", divider="rainbow")


# add log in page
def log_in_page():
    st.header("", divider="rainbow")
    st.title("Log In")
    with st.form("log_in_form"):
        st.subheader("Access your account")
        user_name = st.text_input("Enter your user name")
        password = st.text_input("Password", type="password")
        log_in_submit = st.form_submit_button("Log In")
    if log_in_submit:
        if len(user_name) < 1 or len(password) < 1:
            st.error("Please fill in all fields.")
        elif user_name not in st.session_state.users or st.session_state.users[user_name] != password:
            st.error("Invalid username or password. Please try again or create an account.")
        else:
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.page = "Dashboard"
            st.rerun()
    if st.button("Create an account"):
        st.session_state.page = "Sign In"
        st.rerun()

    st.header("", divider="rainbow")


# add create account page
def create_account_page():
    st.header("️", divider="rainbow")
    st.title("Create an account")
    with st.form("create_account_form"):
        st.subheader("Create a new account")
        user_name = st.text_input("Enter a user name")
        password = st.text_input("Password", type="password")
        repeat_password = st.text_input("Repeat Password", type="password")
        create_account_submit = st.form_submit_button("Create an account")
    if create_account_submit:
        if len(password) < 1:
            st.error("Please enter a password.")
        elif password != repeat_password:
            st.error("Passwords do not match.")
        elif len(user_name) < 1:
            st.error("Please enter a username.")
        elif user_name in st.session_state.users:
            st.error("Username already exists. Please choose a different username.")
        else:
            st.session_state.users[user_name] = password
            st.success("Account created successfully! You can now log in.")
            st.session_state.page = "Log In"
            st.rerun()
    if st.button("Go to Log In"):
        st.session_state.page = "Log In"
        st.rerun()

    st.header("", divider="rainbow")


# add dashboard page with all the features in the sidebar
def dashboard_page():
    # adjust color of sidebar
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-color: #ACCBDD;
                padding: 10px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # add different features to the sidebar
    page_selection = st.sidebar.radio("",["Diary", "Projects", "Project Generator", "Inspiration", "Tips & Tricks", "Log Out"])

    if page_selection == "Diary":
        diary_page()
    elif page_selection == "Projects":
        projects_page()
    elif page_selection == "Project Generator":
        generator_page()
    elif page_selection == "Inspiration":
        inspiration_page()
    elif page_selection == "Tips & Tricks":
        tips_tricks_page()
    elif page_selection == "Log Out":
        log_out_page()

    st.header("", divider="rainbow")


# add diary page
def diary_page():
    st.header("", divider="rainbow")
    st.markdown("<h1 style='text-align: center; color:#01466F; '>💫Diary💫</h1>️", unsafe_allow_html=True)
    if "diary_entries" not in st.session_state:
        st.session_state.diary_entries = []

    diary_entry = st.text_area("Write about your project:")

    if st.button("Save"):
        if diary_entry.strip():
            st.session_state.diary_entries.append(diary_entry)
            st.rerun()


# add project page
def projects_page():
    st.header("", divider="rainbow")
    st.markdown("<h1 style='text-align: center; color: #01466F; '>✨Projects✨</h1>️", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #257CB0; '>look at your previous projects</h4>️", unsafe_allow_html=True)

    if "diary_entries" in st.session_state and st.session_state.diary_entries:
        for entry in reversed(st.session_state.diary_entries):
            st.info(entry)
    else:
        st.info("No entry saved yet. Make your first entry in your diary :)")
    # add file_uploader to upload own images of knits
    uploaded_files = st.file_uploader("Upload a picture of your project:", type=["jpg", "jpeg", "png"],
                                      accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Uploaded images:")
        # adjusts the size and position of images
        col = st.columns(2)

        for idx, uploaded_file in enumerate(uploaded_files):
            image = Image.open(uploaded_file)

            max_width = 300
            image.thumbnail((max_width, max_width))

            with col[idx % 2]:
                st.image(image, caption=uploaded_file.name, use_column_width=False)


# add generator page
def generator_page():
    st.header("", divider="rainbow")
    st.markdown("<h1 style='text-align: center; color: #01466F;'>💫Project Generator💫️</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #257CB0;'>press buttons to generate a project!</h4>",
                unsafe_allow_html=True)

    # List of possible projects and colors
    projects = ['scarf', 'gloves', 'sweater', 'bag', 'socks', 'fingerless gloves', 'gauntlets', 'cushion', 'dishcloth',
                'headband', 'sweater vest', 'knitted flowers']
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black",
              "gray", "cyan", "magenta", "lime", "olive", "maroon", "navy", "teal", "turquoise", "gold",
              "silver", "beige", "coral", "ivory", "lavender", "peach", "salmon", "violet", "indigo", "crimson"]

    if "project" not in st.session_state:
        st.session_state.project = ""
    if "color" not in st.session_state:
        st.session_state.color = ""

    # add columns to make the buttons symmetrical
    col1, col2, col3 = st.columns([3, 2, 3])

    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        color_button, project_button = st.columns(2)

        with color_button:
            if st.button("Choose a Color🎨!", key="color_button"):
                time.sleep(1)
                st.session_state.color = random.choice(colors)

        with project_button:
            if st.button("Choose a Project✨!", key="project_button"):
                time.sleep(1)
                st.session_state.project = random.choice(projects)

    # add a field for the results: background color matches the selected color and writes the color and project
    st.markdown(
        f"<div style='text-align: center; background-color: {st.session_state.color}; padding: 15px; border-radius: 10px;'>"
        f"<h2 style='color: white;'>Your new project:</h2>"
        f"<p style='font-size: 24px; color: white;'>Create a {st.session_state.color} {st.session_state.project}!</p>"
        "</div>", unsafe_allow_html=True)


# add inspiration page
def inspiration_page():
    st.header("", divider="rainbow")
    st.markdown("<h1 style='text-align: center; color: #01466F; '>✨Inspiration✨</h1>️", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #257CB0;'>get inspired</h4", unsafe_allow_html=True)

    # add columns for inspiration pictures
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("scarf-picture.jpeg", caption="Cozy Scarf", use_column_width=True)

    with col2:
        st.image("beanie-picture.jpeg", caption="Winter Beanie", use_column_width=True)

    with col3:
        st.image("pullover.jpeg", caption="Pullover", use_column_width=True)

    with col4:
        st.image("gloves.jpeg", caption="full-fingered Gloves", use_column_width=True)

    # add another row of columns for instructions
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**Difficulty:** Beginner")
        if st.button("press for instructions"):
            st.markdown("""
                    ### **Beginner Knitting Pattern: Cozy Scarf 🧣**  

                **Materials Needed:**  
                - Medium-weight yarn (200g)  
                - Size 8-10 (US) / 5-6mm knitting needles  
                - Scissors & Tapestry Needle  

                **Instructions:**  
                **1. Cast On:** Cast on **30 stitches**.  
                **2. Knit Every Row:** Knit every stitch until the scarf is about **150 cm (60 inches)**.  
                **3. Bind Off:** Bind off all stitches loosely.  
                **4. Weave in Ends:** Use a tapestry needle to hide loose ends.  
                **5. Optional:** Add fringe for a stylish touch!  

                 **Your scarf is ready to wear!🌈**  
                    """)
            # add button to hide instructions again (same in the following)
            hide_button = st.button("Hide instructions")
            if hide_button:
                st.markdown("")

    with col2:
        st.markdown("**Difficulty:** Beginner ")
        if st.button("press for instructions", key="Button2"):
            st.markdown("""
                    ### **Beginner Knitting Pattern: Cozy Beanie 🧶**  

            **Materials Needed:**  
            **- Yarn:** Chunky or worsted-weight yarn (approx. 100g)  
            **- Needles:** Size 8-10 (US) / 5-6mm circular or double-pointed needles  
            **- Scissors & Tapestry Needle**  

            **Instructions**  
            **1. Cast On:**  
               - Cast on **80 stitches** (adjust for head size).  
               - Join in the round, being careful not to twist stitches.  

            **2. Ribbing:**  
               - Knit in **K1, P1 rib stitch** for **5 cm (2 inches)**.  

            **3. Body:**  
               - Switch to stockinette stitch (**knit every round**) until the hat is **15-18 cm (6-7 inches)** tall.  

            **4. Decrease for Crown:**  
               - *Round 1:* **Knit 8, k2tog** (repeat around).  
               - *Round 2:* Knit all stitches.  
               - *Round 3:* **Knit 7, k2tog** (repeat around).  
               - Continue decreasing every other row until only **8 stitches remain**.  

            **5. Finish:**  
               - Cut yarn, thread through remaining stitches, and pull tight.  
               - Weave in ends with a tapestry needle.  

            **Your beanie is ready to wear️!☃️**  
                    """)
            hide_button2 = st.button("Hide instructions")
            if hide_button2:
                st.markdown("")

    with col3:
        st.markdown("**Difficulty:** Intermediate ")
        if st.button("press for instructions", key="Button3"):
            st.markdown("""
                    ### **Intermediate Knitting Pattern: Pullover🧶**  

                **Materials Needed:**  
                - Medium-weight yarn (600-1000g)  
                - Circular needles (4-5mm) 
                - Stitchmarkers
                - Scissors & Tapestry Needle  

                **Instructions:**  
                **1. Cast On:** - 160-200 sts (adjust for size), join in the round
                                - work 5 cm in garter stitch or twisted rib
                **2. Body:** - switch to stockinette stitch
                             - knit until body measures 35-45cm, then place sleeve stitches on waste yarn
                **3. Divide for Sleeves:** - continue knitting the body for another 5-10cm, then bind off
                **4. Sleeves:** - pick up sleeve stitches, knit in stockinette until 40cm
                                - finish with garter stitch for 5cm, then bind off
                **5. Neckline:** - pick up stitches, knit 2-4cm in garter or rolled edge, then bind off
                **6. Finishing:** - weave in the ends, block lightly

                **Your pullover is ready to wear!❄️**  
                    """)
            hide_button3 = st.button("Hide instructions")
            if hide_button3:
                st.markdown("")

    with col4:
        st.markdown("**Difficulty:** Advanced ")
        if st.button("press for instructions", key="Button4"):
            st.markdown("""
                   ### **Advanced Knitting Pattern: Full-fingered Gloves🧤**  

               **Materials Needed:**  
               - light-weight yarn (50-100g)  
               - double-pointed needles or circular needles (2.5-3.5mm) 
               - Stitchmarkers 
               - Scissors & Tapestry Needle  

               **Instructions:**  
               **1. Cast On:** 48-60 sts (adjust for size), join in the round.  
               **2. Cuff:** Knit K2, P2, rib for 5cm.  
               **3. Hand:** Switch to stockinette (knit all rounds) for 5-7cm.  
               **4. Thumb Gusset:** Increase stitches every 2 rounds until 18-20 sts, then place them on waste yarn.
               **5. Fingers:** - divide stitches into 4 sections for fingers 
                               - knit each finger 5-7cm (until fully covered)
                               - bind off loosely for comfort
               **6. Thumb:** Pick up thumb stitches, knit 5-6cm, bind off.
               **7. Finishing:** Weave in the ends, block lightly for a perfect fit.

               **Your full-fingered gloves are ready to wear!❄️**  
                   """)
            hide_button4 = st.button("Hide instructions")
            if hide_button4:
                st.markdown("")

    # add file_uploader to be able to upload own instructions
    uploaded_files = st.file_uploader("Upload your own instructions:", accept_multiple_files=True,
                                      type=["jpg", "jpeg", "png", "pdf"])

    for uploaded_file in uploaded_files:
        # opens image
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

        # adds a button to download the pdf
        elif uploaded_file.type == "application/pdf":
            st.download_button(label="Download PDF", data=uploaded_file, file_name=uploaded_file.name)
            st.write(f"**PDF File**: {uploaded_file.name}")


# add page for tips and tricks
def tips_tricks_page():
    st.header("", divider="rainbow")
    st.markdown("<h1 style='text-align: center; color: #01466F; '>💫Tips & Tricks💫</h1>️", unsafe_allow_html=True)
    tips = [
        "Always check your gauge before starting a project.",
        "Use stitch markers to keep track of pattern repeats.",
        "Invest in good quality yarn for better results.",
        "Block your finished projects to enhance their appearance.",
    ]
    for tip in tips:
        st.info(tip)


# add log out page that leads back to home page when pressing log out button
def log_out_page():
    st.header("", divider="rainbow")
    st.markdown("<h3 style='text-align: center; color:#8CC1E1; '>SEE YOU NEXT TIME!</h3>️", unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
    with col5:
        log_out_button = st.button("LOG OUT")
        if log_out_button:
            st.session_state.logged_in = False
            st.session_state.page = "Home"
            st.rerun()

# main logic for app
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Log In":
    log_in_page()
elif st.session_state.page == "Sign In":
    create_account_page()
elif st.session_state.logged_in:
    dashboard_page()
