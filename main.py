
"""Explore UD: a beginner-friendly University of Delaware guide built with Drafter.

Student project. Cost entries are user-provided estimates, not official UD rates.
The activity list is an example; it is not an official list of UD organizations.
"""

from dataclasses import dataclass
from drafter import *


# Website information
set_website_title("Explore UD")
set_site_information(
    author="Justin Singley",
    description="Explore UD: costs, campus life, and activities for future students.",
    sources="University of Delaware official website: https://www.udel.edu/;, ChatGPT LLM",
    planning="Copy of CS1 Final project 0_Pick a Problem.docx, CS1 Final Project 1_Design.docx, Website Flowchart.pdf",
    links=["https://www.udel.edu/"]
)

set_website_framed(False)

# Uncomment after finishing debugging:
# hide_debug_information()


@dataclass
class Interest:
    """An example activity a visitor can choose to save."""
    name: str
    category: str
    saved: bool


@dataclass
class State:
    """Store values that remain available across pages."""
    student_name: str
    residency: str
    estimated_cost: float
    interests: list[Interest]
    feedback_message: str


def make_starting_state() -> State:
    """Create a new visitor with six example activities."""
    return State(
        student_name="",
        residency="In-State",
        estimated_cost=0.0,
        interests=[
            Interest("Club Sports", "Sports", False),
            Interest("Student Government", "Leadership", False),
            Interest("Engineering Clubs", "Academics", False),
            Interest("Community Service", "Volunteering", False),
            Interest("Music and Arts", "Arts", False),
            Interest("Outdoor Activities", "Recreation", False)
        ],
        feedback_message=""
    )


def navigation() -> list:
    """Provide navigation links to all main pages."""
    return [
        HorizontalRule(),
        Button("Home", "index"),
        Button("View Tuition", "cost"),
        Button("Explore Housing", "housing"),
        Button("Discover Student Life", "student_life"),
        Button("Browse Activities", "activities"),
        Button("View Favorites", "saved_interests"),
        Button("Leave Feedback", "feedback"),
        Button("About This Website", "about")
    ]


@route
def about(state: State) -> Page:
    """Show the project information and planning documents."""
    return Page(state, [
        Header("About Explore UD"),

        Header("Description", 2),
        Paragraph("Explore UD: costs, campus life, and activities for future students."),

        Header("Sources", 2),
        Paragraph("University of Delaware official website and ChatGPT LLM."),
        Link("University of Delaware Official Website", "https://www.udel.edu/"),

        Header("Planning", 2),
        Paragraph("1. Copy of CS1 Final project 0_Pick a Problem.docx"),
        Paragraph("2. CS1 Final Project 1_Design.docx"),
        Paragraph("3. Website Flowchart.pdf"),

        Paragraph("These planning files are uploaded in the GitHub repository."),
        Link("View Project Repository", "https://github.com/JustinSingley/UD-Website")

    ] + navigation())


@route
def index(state: State) -> Page:
    """Display the welcome page and allow visitors to enter their name."""
    greeting = "Welcome to Explore UD!"

    if state.student_name != "":
        greeting = "Welcome, " + state.student_name + "!"

    return Page(state, [
        Header("Explore UD"),
        Header(greeting, 2),

        "Learn about costs, campus living, student life, and activities at UD.",

        "What is your name?",
        TextBox("new_name", state.student_name),
        Button("Save Name", "save_name"),

        Header("Choose a page to explore", 2)

    ] + navigation())


@route
def save_name(state: State, new_name: str) -> Page:
    """Save a visitor's name and return to the homepage."""
    state.student_name = new_name.strip()
    return index(state)


@route
def cost(state: State) -> Page:
    """Show a cost calculator using visitor-provided estimates."""
    contents = [
        Header("Cost of Attendance"),

        "Use your own annual estimates. These are NOT official UD prices.",

        "Where do you live?",
        SelectBox("new_residency", ["In-State", "Out-of-State"], state.residency),

        "Your estimated yearly tuition and fees ($):",
        TextBox("tuition", 0, "number"),

        "Your estimated yearly housing, meals, and other costs ($):",
        TextBox("other_costs", 0, "number"),

        Button("Calculate Cost", "calculate_cost")
    ]

    if state.estimated_cost > 0:
        contents.append(
            "Your estimated yearly total: $" +
            format(state.estimated_cost, ",.2f")
        )
        contents.append("Residency: " + state.residency)

    contents.append("Check udel.edu for up-to-date tuition and housing prices.")

    return Page(state, contents + navigation())


@route
def calculate_cost(state: State, new_residency: str,
                   tuition: float, other_costs: float) -> Page:
    """Validate and calculate estimated yearly costs."""

    if tuition < 0 or other_costs < 0:
        return Page(state, [
            Header("Please check your costs"),
            "Costs cannot be negative.",
            Button("Try Again", "cost")
        ] + navigation())

    state.residency = new_residency
    state.estimated_cost = tuition + other_costs

    return cost(state)


