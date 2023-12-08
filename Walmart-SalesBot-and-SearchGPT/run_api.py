from search_capabilities import *
from walmart_functions import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or 'OPENAI_API_KEY'
OPENAI_ORG_ID = os.getenv('OpenAI_ORG_ID') or 'OpenAI_ORG_ID'
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY') or 'PINECONE_API_KEY'

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your deployment environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class ConversationRequest(BaseModel):
    messages: List[str]

class ConversationResponse(BaseModel):
    messages: List[str]

# Initialize the Sales Agent
sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)


@app.post("/walmartbot") # This is the endpoint for the walmart bot. It will search walmart for products and return product related information with a link to the product
def handle_conversation(request: ConversationRequest):
    try:
        # Determine if it's a new conversation or continuation
        if not request.messages:
            # It's a new conversation
            sales_agent.seed_agent()
            sales_agent.determine_conversation_stage()
        else:
            # It's a continuation
            for message in request.messages:
                print("User: ",message)
                sales_agent.human_step(message)
                sales_agent.determine_conversation_stage()
                ai_message = sales_agent.step()
                if "<END" in str(ai_message):
                    ai_message = str(ai_message).split('<END')[0]
                sources = knowledge_base.sources_list

                print('Response Received')
                response =  {
                            "messages": [str(ai_message)],
                            "sources": sources,
                            }
                if sources:
                    print('Sources: ', sources)
                return response

                # return ConversationResponse(messages=[ai_message])

        # Process user input and update conversation history
        ai_message = sales_agent.step()
        if "<END" in str(ai_message):
            ai_message = str(ai_message).split('<END')[0]
        sources = knowledge_base.sources_list
        print('Response Received')
        # Return AI response
        response =  {
        "messages": [str(ai_message)],
        "sources": sources,
        }
        if sources:
            print('Sources: ', sources)
        knowledge_base.sources_list = []
        return response
        # return ConversationResponse(messages=[ai_message])

    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Add new endpoints here like conversation above
class ChatResponse(BaseModel):
    text: str
@app.post("/searchgpt") # This is the endpoint for the search AI. It will search duckduckgo, wikipedia, weather api and arxiv for answers to questions. \
#Unlike chatgpt, this will be able to give up to date information
def handle_chat(request: ChatResponse):
    try:
        # Determine if it's a new conversation or continuation
        if not request.text:
            # It's a new conversation
            response =  "Pleaes enter input in the text field"
            return response
        else:
            # It's a continuation
            if request.text:
                input_text = request.text
                print(input_text)
                response = get_response(input_text)
                return response

    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)