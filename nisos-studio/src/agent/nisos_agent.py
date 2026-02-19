from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import START, StateGraph, MessagesState, END
from langgraph.prebuilt import tools_condition, ToolNode
from src.agent.social_api import get_social_media_profile
import os 
from dotenv import load_dotenv

load_dotenv()

# llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv('GEMINI_API_KEY'))

# url = 'http://localhost:3001/users/alex_rivers'

class State(TypedDict):
    profile_url: str
    user_profile: dict
    is_threat_detected: bool
    threat_confidence: float
    flagged_posts_ids: List[str]
    threat_category: str
    category_rationale: str
    summary: str  # Added so it persists in the State

class InputState(TypedDict):
    profile_url: str

class RiskFlaggingResult(TypedDict):
    threat_confidence: float
    flagged_posts_ids: List[str]

class CategoryAnalysisResult(TypedDict):
    category: str
    rationale: str

class ExecutiveSummaryResult(TypedDict):
    summary: str

system_prompt = SystemMessage(content="You are an expert at threat assessment and specialise in social media analysis. Your task is to analyse social media profiles to detect potential threats. Use the provided tools to assist in your analysis.")

def risk_flagging(state: State):
    """Analyse the social media profile of a specific user to detect potential threats.
    """
    url = state.get("profile_url", "")
    print(f"--- [Node: risk_flagging] Fetching profile for URL: {url} ---")
    profile = get_social_media_profile(url)
    request = f"analyse the following social media profile of from user {profile.get('username')} and determine if it contains a potential threat. Here is the profile data: {profile}"
    
    structured_llm = llm.with_structured_output(RiskFlaggingResult)
    llm_output = structured_llm.invoke([system_prompt, request])
    threat_confidence = llm_output.get("threat_confidence", 0.0)

    # Determine threat status based on a 0.7 confidence threshold
    is_threat_detected = threat_confidence > 0.7
    
    print(f"--- [Node: risk_flagging] Threat Detected: {is_threat_detected} (Confidence: {threat_confidence}) ---")

    return {
        **llm_output,
        "is_threat_detected": is_threat_detected,
        "user_profile": profile
    }

def route_after_risk_flagging(state: State):
    if state.get("is_threat_detected") == True:
        return "category_analysis"
    return "executive_summary"

def category_analysis(state: State):
    """Fraud, Violence, Hate Speech, Misinformation, Other"""
    profile = state.get("user_profile")
    print(f"--- [Node: category_analysis] Analysing user: {profile.get('username')} ---")
    
    structured_llm = llm.with_structured_output(CategoryAnalysisResult)
    # Added profile data to the request for better context
    request = f"Based on the social media profile of user {profile.get('username')}, categorise the potential threat into one of the following categories: Fraud, Violence, Hate Speech, Misinformation, or Other. Provide a rationale for your categorisation.\n\nProfile Data: {profile}"

    response = structured_llm.invoke([system_prompt, request])
    
    category = response.get("category", "Other")
    print(f"--- [Node: category_analysis] Category: {category} ---")

    return {
        "threat_category": category,
        "category_rationale": response.get("rationale", "No rationale provided.")
    }

def executive_summary(state: State):
    profile = state.get("user_profile", {})
    category = state.get("threat_category", "Unknown")
    rationale = state.get("category_rationale", "No rationale provided.")
    flagged_posts = state.get("flagged_posts_ids", [])
    
    print(f"--- [Node: executive_summary] Generating summary for user: {profile.get('username')} ---")
    
    structured_llm = llm.with_structured_output(ExecutiveSummaryResult)

    if state.get("is_threat_detected"):
        threat_summary = f"Provide an executive summary of the threat detected in the social media profile of user {profile.get('username')}. The threat has been categorised as {category} with the following rationale: {rationale}. The following posts have been flagged as potential threats: {flagged_posts}.\n\nFull Profile Context: {profile}"
        response = structured_llm.invoke([system_prompt, threat_summary])
    else:
        benign_summary = f"Provide an executive summary of the social media profile of user {profile.get('username', 'Unknown')}, highlight why no threats have been detected based on the analysis.\n\nFull Profile Context: {profile}"
        response = structured_llm.invoke([system_prompt, benign_summary])
    
    summary_text = response.get("summary", "Summary generation failed.")
    print(f"--- [Node: executive_summary] Summary generated (length: {len(summary_text)}) ---")
    
    return {
        "summary": summary_text
    }

builder = StateGraph(State, input=InputState)

builder.add_node("risk_flagging", risk_flagging)
builder.add_node("category_analysis", category_analysis)
builder.add_node("executive_summary", executive_summary)

builder.set_entry_point("risk_flagging")

builder.add_conditional_edges(
    "risk_flagging",
    route_after_risk_flagging,
    {
        "executive_summary": "executive_summary",
        "category_analysis": "category_analysis"
    }
)

builder.add_edge("category_analysis", "executive_summary")

builder.add_edge("executive_summary", END)

graph = builder.compile()