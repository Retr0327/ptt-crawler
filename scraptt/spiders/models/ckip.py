from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger

NLP_MODEL = "bert-base"

ws_driver = CkipWordSegmenter(model=NLP_MODEL)
pos_driver = CkipPosTagger(model=NLP_MODEL)
