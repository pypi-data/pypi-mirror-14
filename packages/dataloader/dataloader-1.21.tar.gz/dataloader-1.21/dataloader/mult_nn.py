import dataloader
import tensorflow as tf
import numpy as np

# mnist = input_data.read_data_sets("MNIST_data/",one_hot=True)
data = dataloader.read_data_sets('mat2/')

# train = data.train.next_batch(100)
# train[0] = user one hots # matrix
# train[1] = tfidf vectors # matrix
# train[2] = ratings # vector

# dropout DONE
# other activation DONE
# tf.sigmoid DONE
# tf.tanh DONE
# tf.nn.relu DONE
# tf.nn.relu6 DONE
# tf.nn.softplus DONE
# other gradient descent DONE
# tf.train.AdamOptimizer DONE
# tf.train.AdagradOptimizer DONE
# tf.train.GradientDescentOptimizer DONE
# tf.train.MomentumOptimizer DONE
# tf.train.FtrlOptimzer POSTPONED
# tf.train.RMSPropOptimzer POSTPONED
# decaying lrate
# tf.train.exponential_decay
# decaying weights POSTPONED
# multiple {in,out}puts
# dropconnect on convolutional

Litem = 30
Luser = 30
L = 50

# keep_prob = tf.placeholder("float")
xuser = tf.placeholder("float", [None, None], name='user')
xitem = tf.placeholder("float", [None, None], name='item')

witem = tf.Variable(tf.truncated_normal([data.train.features['tfidf'].shape[1], Litem], stddev=.1), name='Witem')
bitem = tf.Variable(tf.constant(.1, shape=[Litem]), name='Bitem')

wuser = tf.Variable(tf.truncated_normal([data.train.features['onehots'].shape[1], Luser], stddev=.1), name='Wuser')
buser = tf.Variable(tf.constant(.1, shape=[Luser]), name='Buser')

hitem = tf.tanh(tf.matmul(xitem, witem) + bitem)  # NxL
huser = tf.tanh(tf.matmul(xuser, wuser) + buser)  # NxL

vitem = tf.Variable(tf.truncated_normal([Litem, L], stddev=.1), name='vitem')
q = tf.Variable(tf.constant(.1, shape=[L]))

vuser = tf.Variable(tf.truncated_normal([Luser, L], stddev=.1), name='vuser')

hfinal = tf.tanh(tf.matmul(hitem, vitem) + tf.matmul(huser, vuser) + q)

u = tf.Variable(tf.truncated_normal([L, 1], stddev=.1), name='U')
bfinal = tf.Variable(tf.constant(.1))

y = tf.matmul(hfinal, u) + bfinal

y_ = tf.placeholder("float", [None, None], name='Y_')

# cross_entropy = -tf.reduce_sum(y_*tf.log(y), name='Loss')
objective = tf.sqrt(tf.div(tf.reduce_sum(tf.square(y_ - y)), tf.to_float(tf.size(y_))))
tf.scalar_summary('Loss', objective)

train_step = tf.train.GradientDescentOptimizer(.02).minimize(objective)

# correct_predictions = tf.equal(tf.argmax(y,1),tf.argmax(y_,1), name='corr_pred')
# accuracy = tf.reduce_mean(tf.cast(correct_predictions,"float"), name='accuracy')
#tf.scalar_summary('Objective', objective)
# when you have more data lower the learning rate

init = tf.initialize_all_variables()

session = tf.Session()
session.run(init)

merged_summary_op = tf.merge_all_summaries()
summary_writer = tf.train.SummaryWriter('/tmp/mnist_logs', session.graph.as_graph_def())

for i in range(500):
    newbatch = data.train.next_batch(100)
    batch_user, batch_item, batch_y = newbatch.features['onehots'], newbatch.features['tfidf'], newbatch.labels[
        'ratings']
    session.run(train_step, feed_dict={xuser: batch_user.todense(), y_: batch_y, xitem: batch_item.todense()})
    # summary_str = session.run(merged_summary_op, feed_dict={x: mnist.train.images, y_: mnist.train.labels})
    # summary_writer.add_summary(summary_str, i)
    print "Objective: ", i, " ", session.run(objective,
                                             feed_dict={y_: data.dev.labels['ratings'],
                                                        xitem: data.dev.features['tfidf'].todense(),
                                                        xuser: data.dev.features['onehots'].todense()})
