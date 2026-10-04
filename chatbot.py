import random

# ============================================================
# SAHAARA — Student Stress Relief Chatbot
# ============================================================

DATA = {
    "exams": (
        [
            "Exam pressure can make the whole syllabus feel like an emergency, but you only need to handle one piece at a time.",
            "One exam is an event, not a definition of your ability.",
            "You can take academics seriously without treating every paper like a verdict on your future."
        ],
        [
            "Make a must-do / should-do / can-wait list.",
            "Choose one chapter or question type and work on it for 20–30 minutes.",
            "Use active recall or practice questions instead of only rereading.",
            "Do one timed practice set and review the mistakes.",
            "Protect your sleep instead of trying to learn everything at the last minute."
        ]
    ),

    "marks": (
        [
            "A mark is information about one assessment, not a measurement of your entire worth.",
            "It is okay to be disappointed without deciding that you are incapable.",
            "A disappointing result can become useful once you identify exactly where the marks went."
        ],
        [
            "Separate mistakes caused by knowledge gaps from careless errors.",
            "Make a short error list and revise those areas first.",
            "Compare your current work with your own previous work rather than someone else's score.",
            "Ask your teacher about anything you genuinely do not understand.",
            "Give yourself time to process the result before making big conclusions."
        ]
    ),

    "study": (
        [
            "You do not need to study perfectly. You need a method you can actually repeat.",
            "A huge syllabus becomes less scary when it becomes one small task.",
            "A short focused session is more useful than hours of panicked staring at notes."
        ],
        [
            "Write the exact topic you will finish in the next 20–30 minutes.",
            "Use questions, flashcards or active recall to check what you actually know.",
            "Keep your phone physically away during the study block.",
            "Take a proper short break instead of scrolling while pretending to study.",
            "Stop trying to make the timetable perfect and make it realistic."
        ]
    ),

    "deadlines": (
        [
            "Several deadlines together can make everything feel urgent at once.",
            "You do not have to mentally carry every unfinished task simultaneously.",
            "The goal is to reduce the pile one task at a time."
        ],
        [
            "Write every deadline down with its actual due date.",
            "Do the nearest important deadline first.",
            "Break a large assignment into the smallest possible first step.",
            "If a deadline is genuinely impossible, communicate early instead of disappearing.",
            "Submit solid work rather than exhausting yourself chasing perfection."
        ]
    ),

    "procrastination": (
        [
            "Procrastination often means the task feels too large, unclear or uncomfortable, not that you are simply lazy.",
            "You do not need motivation before starting.",
            "Make the first step so small that your brain has very little to argue with."
        ],
        [
            "Use a five-minute start.",
            "Open the exact book, document or question before starting the timer.",
            "Remove one distraction instead of trying to become perfectly disciplined.",
            "Choose one tiny completed task before planning the rest of the day.",
            "Once you start, continue only if it feels manageable."
        ]
    ),

    "focus": (
        [
            "Stress and mental overload can make concentration much harder.",
            "You do not need perfect focus; you need a short period of useful focus.",
            "If your brain is scattered, make the task smaller."
        ],
        [
            "Put the phone in another room or out of reach.",
            "Work in a short focused block followed by a planned break.",
            "Keep only the material needed for the current task visible.",
            "Write distracting thoughts on paper so you do not have to hold them in your head.",
            "Check whether poor sleep or exhaustion is making concentration worse."
        ]
    ),

    "memory": (
        [
            "Forgetting after studying does not mean you are bad at learning.",
            "Memory improves when you retrieve information instead of only rereading it.",
            "Stress and lack of sleep can make recall feel much worse."
        ],
        [
            "Close the book and explain the concept from memory.",
            "Use practice questions to find the exact gaps.",
            "Review difficult information again after a gap rather than cramming it repeatedly.",
            "Make short links between concepts instead of memorising isolated sentences.",
            "Protect sleep before an important exam."
        ]
    ),

    "parents": (
        [
            "Parent pressure can feel especially intense because their opinion matters to you.",
            "You can understand your parents' hopes without making their expectations your entire identity.",
            "You deserve support while you are figuring things out."
        ],
        [
            "Talk when everyone is calmer, not during an argument.",
            "Explain one specific effect of the pressure rather than listing everything.",
            "Show a realistic plan if your parents are worried about your work.",
            "Ask for one concrete change, such as uninterrupted study time.",
            "If conversations repeatedly become overwhelming, involve a trusted teacher or counsellor."
        ]
    ),

    "friends": (
        [
            "That sounds hurtful. Someone being mean does not automatically mean there is something wrong with you.",
            "You deserve friendships where respect goes both ways.",
            "You can care about someone and still decide that their behaviour is not okay."
        ],
        [
            "Look at the pattern rather than one isolated moment.",
            "If it feels safe, explain the specific behaviour that hurt you.",
            "Do not send a long angry message immediately; give yourself time first.",
            "Spend more time around people who treat you well.",
            "If bullying or harassment is involved, tell a trusted adult rather than handling it alone."
        ]
    ),

    "bullying": (
        [
            "Being bullied is not something you have to solve by yourself.",
            "Someone else's behaviour does not define your worth.",
            "You deserve to feel safe at school and online."
        ],
        [
            "Tell a parent, teacher, counsellor or another trusted adult.",
            "Save evidence of serious online harassment.",
            "Block, mute or report abusive accounts when appropriate.",
            "Stay around supportive people instead of isolating yourself.",
            "If you feel unsafe, prioritise getting to a safe adult or place."
        ]
    ),

    "lonely": (
        [
            "Loneliness can make the world feel much smaller than it really is.",
            "Being lonely right now does not mean you will always be lonely.",
            "You do not need a huge friend group to feel connected."
        ],
        [
            "Message one person you already feel reasonably comfortable with.",
            "Join a shared-interest activity where conversation happens naturally.",
            "Aim for one genuine interaction instead of trying to become popular.",
            "Spend time in places where you naturally encounter people.",
            "Tell a trusted adult if loneliness is becoming overwhelming."
        ]
    ),

    "overthinking": (
        [
            "Overthinking can feel like problem-solving even when the same thought is simply going in circles.",
            "A possibility is not the same thing as a fact.",
            "You do not have to solve your entire future tonight."
        ],
        [
            "Write the thought down and label it fact, possibility or fear.",
            "Ask what action is actually available right now.",
            "If there is no action available, give yourself permission to pause it.",
            "Avoid repeatedly checking messages or social media for reassurance.",
            "Do something concrete and ordinary to bring attention back to the present."
        ]
    ),

    "future": (
        [
            "Not knowing your entire future is normal, especially while you are still in school.",
            "You do not need a perfect five-year plan to make a good next decision.",
            "Your future is built through many smaller decisions."
        ],
        [
            "Separate decisions that need to happen now from decisions that can wait.",
            "Research real courses and career paths rather than trying to predict everything.",
            "Keep more than one option open while you gather information.",
            "Talk to a teacher, counsellor or trusted adult with relevant experience.",
            "Choose the next useful step rather than demanding certainty."
        ]
    ),

    "career": (
        [
            "Career confusion does not mean you are behind.",
            "You do not need one magical answer immediately.",
            "It is okay for your plan to change as you learn more."
        ],
        [
            "List subjects and activities you genuinely enjoy.",
            "Research the actual courses and requirements for possible paths.",
            "Write down several realistic options instead of forcing one answer.",
            "Talk to people who actually study or work in those fields.",
            "Give yourself a deadline for researching, then choose a next step."
        ]
    ),

    "college": (
        [
            "College applications can make the future feel extremely immediate.",
            "You do not have to solve your whole adult life through one application."
        ],
        [
            "Make a checklist of documents and deadlines.",
            "Handle one application step at a time.",
            "Keep backup options so one result does not feel like the only possible future.",
            "Avoid comparing your entire future with someone else's college announcement.",
            "Ask a trusted adult or counsellor about confusing requirements."
        ]
    ),

    "sleep": (
        [
            "Poor sleep can make every other stressor feel louder.",
            "Rest is not laziness; it is part of being able to function.",
            "You do not have to solve tomorrow's problems from bed."
        ],
        [
            "Keep your wake-up time reasonably consistent.",
            "Reduce stimulating screens before bed.",
            "If you cannot sleep for a long time, switch to something quiet instead of repeatedly checking the clock.",
            "Avoid turning bedtime into another study session.",
            "If sleep problems keep affecting daily life, tell a trusted adult or healthcare professional."
        ]
    ),

    "anxiety": (
        [
            "Anxiety can make a possibility feel like a certainty.",
            "You do not have to obey every alarming thought.",
            "When your body feels stressed, slowing things down can help you think more clearly."
        ],
        [
            "Take a few slow breaths and relax your shoulders.",
            "Write down what you can control and what you cannot.",
            "Reduce immediate stimulation if possible.",
            "Do one ordinary grounding activity such as washing your face, walking or organising your desk.",
            "If anxiety repeatedly interferes with school, sleep or daily life, talk to a trusted adult or professional."
        ]
    ),

    "low_mood": (
        [
            "You do not have to pretend to be cheerful when you are having a low day.",
            "A difficult mood does not automatically predict your future.",
            "You are allowed to need support."
        ],
        [
            "Keep one or two basic routines going.",
            "Talk to someone you trust instead of isolating yourself.",
            "Change your environment for a little while.",
            "Do one small manageable activity rather than demanding a productive day.",
            "If low mood persists or seriously affects daily life, tell a trusted adult or professional."
        ]
    ),

    "family": (
        [
            "Family stress is exhausting because home is also where you are supposed to recover.",
            "You do not have to solve every family problem yourself.",
            "Your wellbeing matters alongside your responsibilities."
        ],
        [
            "Choose a calm time for difficult conversations.",
            "Focus on one specific problem.",
            "Write your thoughts down before talking if that helps.",
            "Ask a trusted adult outside the conflict for perspective.",
            "Take some space after a heated argument before trying to solve it."
        ]
    ),

    "perfectionism": (
        [
            "Perfectionism can make good work feel like failure.",
            "You do not need to make everything flawless to make it valuable.",
            "A finished good piece of work is more useful than a perfect piece that never gets finished."
        ],
        [
            "Define 'good enough' before starting.",
            "Set a time limit for polishing.",
            "Ask whether another hour will actually change the result.",
            "Allow ordinary mistakes while learning.",
            "Finish when the important requirements are met."
        ]
    ),

    "health": (
        [
            "Health worries deserve attention without immediately assuming the worst.",
            "Stress can affect how you feel physically, but persistent symptoms should not simply be dismissed as stress."
        ],
        [
            "Tell a trusted adult if a health concern is worrying you.",
            "Keep a simple note of symptoms and when they occur.",
            "Avoid diagnosing yourself from random internet posts.",
            "Prioritise reasonable sleep, food, hydration and rest.",
            "For severe, persistent or disruptive symptoms, seek appropriate medical care."
        ]
    ),

    "generic": (
        [
            "That sounds like a lot to carry. You do not have to solve everything at once.",
            "A stressful moment can make everything feel urgent, even when only a few things need attention now.",
            "You can take your feelings seriously without treating every stressed thought as a fact."
        ],
        [
            "Write the exact problem in one sentence.",
            "Separate what you can control from what you cannot.",
            "Choose one small action you can complete today.",
            "Take a short break if you are overwhelmed.",
            "Talk to a trusted adult, teacher, counsellor or friend if the problem is becoming too much to carry alone."
        ]
    )
}


