from utils import *

st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

# Right Hand Side for Creating Embedding based on the given URLs
num_urls = st.sidebar.number_input("How many URLs do you want to enter?", min_value=1, value=3)
urls = []
for i in range(num_urls):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)
process_url_clicked = st.sidebar.button("Process URLs")

# Placeholders for displaying messages
main_placeholder = st.empty()
message_placeholder = st.empty()  

llm = OpenAI(temperature=0.9, max_tokens=500)

# To check if same URLs have already been processed. 
# This is to avoid extra cost as it will again creating embeddings. 
if os.path.exists(PROCESSED_URLS_PATH):
    with open(PROCESSED_URLS_PATH, "rb") as f:
        processed_urls = pickle.load(f)
else:
    processed_urls = []

# Check if any of the URL fields are empty
empty_fields = [i+1 for i, url in enumerate(urls) if not url]
if empty_fields:
    message_placeholder.text(f"URL field(s) {', '.join(map(str, empty_fields))} is/are empty. Please enter a URL.")

elif process_url_clicked:
    # Check if any of the URLs are new
    if any(url not in processed_urls for url in urls):
        # load data
        loader = UnstructuredURLLoader(urls=urls)
        message_placeholder.text("Loading new URLs... Please wait.")
        data = loader.load()
        # split data
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        message_placeholder.text("Splitting text from the new URLs...")
        docs = text_splitter.split_documents(data)
        # create embeddings and save it to FAISS index
        embeddings = OpenAIEmbeddings()
        vectorstore_openai = FAISS.from_documents(docs, embeddings)
        message_placeholder.text("Building embeddings for the new URLs...")
        time.sleep(2)

        # Save the FAISS index to a pickle file
        with open(FILE_PATH, "wb") as f:
            pickle.dump(vectorstore_openai, f)

        # Update and save the list of processed URLs
        processed_urls.extend([url for url in urls if url not in processed_urls])  # Only add new URLs
        with open(PROCESSED_URLS_PATH, "wb") as f:
            pickle.dump(processed_urls, f)

        message_placeholder.text("Embeddings built and saved successfully!")  # Completion message
        time.sleep(2)  # Let the message be visible for 2 seconds
        message_placeholder.empty()  # Clear the message
    else:
        message_placeholder.text("The provided URLs have already been processed. No new actions taken.")

# Asking Question to the User
query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)