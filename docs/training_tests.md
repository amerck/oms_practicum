# Project Training Tests

## Potential Base LLM Models
* ~~**deepseek-r1**: [https://ollama.com/library/deepseek-r1](https://ollama.com/library/deepseek-r1)~~
    * ~~deepseek-r1:8b~~
    * ~~"The model has demonstrated outstanding performance across various benchmark evaluations, including mathematics, programming, and general logic."~~
    * This model was prone to freak-outs and paranoid ramblings, and was kind of racist
* **gemma3**: [https://ollama.com/library/gemma3](https://ollama.com/library/gemma3)
    * gemma3:12b
    * "They excel in tasks like question answering, summarization, and reasoning, while their compact design allows deployment on resource-limited devices."
* **qwen3**: [https://ollama.com/library/qwen3](https://ollama.com/library/qwen3)
    * qwen3:8b
    * "Achieves competitive results in benchmark evaluations of coding, math, general capabilities"
* ~~**llama4**: [https://ollama.com/library/llama4](https://ollama.com/library/llama4)~~
    * ~~llama4:16x17b~~
    * ~~"Meta's latest collection of multimodal models."~~
    * ~~MUCH larger than other models~~
    * This model wouldn't run on my device
* ~~**llama3.3**: [https://ollama.com/library/llama3.3](https://ollama.com/library/llama3.3)~~
    * ~~llama3.3:70b~~
    * ~~Also quite large~~
    * This model wouldn't run on my device
* **llama3.2**: [https://ollama.com/library/llama3.2](https://ollama.com/library/llama3.2)
    * llama3.2:3b
* **llama3.1**: [https://ollama.com/library/llama3.1](https://ollama.com/library/llama3.1)
    * llama3.1:8b


## Sentence Transformers

* This project will be using SBERT Pretrained Models for Sentence Transformers, found here: [https://www.sbert.net/docs/sentence_transformer/pretrained_models.html](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
* Potential models:
    * all-mpnet-base-v2: "All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs."
    * multi-qa-mpnet-base-dot-v1: "This model was tuned for semantic search: Given a query/question, it can find relevant passages. It was trained on a large and diverse set of (question, answer) pairs."
    * all-distilroberta-v1: "All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs."
    * multi-qa-distilbert-cos-v1: "This model was tuned for semantic search: Given a query/question, it can find relevant passages. It was trained on a large and diverse set of (question, answer) pairs."