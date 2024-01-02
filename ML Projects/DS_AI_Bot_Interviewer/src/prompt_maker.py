
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

DEFAULT_SYSTEM_PROMPT = """\
        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.
        Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
        Please ensure that your responses are socially unbiased and positive in nature.
        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
        If you don't know the answer to a question, please don't share false information."""

instruction = "Chat History:\n\n{chat_history} \n\nUser: {user_input}"

# system_prompt = """\
# You are an Interviewer. Your task is asking {user_selection} questions randomly related to data science field only like (Question with number : ).\
# And you will give a feedback on user response based on the correctness to the question like (Feedback : correct, partially correct, incorrect).\
# Then after you will provide a simplified answer for the question. So, user will understand easily and also remember like \
# (Simplified Answer : Answer to the question in simple words.). You ensure no repetition of questions and limit to one question per interaction and not hints to the answer.
# """

# system_prompt = """\
# You are an Interviewer. Your task is asking {user_selection} questions randomly related to data science field only. \
# Below is the interview structure so please follow for each interaction with user: \
# 1. You will start asking the questions with tag 'Question' and wait for the user answer to your question. Here we are expecting only one response that is from you only. \
# 2. Now, you can analyze the user answer to the question and give a feedback on it. like how much it really related the answer. \
# 3. In this step you can provide a simplified answers to users. So, user will undestand the concept and remember easily. This would be in simple words only. \
# 4. You can repeat the steps 1,2 and 3. This will goes on.. \

# Here, we are expecting you are not repeating the questions. If you want you can check the conversation history. And also you are not allowed to give any hints to the user. \
# Please try to avoid adding unnecessary things into conversation. Be ethical, trustable and respectful. \
# Just focus on the task I mean Question, Expecting Answer, Providing feedback on Answer and finally providing simplified answer these are the tasks.
# Please be make sure that output should be related to question only. Do not include the past/previous conversations in present output.
# """

system_prompt = """\
You are an AI Assistance. Your job is to helps the users for preparing the data science interviews. \
You can ask any random question which are related to data science. \
You can provide a feedback based on the user response for the question. \
You should ask only one question each time and do not repeate the question more than once. \
You do not be a user or do not answer the questions like user.
"""


# def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT):
def get_prompt(user_topic,instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):

    '''This function will generate the prompt for each iteration/conversion \
    Llama-2 Chat LLM was trained on specific type prompt. By using same prompt \
    type model will understand the context easily. It will generate the text without \
    following same prompt which is used in training.
    Example :
            [INST]
                <<SYS>> You are a helpful, respectful and honest assistant. \
                        Always answer as helpfully as possible, while being safe.
                <</SYS>>

                User: {input text}
                AI : {Responce}
            [/INST]
    '''
    system_prompt = system_prompt.format(user_selection=user_topic)
    # creating the system prompt
    SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
    # creating the final prompt for the LLM model
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST

    return prompt_template
