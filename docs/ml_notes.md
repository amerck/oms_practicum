# Machine Learning Notes

## Embeddings

* Vectors
    * A vector is a point in space (an ordered list)
    * Examples
        * values = [1, 5, -2]
        * $ p = (1, 5, -2) $
    * Embedding
        * A "vector representation" or numeric coordinate in some high dimensional space
        * An embedding is the vector that is created by a deep learning model for the purpose of similarity searches by that model
    * Tokenization
        * Converts input data into numeric representation
        * The same input data will produce the same output from the tokenizer
        * Byte-Pair Encoding (BPE) - encodes pairs of bytes
            * tiktoken (https://github.com/openai/tiktoken)
            * tokens = tokenizer.encode(f.read().lower())
    * For training, we need to generate a token and label
        * Token is the x value, label is the y value
        * One approach is for y to be the prediction of what the next token should be
    * One-hot encoding
        * A vector as wide as all possible outputs
            * Only one position in the vector set to '1'
        * x value is the token
        * y value is an array of boolean values


## TensorFlow
* Framework for creating and deploying ML
* Three main tasks
    * Create a TensorFlow Dataset object from token generator
    * Create nural network to train embeddings
    * Train the network
* tf.data.Dataset.from_generator()
    * First argument is token generator function
    * Second argument is an output signature
        * Must be a tuple of tf.TensorSpec() objects
* Need to batch dataset to input into neural network
    * ds = ds.batch(16)
    * ds.take(1) returns one batch


## Keras
* Python interface for artificial neural networks
* Models
    * Sequential model
        * Straightforward list of layers
        * Limited to single-input, single-output stacks of layers
    * Functional API
        * fully-featured API
        * supports arbitrary model architectures
        * "industry strength" model
    * Model subclassing
        * Implement everything from scratch
        * Used for out-of-box research use cases


## Training Models
* Options for training a new model
    * Fine tuning
        * Potentially very costly
        * Time consuming to train (or fine tune) a model
        * Low Rank Adaptation (LoRA) and Quantized Low Rank Adaptation (QLoRA) an option
            * Able to run on lower resource hardware
        * Possibility for catastrophic forgetting
    * Freeze, add adapter layers, and train adapter layers
        * Still susceptible to hallucinations
* Sentence-based Bidirectional Encoder Representations from Transformers (SBERT)
    * General idea is the same as training word embeddings
    * sentence-transformers Python library contains several SBERT models (https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
* LangChain
    * Text Splitters
        * https://python.langchain.com/docs/concepts/text_splitters/
        * RecursiveCharacterTextSplitter()
            * chunk_size - maximum length of text string output
            * chunk_overlap - how many characters overlap previous and next string
            * length_function - function name to determine length of chunk


## Data Processing
* Handling HTML data:
    * https://beautiful-soup-4.readthedocs.io/en/latest/
    * https://pypi.org/project/markdownify/


## RAG

* Rough steps
    1. Create model that can convert text into embedding vectors
    2. Convert data into suitable format
    3. Take text and convert into overlapping chunks
    4. Convert chunks into embeddings
    5. Store embeddings and text into vector database
    6. Search database for elements related to a given question
    7. Feed question, search results, and prompt into LLM 
