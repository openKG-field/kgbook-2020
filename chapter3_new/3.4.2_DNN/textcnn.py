from keras import backend as K
from keras.models import Model
from keras.engine.topology import Layer
from keras.regularizers import l1, l2
from keras.layers import (Input, Embedding, Concatenate,
                          Conv1D, Subtract, Add,
                          MaxPooling1D, Flatten, Dropout,
                          Dense, Dot, LSTM, GRU, Bidirectional, BatchNormalization)


class TextCNN:

    def __init__(self, config):
        self.input_dim = config.input_dim
        self.pool_size = config.pool_size
        self.drop = config.drop_prob
        self.nClass = config.nClass
        self.final_active = config.final_active
        self.need_position = config.need_position
        self.token_embedding = Embedding(input_dim=config.vocab_size,
                                         output_dim=config.embedding_dim,
                                         weights=[config.token_matrix],
                                         trainable=False)
        self.position_embedding = Embedding(input_dim=config.input_dim,
                                            output_dim=config.embedding_dim,
                                            weights=[config.position_matrix],
                                            trainable=True)
        self.conv_group = [Conv1D(config.num_filter,
                                  kernel_size=config.filter_size[i],
                                  padding='valid',
                                  activation='relu',
                                  strides=1,
                                  # kernel_regularizer=l2(0.01),
                                  # activity_regularizer=l2(0.01)
                                  ) for i in range(len(config.filter_size))]

    def encoder(self, inputs, positons=None):
        conv_list = []
        for conv in self.conv_group:
            inputs = conv(inputs)
            inputs = MaxPooling1D(pool_size=self.pool_size)(inputs)
            conv_list.append(inputs)
        concat = Concatenate(axis=1)(conv_list)
        flat = Flatten()(concat)
        dropout = Dropout(self.drop)(flat)
        return dropout

    def _Mult(self, u, v):
        return Dot(axes=1)([u, v])

    def _Sub(self, u, v):
        s = Subtract()([u, v])
        return Dot(axes=-1)([s, s])

    def _NN(self, u, v):
        return Dense(2, activation='relu')([u, v])

    def _SubMultNN(self, u, v):
        s = Subtract()([u, v])
        m1 = Dot(axes=-1)([s, s])
        m2 = Dot(axes=-1)([u, v])
        return Dense(2, activation='relu')(Concatenate()([m1, m2]))

    def model_build(self):
        inputQ = Input(shape=(self.input_dim,), dtype='int32',name='Q')
        inputC = Input(shape=(self.input_dim,), dtype='int32',name='C')
        model_inputs = [inputQ, inputC]

        embedQ = self.token_embedding(inputQ)
        embedC = self.token_embedding(inputC)

        if self.need_position:
            posiQ = Input(shape=(self.input_dim,), dtype='int32')
            posiC = Input(shape=(self.input_dim,), dtype='int32')
            model_inputs = [inputQ, posiQ, inputC, posiC]

            embed_posiQ = self.position_embedding(posiQ)
            embed_posiC = self.position_embedding(posiC)

            embedQ = Add()([embedQ, embed_posiQ])
            embedC = Add()([embedC, embed_posiC])

        cnn_qry = self.encoder(embedQ)
        cnn_cnd = self.encoder(embedC)

        concat = Concatenate()([cnn_qry, cnn_cnd])
        outputs = Dense(self.nClass, activation=self.final_active,
                          activity_regularizer=l2(0.01),
                          kernel_regularizer=l2(0.01)
                        )(concat)
        return Model(inputs=model_inputs, outputs=outputs)
