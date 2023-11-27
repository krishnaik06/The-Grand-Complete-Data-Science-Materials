import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image
from pickle import load

# Load tokenizer
tokenizer = load(open('tokenizer1.pkl', 'rb'))
max_len = 34

# Load image captioning model
model = load_model('model_18.h5')

# Load VGG16 model for feature extraction
vgg_model = VGG16()
vgg_model.layers.pop()
vgg_model = Model(inputs=vgg_model.inputs, outputs=vgg_model.layers[-2].output)

# Function to map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# Function to generate image caption
def generate_caption(model, tokenizer, photo, max_length):
    # Seed the generation process
    in_text = 'startseq'
    # Iterate over the whole length of the sequence
    for i in range(max_length):
        # Integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # Pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # Predict next word
        yhat = model.predict([photo, sequence], verbose=0)
        # Convert probability to integer
        yhat = np.argmax(yhat)
        # Map integer to word
        word = word_for_id(yhat, tokenizer)
        # Stop if we cannot map the word
        if word is None:
            break
        # Append as input for generating the next word
        in_text += ' ' + word
        # Stop if we predict the end of the sequence
        if word == 'endseq':
            break
    return in_text

# Function to extract image features
def extract_features(filename):
    # Load the photo
    image = load_img(filename, target_size=(224, 224))
    # Convert the image pixels to a numpy array
    image = img_to_array(image)
    # Reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # Prepare the image for the VGG model
    image = preprocess_input(image)
    # Get features
    feature = vgg_model.predict(image, verbose=0)
    return feature

# Remove start and end sequence tokens from the generated caption
def remove_start_end_tokens(caption):
    stopwords = ['startseq', 'endseq']
    querywords = caption.split()
    resultwords = [word for word in querywords if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    return result

def main():
    st.set_page_config(page_title="Image Captioning", page_icon="📷")
    st.title("Image Captioning")
    st.markdown("Upload an image and get a caption for it.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        resized_image = image.resize((400, 400))
        st.image(resized_image, caption='Uploaded Image')

        # Extract image features
        photo = extract_features(uploaded_file)

        # Generate image caption
        if st.button("Generate Caption"):
            with st.spinner("Generating caption..."):
                description = generate_caption(model, tokenizer, photo, max_len)

    # Remove start and end sequence tokens from the caption
            caption = remove_start_end_tokens(description)

            # Display caption
            st.subheader("  Generated Caption")
            st.markdown("---")
            st.markdown(f"<p style='font-size: 18px; text-align: center;'>{caption}</p>", unsafe_allow_html=True)
            st.markdown("---")


if __name__ == '__main__':
    main()
