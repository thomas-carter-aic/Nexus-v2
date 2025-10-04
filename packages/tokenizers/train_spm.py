"""
Train SentencePiece tokenizer placeholder
"""

import sentencepiece as spm

if __name__ == "__main__":
    spm.SentencePieceTrainer.Train(
        input='training/sample_text.txt',
        model_prefix='tokenizers/spm_model',
        vocab_size=8000,
        model_type='unigram'
    )
    print("Trained SentencePiece model saved to tokenizers/spm_model.model")
