# CAIM - a Cognitive AI Memory Framework for LLMs

CAIM aims to enhance the memory capabilities of LLMs by integrating aspects of cognitive AI, such as thoughts, memory mechanisms, and decision-making. CAIM consists of three modules: 1.) The Memory Controller as central decision unit 2.) the Memory Retrieval, which filters relevant data for an interaction upon request, and 3.) the Post-Thinking, which maintains the memory storage.

**IUI Short Paper:** https://dl.acm.org/doi/full/10.1145/3708557.3716342  
**Arxiv Full-Paper:** https://arxiv.org/abs/2505.13044

How to get started:

1. install requirements: `pip install -r requirements.txt`
2. start CAIM: `python .\main.py`
3. stop conversation: type `exit`

Evaluation of CAIM on GVD:

1. start CAIM: `python .\main.py`
2. fill memories: type `eval`
3. answer probing questions: type `questions`

Note: CAIM with GLM requires an NVIDIA GPU and Python 3.11. See requirements.txt for specific GLM dependencies.

## License

This project is licensed under the [MIT License](./LICENSE).
