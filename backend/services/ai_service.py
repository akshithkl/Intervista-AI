from openai import OpenAI
import os
import random
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

# Get OpenAI API key
api_key = os.getenv('OPENAI_API_KEY') or getattr(settings, 'OPENAI_API_KEY', None)

if not api_key:
    print("Warning: OPENAI_API_KEY not found. Please set it in your environment variables or .env file")
    print("Get your API key from: https://platform.openai.com/api-keys")

# Initialize OpenAI client with new API format
client = OpenAI(api_key=api_key) if api_key else None

# Fallback questions for when OpenAI API is not available
FALLBACK_QUESTIONS = {
    "Software Engineer": [
        "Explain the difference between a stack and a queue. When would you use each?",
        "What is the time complexity of binary search? Can you explain how it works?",
        "Describe the difference between SQL and NoSQL databases. When would you choose each?",
        "What is object-oriented programming? Explain the four main principles.",
        "How would you optimize a slow-running database query?",
        "Explain the difference between GET and POST HTTP methods.",
        "What is version control? Why is it important in software development?",
        "Describe the difference between frontend and backend development.",
        "What is an API? How do you design a RESTful API?",
        "Explain the concept of recursion with an example."
    ],
    "Frontend Developer": [
        "What is the difference between HTML, CSS, and JavaScript?",
        "Explain the box model in CSS. How does it affect layout?",
        "What is the difference between let, const, and var in JavaScript?",
        "How do you make a website responsive? What are media queries?",
        "Explain the difference between React and vanilla JavaScript.",
        "What is the Document Object Model (DOM)? How do you manipulate it?",
        "Describe the difference between inline and block elements in HTML.",
        "What are CSS flexbox and grid? When would you use each?",
        "Explain the concept of state in React applications.",
        "How do you handle user input and form validation in web applications?"
    ],
    "Backend Developer": [
        "What is the difference between a relational and non-relational database?",
        "Explain the concept of RESTful APIs. What are the main HTTP methods?",
        "What is authentication vs authorization? How do you implement them?",
        "Describe the MVC (Model-View-Controller) pattern.",
        "What is caching? How can it improve application performance?",
        "Explain the difference between synchronous and asynchronous programming.",
        "What is a microservice architecture? What are its benefits and challenges?",
        "How do you handle errors and exceptions in your applications?",
        "What is database normalization? Why is it important?",
        "Explain the concept of load balancing and why it's needed."
    ],
    "Data Scientist": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain the concept of overfitting in machine learning. How do you prevent it?",
        "What is the difference between correlation and causation?",
        "Describe the steps in a typical data science project workflow.",
        "What is feature engineering? Why is it important?",
        "Explain the difference between classification and regression problems.",
        "What is cross-validation? Why is it important in model evaluation?",
        "Describe the bias-variance tradeoff in machine learning.",
        "What is the difference between precision and recall?",
        "How do you handle missing data in your datasets?"
    ],
    "DevOps Engineer": [
        "What is CI/CD? How does it improve the software development process?",
        "Explain the difference between containers and virtual machines.",
        "What is infrastructure as code? What tools would you use?",
        "Describe the concept of monitoring and logging in production systems.",
        "What is load balancing? What are the different types?",
        "Explain the concept of blue-green deployment.",
        "What is Docker? How does it differ from traditional deployment?",
        "Describe the importance of security in DevOps practices.",
        "What is version control? How do you manage different environments?",
        "Explain the concept of scalability and how to achieve it."
    ],
    "Product Manager": [
        "How do you prioritize features in a product roadmap?",
        "What is the difference between a product manager and a project manager?",
        "How do you gather and analyze user feedback?",
        "Explain the concept of product-market fit.",
        "What is A/B testing? How do you design and interpret results?",
        "How do you work with engineering teams to deliver products?",
        "What is the difference between user stories and requirements?",
        "How do you measure product success? What metrics do you track?",
        "Describe your approach to competitive analysis.",
        "How do you handle conflicting stakeholder requirements?"
    ]
}

# Add this mapping for fallback correct answers:
FALLBACK_ANSWERS = {
    "Explain the difference between a stack and a queue. When would you use each?":
        "A stack is LIFO (Last-In, First-Out); a queue is FIFO (First-In, First-Out). Use a stack for undo features, a queue for task scheduling.",
    "What is the time complexity of binary search? Can you explain how it works?":
        "O(log n). Binary search repeatedly divides a sorted array in half to find a target value.",
    # ...add more for your fallback questions...
}