KEYWORDS = {
    "exams": ["exam", "exams", "test", "tests", "board", "boards", "preboard", "paper"],
    "marks": ["mark", "marks", "score", "result", "results", "percentage", "grade"],
    "study": ["study", "studying", "syllabus", "revision", "revise", "chapter", "homework"],
    "deadlines": ["deadline", "deadlines", "due", "backlog", "pending", "assignment"],
    "procrastination": ["procrastinat", "delaying", "putting off", "keep delaying", "can't start", "cannot start"],
    "focus": ["focus", "concentrate", "concentration", "distracted", "can't focus", "cannot focus"],
    "memory": ["forget", "forgot", "remember", "memory", "can't remember", "cannot remember"],
    "parents": ["parent", "parents", "mom", "mum", "dad", "mother", "father"],
    "friends": ["friend", "friends", "bestie", "classmate"],
    "bullying": ["bully", "bullied", "bullying", "harass", "harassment"],
    "lonely": ["lonely", "alone", "isolated", "no friends"],
    "overthinking": ["overthink", "overthinking", "can't stop thinking", "cannot stop thinking"],
    "career": ["career", "career choice", "career path"],
    "college": ["college", "university", "admission", "admissions"],
    "future": ["future", "what will happen", "what am i going to do"],
    "sleep": ["sleep", "insomnia", "can't sleep", "cannot sleep", "sleeping late"],
    "anxiety": ["anxiety", "anxious", "panic", "panicking", "nervous", "overwhelmed"],
    "low_mood": ["sad", "sadness", "low mood", "feeling low", "down", "unhappy"],
    "health": ["health", "sick", "ill", "illness", "doctor", "symptom"],
    "family": ["family", "home problem", "problem at home"],
    "perfectionism": ["perfect", "perfectionist", "perfectionism", "never good enough"]
}