@route
def housing(state: State) -> Page:
    """Introduce housing and dining at UD."""
    return Page(state, [
        Header("Campus Living"),

        Header("Housing", 2),
        "Residence halls are one way to live near classes and meet new people.",

        Header("Dining", 2),
        "Students can explore dining halls, meal plans, and other dining options.",

        "Confirm options and policies on UD's official housing and dining pages."

    ] + navigation())


@route
def student_life(state: State) -> Page:
    """Describe student life at UD."""
    return Page(state, [
        Header("Life as a Blue Hen"),

        "There are campus traditions, sporting events, and ways to meet people.",

        Header("Campus Experience", 2),
        "Students can spend time on The Green and explore campus events.",

        Header("Sports", 2),
        "Visitors can learn about Blue Hens teams and school spirit.",

        Button("Find Activities", "activities")

    ] + navigation())


@route
def activities(state: State) -> Page:
    """Display activities with checkboxes for saving favorites."""
    contents = [
        Header("Get Involved"),
        "Choose activities that sound interesting, then select Save My Interests."
    ]

    for activity in state.interests:
        contents.append(
            RelatedCheckBox("selected", activity.name, activity.saved)
        )
        contents.append(
            activity.name + " (" + activity.category + ")"
        )

    contents.append(
        Button("Save My Interests", "save_activities")
    )

    return Page(state, contents + navigation())


@route
def save_activities(state: State, selected: list[str]) -> Page:
    """Update the visitor's saved activities."""

    for activity in state.interests:
        if activity.name in selected:
            activity.saved = True
        else:
            activity.saved = False

    return saved_interests(state)


@route
def saved_interests(state: State) -> Page:
    """Show the visitor's saved activities."""
    contents = [
        Header("My UD List"),
        "Activities you saved:"
    ]

    saved_count = 0

    for activity in state.interests:
        if activity.saved:
            contents.append(
                activity.name + " - " + activity.category
            )
            saved_count = saved_count + 1

    if saved_count == 0:
        contents.append(
            "You have not saved any activities yet."
        )

    contents.append(
        Button("Browse More Activities", "activities")
    )

    return Page(state, contents + navigation())


@route
def feedback(state: State) -> Page:
    """Allow visitors to leave feedback."""
    contents = [
        Header("Share Your Thoughts"),

        "What else would you like to know about UD?",

        TextArea("new_feedback", state.feedback_message),

        Button("Submit Feedback", "submit_feedback")
    ]

    if state.feedback_message != "":
        contents.append(
            "Your saved feedback: " + state.feedback_message
        )

    return Page(state, contents + navigation())


@route
def submit_feedback(state: State, new_feedback: str) -> Page:
    """Reject blank feedback or save a visitor's message."""

    if new_feedback.strip() == "":
        return Page(state, [
            Header("Feedback Needed"),
            "Please write something before submitting.",
            Button("Try Again", "feedback")
        ] + navigation())

    state.feedback_message = new_feedback.strip()

    return Page(state, [
        Header("Thanks for your feedback!"),

        "Your message is saved during this visit, not sent to UD.",

        Button("Back to Feedback", "feedback")

    ] + navigation())


# UNIT TESTS
# Tests run before starting the website.

assert_has(index(make_starting_state()), "Welcome to Explore UD!")

assert_has(about(make_starting_state()), "About Explore UD")

assert_state(
    save_name(make_starting_state(), "  Alex  "),
    State("Alex", "In-State", 0.0, make_starting_state().interests, "")
)

assert_has(cost(make_starting_state()), "Cost of Attendance")

assert_equal(
    calculate_cost(
        make_starting_state(),
        "Out-of-State",
        20000.0,
        15000.0
    ).state.estimated_cost,
    35000.0
)

assert_equal(
    calculate_cost(
        make_starting_state(),
        "Out-of-State",
        -1.0,
        500.0
    ).state.estimated_cost,
    0.0
)

assert_has(housing(make_starting_state()), "Residence halls")

assert_has(student_life(make_starting_state()), "Life as a Blue Hen")

assert_has(activities(make_starting_state()), "Club Sports")

assert_equal(
    save_activities(
        make_starting_state(),
        ["Club Sports"]
    ).state.interests[0].saved,
    True
)

assert_has(
    saved_interests(make_starting_state()),
    "You have not saved any activities yet."
)

assert_has(feedback(make_starting_state()), "Share Your Thoughts")

assert_equal(
    submit_feedback(
        make_starting_state(),
        "  Nice website!  "
    ).state.feedback_message,
    "Nice website!"
)

assert_equal(
    submit_feedback(
        make_starting_state(),
        "  "
    ).state.feedback_message,
    ""
)


# Start the website
start_server(make_starting_state())
