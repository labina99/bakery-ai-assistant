# Sweet Crust Bakery AI Assistant

An AI-powered chatbot for a fictional bakery that lets customers place orders, ask about the menu, check opening hours, find the location, and request contact details — all using natural language.

Built with Python and Streamlit.

---

## Features

- **Natural language ordering** — customers describe their order in plain English and the assistant extracts the relevant details
- **Multi-turn conversation** — if information is missing, the assistant asks follow-up questions and merges responses into the order
- **Order editing** — customers can change any part of their order before confirming
- **FAQ responses** — handles questions about the menu, opening hours, location, and how to contact staff
- **Live order tracker** — sidebar shows which fields have been collected and which are still needed
- **Evaluation panel** — built-in test cases at the bottom of the app show how the order extractor performs

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/bakery-ai-assistant.git
cd bakery-ai-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run bakery_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Example Interactions

**Placing an order:**
> "I want 12 chocolate cupcakes for Friday at 2 pm"

**Multi-turn ordering:**
> "I want vanilla brownies for Thursday"
> *(bot asks for quantity and pickup time)*
> "10 brownies at noon"

**Changing an order:**
> "Actually, make it chocolate instead"

**FAQ questions:**
> "What's on the menu?"
> "When do you open?"
> "Where are you located?"
> "Can I speak to someone?"

---

## Project Structure

```
bakery-ai-assistant/
├── bakery_app.py       # Main application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Tech Stack

- **Python 3.x**
- **Streamlit** — web interface and chat UI
- **Regex** — pattern matching for quantity and time extraction
- **Session state** — maintains order context across conversation turns

---

## Approach

The assistant uses **rule-based intent detection** to classify each user message into one of several categories: placing an order, asking about the menu, hours, location, contact, or requesting a change. 

For orders, it uses keyword matching and regex to extract five fields: item, flavor, quantity, pickup date, and pickup time. These are stored in session state and merged across turns — so a customer can provide information gradually and the bot keeps track of what it has and what it still needs.

---

## Ethical Considerations

- The system uses no external APIs or user data collection
- No personal data is stored between sessions
- All responses are rule-based and transparent — the bot will not fabricate information outside its defined responses
- The evaluation panel makes the system's behavior visible and testable

---

## Docker Deployment

The application is containerized using Docker, enabling consistent deployment across any environment.

**Build the image:**
```bash
docker build -t bakery-ai-assistant .
```

**Run the container:**
```bash
docker run -p 8501:8501 bakery-ai-assistant
```

Then open your browser at `http://localhost:8501`.

This satisfies the deployment component of the project and demonstrates basic MLOps practices — the app is environment-agnostic and can be shipped to any cloud provider (AWS, Azure, GCP) or run locally without any setup beyond Docker.

---

## Future Scope

- **LLM integration** — replace rule-based intent detection with a fine-tuned language model or LLM API call for more flexible, natural conversation handling
- **RAG pipeline** — connect the assistant to a knowledge base of bakery documents (recipes, policies, FAQs) using retrieval-augmented generation
- **Database backend** — persist confirmed orders to a database (e.g. PostgreSQL) so staff can view and manage them
- **CI/CD pipeline** — automate testing and deployment using GitHub Actions, so every code change is tested and redeployed automatically
- **Cloud deployment** — deploy the Docker container to Azure Container Apps or AWS ECS for public access
- **Authentication** — add a staff-facing login portal to view, edit, and fulfill confirmed orders
- **Order history** — allow returning customers to view past orders and reorder with one click
- **Payment integration** — connect to Stripe or another payment processor to handle deposits at order time
- **Analytics dashboard** — track popular items, peak ordering times, and common drop-off points in the ordering flow