def evaluate_answer(question, user_answer, job_role):
    # Fallback: check if we have a correct answer for this question
    correct_answer = FALLBACK_ANSWERS.get(question)
    if correct_answer:
        if user_answer.strip().lower() == correct_answer.strip().lower():
            return "Correct! Your answer is accurate."
        else:
            return f"Incorrect. The correct answer is: {correct_answer}"
    # Otherwise, use OpenAI or fallback feedback as before
    if client:
        prompt = f"""
        Evaluate this interview answer:

        Question: {question}
        Answer: {user_answer}
        Job Role: {job_role}

        Provide constructive feedback on:
        1. Technical accuracy
        2. Clarity of explanation  
        3. Relevance to the question
        4. Areas for improvement

        Keep feedback concise and actionable.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical interview evaluator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "billing" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                print(f"OpenAI quota exceeded, using fallback feedback. Error: {error_msg}")
                return get_fallback_feedback()
            else:
                return f"Error evaluating answer: {error_msg}"

    return get_fallback_feedback()



FALLBACK_FEEDBACK = [
    "Good start! Consider providing more specific examples to strengthen your answer.",
    "Your answer shows understanding of the concept. Try to explain the practical applications as well.",
    "Well explained! You might want to mention the trade-offs or limitations of this approach.",
    "Good technical knowledge! Consider adding how this relates to real-world scenarios.",
    "Solid answer! You could enhance it by discussing best practices or common pitfalls.",
    "Nice explanation! Try to include performance considerations or optimization techniques.",
    "Good understanding! Consider mentioning alternative approaches or related concepts.",
    "Well done! You might want to add examples of when you've used this in practice.",
    "Good answer! Consider discussing the pros and cons of different approaches.",
    "Nice work! Try to explain how this concept fits into the bigger picture."
]

def generate_interview_question(job_role, experience_level="beginner", context=None):
    # Try OpenAI API first
    if client:
        prompt = f"""
        Generate a technical interview question for a {experience_level} {job_role} position.
        Make it practical and relevant to real-world scenarios.
        {f"Context: {context}" if context else ""}
        
        Return the question only, no additional text.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical interview coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota/billing error
            if "quota" in error_msg.lower() or "billing" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                print(f"OpenAI quota exceeded, using fallback questions. Error: {error_msg}")
                return get_fallback_question(job_role)
            else:
                return f"Error generating question: {error_msg}"
    
    # Fallback to predefined questions
    return get_fallback_question(job_role)

def get_fallback_question(job_role):
    """Get a random question from the fallback questions for the given job role"""
    # Try to find questions for the exact job role
    if job_role in FALLBACK_QUESTIONS:
        return random.choice(FALLBACK_QUESTIONS[job_role])
    
    # If exact match not found, try to find a similar role
    job_role_lower = job_role.lower()
    for role, questions in FALLBACK_QUESTIONS.items():
        if any(keyword in job_role_lower for keyword in role.lower().split()):
            return random.choice(questions)
    
    # Default to Software Engineer questions if no match found
    return random.choice(FALLBACK_QUESTIONS["Software Engineer"])

def evaluate_answer(question, user_answer, job_role):
    # Try OpenAI API first
    if client:
        prompt = f"""
        Evaluate this interview answer:
        
        Question: {question}
        Answer: {user_answer}
        Job Role: {job_role}
        
        Provide constructive feedback on:
        1. Technical accuracy
        2. Clarity of explanation  
        3. Relevance to the question
        4. Areas for improvement
        
        Keep feedback concise and actionable.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical interview evaluator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota/billing error
            if "quota" in error_msg.lower() or "billing" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                print(f"OpenAI quota exceeded, using fallback feedback. Error: {error_msg}")
                return get_fallback_feedback()
            else:
                return f"Error evaluating answer: {error_msg}"
    
    # Fallback to predefined feedback
    return get_fallback_feedback()

def get_fallback_feedback():
    """Get random feedback from the fallback feedback list"""
    return random.choice(FALLBACK_FEEDBACK)