def detect_category(message):
    text = message.lower()
    scores = {}

    for category, words in KEYWORDS.items():
        for word in words:
            if word in text:
                scores[category] = scores.get(category, 0) + len(word.split()) + 1

    # Specific situations get priority.
    if any(x in text for x in ["suicide", "kill myself", "want to die", "end my life"]):
        return "safety"

    if "friend" in text or "friends" in text:
        if any(x in text for x in ["mean", "rude", "ignore", "ignoring", "fight", "hurt", "toxic"]):
            return "friends"

    if "parent" in text or "parents" in text or "mom" in text or "dad" in text:
        return "parents"

    if "break" in text and "up" in text:
        return "breakup"

    if "social media" in text or "instagram" in text or "reels" in text:
        return "social"

    return max(scores, key=scores.get) if scores else "generic"


def safety_check(message):
    text = message.lower()

    phrases = [
        "kill myself",
        "want to die",
        "end my life",
        "suicide",
        "self harm",
        "self-harm",
        "hurt myself"
    ]

    return any(p in text for p in phrases)



def safety_response():
    responses = [
        (
            "I'm really sorry you're dealing with something this painful. "
            "Please tell a trusted adult right now, such as a parent, guardian, "
            "teacher, school counsellor or another adult you trust. "
            "Try to stay with someone rather than being alone. "
            "If you are in immediate danger, contact your local emergency service "
            "or go to the nearest emergency department."
        ),

        (
            "I'm really glad you said something instead of keeping this completely "
            "to yourself. Please reach out to a trusted adult right now and tell "
            "them honestly that you're not feeling safe. A parent, guardian, "
            "teacher, counsellor or another trusted adult can stay with you and "
            "help you get through this. If there is immediate danger, contact "
            "your local emergency service or go to the nearest emergency department."
        ),

        (
            "You don't have to handle a moment like this on your own. "
            "Please find a trusted adult and stay with them while you talk about "
            "what you're experiencing. You can start with something as simple as, "
            "\"I'm having a really difficult time and I need you to stay with me.\" "
            "If you're in immediate danger, contact your local emergency service "
            "or go to the nearest emergency department."
        ),

        (
            "What you're going through deserves real support, not something you "
            "have to carry silently. Please tell a parent, guardian, teacher, "
            "school counsellor or another adult you trust and stay around people "
            "who can support you. If you feel that you may be in immediate danger, "
            "contact your local emergency service or go to the nearest emergency "
            "department."
        ),

        (
            "Please pause everything else for a moment and reach out to someone "
            "you trust. You don't need to explain everything perfectly; you can "
            "simply tell them that you're struggling and need them to stay with "
            "you. If you're in immediate danger, contact your local emergency "
            "service or go to the nearest emergency department."
        ),

        (
            "I'm sorry that things feel this overwhelming right now. "
            "Please don't face this alone. Go to a trusted adult, tell them what "
            "you're experiencing, and stay with them. This could be a parent, "
            "guardian, teacher, school counsellor or another adult you trust. "
            "If there is immediate danger, contact your local emergency service "
            "or go to the nearest emergency department."
        ),

        (
            "You deserve support from a real person who can be with you right now. "
            "Please tell a trusted adult how serious things feel and ask them to "
            "stay with you. If talking feels difficult, you can simply show them "
            "this message. If you're in immediate danger, contact your local "
            "emergency service or go to the nearest emergency department."
        ),

        (
            "I'm here to listen, but this is something you shouldn't have to manage "
            "through a chatbot alone. Please reach out to a trusted adult right "
            "now and stay with someone you trust. If you're in immediate danger, "
            "contact your local emergency service or go to the nearest emergency "
            "department."
        )
    ]

    return random.choice(responses)

       

