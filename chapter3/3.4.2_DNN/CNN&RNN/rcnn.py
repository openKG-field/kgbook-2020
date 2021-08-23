from keras import backend as K
from keras.regularizers import l1,l2,l1_l2
from keras.models import Model
from keras.layers import (Input, Embedding, Dropout, Concatenate, 
                          Conv1D, MaxPooling1D, GlobalMaxPooling1D,
                          LSTM, GRU, Bidirectional, Dense)

class RCNN:
    def __init__(self, config):

        self.input_dim=config.input_dim
        self.drop = config.drop_prob
        self.filter_num = config.filter_num
        self.filter_size = config.filter_size
        self.rnn_units = config.rnn_units
        self.useBidiriction = config.useBidiriction
        self.nClass = config.nClass
        self.final_active = config.final_active
        self.rnn_cell = GRU if config.rnn_cell == 'gru' else LSTM
        self.lstm_layer = self.RNNencoder()
        self.token_embedding=Embedding(config.vocab_size,
                                    config.embedding_dim,
                                    weights=[config.token_matrix],
                                    trainable=False)

    def RNNencoder(self):
        lstm = self.rnn_cell(units=self.rnn_units,activation='tanh',
                    return_sequences=True,kernel_regularizer=l2(0.1))
        if self.useBidiriction:
            lstm= Bidirectional(lstm)
        return lstm

    def model_build(self):

        inputQ = Input(shape=(self.input_dim,))
        inputC = Input(shape=(self.input_dim,))

        embededQ = self.token_embedding(inputQ)
        embededC = self.token_embedding(inputC)

        lstm_outputQ = self.lstm_layer(embededQ)
        lstm_outputC = self.lstm_layer(embededC)

        cnninputQ = Concatenate(axis=-1)([embededQ,lstm_outputQ])
        cnninputC = Concatenate(axis=-1)([embededC,lstm_outputC])


        #
        dropedQ = Dropout(rate=self.drop)(cnninputQ)
        ConvedQ = Conv1D(filters=self.filter_num, 
                         kernel_size=self.filter_size,
                         padding='valid',
                         activation='relu',
                         kernel_regularizer=l2(0.01))(dropedQ)
        MaxPooledQ = MaxPooling1D(self.filter_size)(ConvedQ)
        globalMaxPoolQ = GlobalMaxPooling1D()(MaxPooledQ)

        dropedC = Dropout(rate=self.drop)(cnninputC)
        ConvedC = Conv1D(filters=self.filter_num, 
                         kernel_size=self.filter_size,
                         padding='valid',
                         activation='relu',
                         kernel_regularizer=l2(0.01))(dropedC)
        MaxPooledC = MaxPooling1D(self.filter_size)(ConvedC)
        globalMaxPoolC = GlobalMaxPooling1D()(MaxPooledC)


        merged = Concatenate(axis=-1)([globalMaxPoolQ, globalMaxPoolC])
        outputs = Dense(self.nClass,activation=self.final_active,
                        kernel_regularizer=l2(0.01)
                        )(merged)
        
        return Model(inputs=[inputQ,inputC],outputs=outputs)
