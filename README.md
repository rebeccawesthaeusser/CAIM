# CAIM - a Cognitive AI Memory Framework for LLMs

CAIM aims to enhance the memory capabilities of LLMs by integrating aspects of cognitive AI, such as thoughts, memory mechanisms, and decision-making. CAIM consists of three modules: 1.) The Memory Controller as central decision unit 2.) the Memory Retrieval, which filters relevant data for an interaction upon request, and 3.) the Post-Thinking, which maintains the memory storage.

**IUI Short Paper:** https://dl.acm.org/doi/full/10.1145/3708557.3716342  
**Arxiv Full-Paper:** https://arxiv.org/abs/2505.13044


## Getting started
### Environment Setup
Install requirements with pip: `pip install -r requirements.txt`

### Start CAIM
1. start CAIM: `python .\main.py`
2. stop conversation: type `exit`

### Evaluation of CAIM on GVD:
1. start CAIM: `python .\main.py`
2. fill memories: type `eval`
3. answer probing questions: type `questions`

Note: CAIM with GLM requires an NVIDIA GPU and Python 3.11. See requirements.txt for specific GLM dependencies.

## License
This project is licensed under the [MIT License](./LICENSE).


## Citation
If you find our work useful, please consider citing the following papers:  

```
@article{westhausser2025caim,
  title={CAIM: Development and Evaluation of a Cognitive AI Memory Framework for Long-Term Interaction with Intelligent Agents},
  author={Westh{\"a}u{\ss}er, Rebecca and Berenz, Frederik and Minker, Wolfgang and Zepf, Sebastian},
  journal={arXiv preprint arXiv:2505.13044},
  year={2025}
}

@inproceedings{westhausser2025caim,
  title={CAIM: A Cognitive AI Memory Framework for Long-term Interaction with LLMs},
  author={Westh{\"a}u{\ss}er, Rebecca and Zepf, Sebastian and Minker, Wolfgang},
  booktitle={Companion Proceedings of the 30th International Conference on Intelligent User Interfaces},
  pages={22--25},
  year={2025}
}

```
