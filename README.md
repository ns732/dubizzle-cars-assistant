# dubizzle Cars AI Assistant

Overview
This project is a prototype of an AI assistant for the dubizzle Cars sample inventory. It lets users search for cars in natural language, ask questions about matching listings, refine a search and request a test drive.

The application uses the supplied Excel dataset as its source of inventory information. Search and filtering are handled by the backend, while the language model helps interpret requests and produce conversational responses. The assistant also stores user preferences and previous interactions so that it can recognise a returning user.

This is a local prototype built for the assessment. It does not access live dubizzle listings or a dealership's booking system.
Features
- Search the sample inventory using natural-language queries.
- Filter listings by make, model, year, price, mileage and other available attributes.
- Combine structured filters with text-based retrieval to find relevant listings.
- Display matching listings and available details, including listing images where provided.
- Remove duplicate records from search results and report the number of distinct matches.
- Answer questions about the total number of distinct listings in the inventory.
- Handle follow-up questions about previously retrieved cars.
- Store user preferences, conversation details and previous search results using a user ID.
- Recall saved preferences when the same user returns in a later session.
- Save customer enquiries to a CSV file.
- Accept test-drive requests from Monday to Saturday, between 8:00 AM and 8:00 PM.
- Save cars as favourites.
- Handle basic automotive questions and politely redirect requests that are outside the assistant's purpose.
The inventory contains 100 rows in the supplied sample file. After duplicate records are removed, the application reports 90 distinct listings. Results depend on the data available in the supplied dataset; missing listing details are shown as unavailable rather than guessed.
Technologies
- Python 3.12 – application logic.
- FastAPI – backend API.
- Streamlit – chat interface.
- Groq API – language-model support for understanding requests and generating responses.
- Pandas – loading and processing the Excel inventory.
- scikit-learn and TF-IDF – text matching using word and bigram features.
- SQLite – persistent user profiles, preferences and conversation memory.
- CSV – storing lead enquiries and test-drive requests.
Project structure
dubizzle-assistant/
├── app/
│   ├── api/
│   │   └── main.py
│   ├── database/
│   │   └── memory.py
│   └── services/
│       ├── inventory.py
│       ├── retrieval.py
│       ├── car_search.py
│       ├── query_understanding.py
│       ├── listing_details.py
│       └── bm25_retrieval.py
├── data/
│   └── Copy_of_sample_cars_dataset.xlsx
├── frontend/
│   └── app.py
├── screenshots/
│   ├── inventory-search.png
│   ├── multi-turn-chat.png
│   └── returning-user-memory.png
├── tests/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
The SQLite database and CSV files are created locally when the application runs. They are not required to be present in a fresh clone.
Setup
Requirements
- Python 3.12
- A Groq API key
- The supplied Excel inventory file
1. Clone the repository
git clone https://github.com/ns732/dubizzle-cars-assistant.git
cd dubizzle-cars-assistant
2. Create and activate a virtual environment
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux
python -m venv .venv
source .venv/bin/activate
3. Install dependencies
python -m pip install -e .
4. Configure the API key
Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
Keep your actual .env file private. Do not commit API keys or other credentials to GitHub.
5. Check the inventory file
Make sure Copy_of_sample_cars_dataset.xlsx is in the data/ directory. The application reads the raw dataset worksheet.
Run the application
Start the FastAPI backend
From the project root, run:
uvicorn app.api.main:app --reload
The backend runs at:
- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
Start the Streamlit interface
Open a second terminal, activate the same virtual environment and run:
python -m streamlit run frontend/app.py
Streamlit normally opens at:

http://localhost:8501

Keep the FastAPI server running while using the Streamlit interface.
How it works
Inventory search and retrieval
The inventory loader reads the Excel file and prepares the listing fields for searching. The search service uses structured filters for attributes such as make, model, year, price and mileage, alongside TF-IDF text matching against listing information. This hybrid approach is useful because some user requirements map directly to dataset columns, while other search terms may appear in listing text.

The backend returns listings from the supplied dataset rather than asking the language model to invent vehicles. Results are deduplicated before they are displayed, and the count reflects the distinct listings returned. The assistant can also answer inventory-wide count questions using the loaded dataset. If a listing does not contain a price, mileage or another detail, that value is presented as not specified.
Conversation and memory
The chat endpoint receives a message and a user ID. Previous search results help the assistant respond to follow-up questions about a car the user has already viewed. SQLite stores user information such as preferences, previous interactions and search results. When a user returns with the same ID, the application can retrieve the saved information and use it to support the conversation.
Leads and test drives
Customer enquiries are saved in data/leads.csv, and test-drive requests are saved in data/bookings.csv. The booking endpoint validates that a requested date is Monday to Saturday and that the requested time falls between 8:00 AM and 8:00 PM.

A submitted test-drive request is recorded with a pending-confirmation status. The prototype does not check a live calendar, reserve an actual dealership slot or confirm an appointment.
API endpoints
Method	Endpoint	Purpose
GET	/health	Check whether the backend is running.
GET	/memory/{user_id}	Retrieve saved information for a user.
POST	/cars/search	Search the inventory using filters.
POST	/chat	Send a message to the assistant.
POST	/cars/{car_index}/like/{user_id}	Save a car as a favourite.
POST	/leads	Save a customer enquiry.
POST	/bookings	Submit a test-drive request.


The full request and response formats are available through the FastAPI documentation at /docs.
Design decisions
I chose Streamlit for the client because it provides a straightforward way to demonstrate a conversational interface without spending most of the project time building a separate frontend. FastAPI handles the application logic and exposes the endpoints, while the Streamlit app sends requests to the backend and displays the responses. Keeping those responsibilities separate also makes it easier to test the API independently.

For retrieval, I used structured filtering together with TF-IDF text matching. Structured filters are suitable for fields such as make, year and price, while text matching helps with terms found in listing descriptions. I used SQLite because it is simple to run locally and can retain user information between sessions without requiring a separate database service. Groq provides the language-model component; the backend remains responsible for retrieving inventory records and grounding car-related responses in the supplied data.
Checks performed
The prototype was manually checked with inventory searches across different manufacturers, an inventory-wide search, duplicate removal, total inventory counting, follow-up questions, returning-user preference recall, automotive questions and out-of-scope requests. Test-drive request validation and lead recording are also implemented.

The supplied sample file contains 100 inventory rows. The application returns 90 distinct listings after deduplication. This is a count of the sample dataset, not a live count of vehicles currently available on dubizzle.
Limitations and possible improvements
The application currently uses a fixed sample dataset, so it does not reflect live listing changes. Test-drive requests are recorded for confirmation rather than checked against a dealership calendar. The prototype also uses a user ID to retrieve saved information; a production version would need proper authentication and access controls.

With more time, I would connect the assistant to live inventory and dealership scheduling systems, improve retrieval evaluation across a wider range of natural-language queries, and add stronger user authentication. These changes would make the assistant more suitable for use beyond a local demonstration.

The following screenshots show examples of the application running.

Inventory search


![Inventory Search](screenshots/inventory-search.png)

Multi-turn conversation


![Multi-turn Conversation](screenshots/multi-turn-chat.png)


Returning-user memory


![Returning User Memory](screenshots/returning-user-memory.png)