def basic_reply(message):
    text = message.lower().strip()

    if text in {"hi", "hello", "hey", "hii", "hiii","hie"}:
        return (
            "Hey! I'm Sahaara. Tell me what's stressing you out, "
            "and I'll help you break it down."
        )

    if text in {"bye", "goodbye", "good bye", "see you", "see ya", "cya","byeee","byee"}:
        return (
            "Bye! Take care, and remember to take things one step at a time. "
            "I'm here whenever you need to talk."
        )

    if text in {"thanks", "thank you", "thank u", "thx", "thankyouuuuu", "thankyouuu","thankyouu","thankyou"}:
        return (
            "You're welcome. Take it one step at a time. "
            "You do not have to solve everything at once."
        )

    if text in {"okay", "got it", "i understand", "yessss", "yes fine", "fine"}:
        return (
            "Anything else that bothers you?"
            "Remember you got this!"
        )

    return None


def generate_response(message, stress_level=None, previous_category=None):

    # Safety comes first.
    if safety_check(message):
        return safety_response()

    basic = basic_reply(message)

    if basic:
        return basic

    category = detect_category(message)

    # If the user gives a short follow-up such as
    # "yeah", "exactly", "that's the problem", keep the previous topic.
    if previous_category and category == "generic":
        category = previous_category

    calm, solutions = DATA.get(category, DATA["generic"])

    opening = random.choice(calm)

    # Mention the ML result only when it is useful.
    stress_note = ""

    if stress_level == "High":
        stress_note = (
            " Your stress assessment is currently on the higher side, "
            "so let's focus on reducing the immediate load rather than "
            "trying to fix everything at once."
        )

    elif stress_level == "Moderate":
        stress_note = (
            " Your assessment suggests some elevated stress, so it may "
            "help to deal with the biggest pressure point first."
        )

    # Pick varied suggestions.
    chosen = random.sample(
        solutions,
        min(3, len(solutions))
    )

    endings = [
        "For now, just take the next manageable step.",
        "You do not need to fix everything today.",
        "Let's make the problem smaller before trying to solve all of it.",
        "One difficult moment does not define your whole situation.",
        "Take it one step at a time and let the rest wait for a moment."
    ]

    answer = opening + stress_note

    answer += "\n\nHere are a few things you could try:"

    for i, item in enumerate(chosen, 1):
        answer += f"\n{i}. {item}"

    answer += "\n\n" + random.choice(endings)

    return answer


