from langchain_google_genai import ChatGoogleGenerativeAI
try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    print("Initialization successful")
except Exception as e:
    print(f"Initialization failed: {e}")
