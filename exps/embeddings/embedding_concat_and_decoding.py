'''
The Chinese University of Hong Kong
CSCI5640 Natural Language Processing
Course Project
Group:             Single Bell
Members:           LU, Fanbin and XING, Jinbo and ZHANG, Yuechen
PIC for this file: XING, Jinbo (JinboXING@link.cuhk.edu.hk)
'''
from flair.data import Corpus
from flair.datasets import CONLL_03
from flair.embeddings import WordEmbeddings, StackedEmbeddings, FlairEmbeddings, TransformerWordEmbeddings, CharacterEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from torch.optim.lr_scheduler import OneCycleLR

corpus: Corpus = CONLL_03('../')
tag_type = 'ner'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

PretrainedEmbeddings = 'XLNet'
withCharEmbedding = True
withBiLSTM = True
withCRF = True


embedding_stack = []
if withCharEmbedding:
    embedding_stack.append(CharacterEmbeddings())
if PretrainedEmbeddings == 'XLNet':
    embeddings = StackedEmbeddings(embedding_stack.append
    (TransformerWordEmbeddings(
    model='xlnet-base-cased',
    layers="-1",
    subtoken_pooling="first",
    fine_tune=True,
    use_context=True,)
        )
    )
elif PretrainedEmbeddings == 'RoBERTa':
    embeddings = StackedEmbeddings(embedding_stack.append(TransformerWordEmbeddings(
    model='roberta-large',
    layers="-1",
    subtoken_pooling="first",
    fine_tune=True,
    use_context=True,
    )

    ))




tagger = SequenceTagger(
    hidden_size=256,
    embeddings=embeddings,
    tag_dictionary=tag_dictionary,
    tag_type='ner',
    use_crf=withCRF,
    use_rnn=withBiLSTM,
    reproject_embeddings=False,
)

trainer = ModelTrainer(tagger, corpus)



trainer.train('resources/taggers/exp3-{}'.format(PretrainedEmbeddings),
            learning_rate=5.0e-6,
            mini_batch_size=4,
            mini_batch_chunk_size=1,
            max_epochs=20,
            scheduler=OneCycleLR,
            embeddings_storage_mode='none',
            weight_decay=0.,
            optimizer=torch.optim.AdamW
            )