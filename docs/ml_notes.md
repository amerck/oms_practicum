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