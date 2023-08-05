# ===================================================================================================
# Aaron Tuor, Western Washington University, Feb. 2016
#
# dataloader.py: General purpose dataloader for python non-sequential machine learning tasks
# Massive modification of input_data.py distributed by Google Inc.
# Original source input_data.py found at:
#
#	https://tensorflow.googlesource.com/tensorflow/+/master/tensorflow/examples/tutorials/mnist/input_data.py
#
# input_data.py is licensed under Apache License 2.0 (the "License")
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# ===================================================================================================
# Aaron Tuor, Western Washington University, Feb. 2016
#
# dataloader.py: General purpose dataloader for python non-sequential machine learning tasks
# Massive modification of input_data.py distributed by Google Inc.
# Original source input_data.py found at:
#
#	https://tensorflow.googlesource.com/tensorflow/+/master/tensorflow/examples/tutorials/mnist/input_data.py
#
# input_data.py is licensed under Apache License 2.0 (the "License")
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
# =====================================================================================================
import struct
import numpy
import scipy.io
import os
import scipy.sparse as sps
import termcolor as tc

slash = '/'
if os.name == 'nt':
    slash = '\\'  # so this works in Windows


# ============================================================================================
# ==========EXCEPTIONS FOR MINIMAL DATA INTEGRITY CHECKS======================================
# ============================================================================================
class Bad_directory_structure_error(Exception):
    '''Raised when a data directory specified
    does not contain all subfolders named in the folders list of :any:`read_data_sets`. Any of these directories
	could be empty and the loader will hand back a :any:`DataSet` object containing no data
	which corresponds to the empty folder.'''
    pass


class Unsupported_format_error(Exception):
    '''Raised when a file with name beginning *labels_* or *features_* is encountered without one of the
    supported file extensions. It is okay to have other file types in your directory as long as their
    names don't begin with *labels_* or *features_*.'''
    pass


class Mat_format_error(Exception):
    '''Raised if the .mat file being read does not contain a
    variable named *data*.'''
    pass


class Sparse_format_error(Exception):
    '''Raised when reading a plain text file with .sparsetxt
    extension and there are not three entries per line.'''
    pass


# ==============================================================================================
# =============================DATA STRUCTURES==================================================
# ==============================================================================================

class DataSet(object):
    """
    General data structure for non-sequential batch gradient descent training. Shuffles data after each epoch.
    """

    def __init__(self, dataset_map):
        self._features = dataset_map[
            'features']  # hashmap of feature matrices #keys are derived from what's between 'features' and file extension#in the filename
        self._labels = dataset_map[
            'labels']  # hashmap of label matrices  #keys are derived from what's between 'labels' and file extension #in the filename
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._num_examples = dataset_map['num_examples']

    @property
    def features(self):
        '''A hashmap (dictionary) of matrices from files with a *features_* prefix.
        Keys are derived from what's between *features_* and the file extension in the filename,
        e.g. the key to a matrix read from a data file named: *features_descriptor.ext*
        is the string  *'descriptor'*.'''
        return self._features

    @property
    def index_in_epoch(self):
        '''The number of datapoints that have been trained on in a particular epoch.'''
        return self._index_in_epoch

    @property
    def labels(self):
        '''A hashmap (dictionary) of matrices from files with a *labels_* prefix.
        Keys are derived from what's between *labels_* and the file extension in the filename,
        e.g. the key to a matrix read from a data file named: *labels_descriptor.ext*
        is the string  *'descriptor'*.'''
        return self._labels

    @property
    def num_examples(self):
        '''Number of rows (data points) of the label matrices in this :any:`DataSet`.'''
        return self._num_examples

    @property
    def epochs_completed(self):
        '''Number of epochs the data has been used to train with.'''
        return self._epochs_completed

    # Underscores mean these functions are supposed to be private, but they aren't really
    def _shuffle_(self, order, datamap):
        '''
        :param order: A list of the indices for the row permutation
        :param datamap:
        :return: void
        Shuffles the rows an individual matrix in the :any:`DataSet` object.'
        '''
        for matrix in datamap:
            datamap[matrix] = datamap[matrix][order]

    def _next_batch_(self, datamap, start, end):
        '''
        :param datamap: A hash map of matrices
        :param start: starting row
        :param end: ending row
        :return: A hash map of slices of matrices from row start to row end
        '''
        batch_data_map = {}
        for matrix in datamap:
            batch_data_map[matrix] = datamap[matrix][start:end]
        return batch_data_map

    def next_batch(self, batch_size):
        '''
        :param batch_size: int
        :return: A :any:`DataSet` object with the next `batch_size` examples.

        If `batch_size` is greater than the number of data points in the the data
        stream a python assert fails and the loader stops. If `batch_size`
        is greater than the number of examples left in the epoch then all the
        matrices in the data stream are shuffled and a :any:`DataSet` object containing
        the first num_examples rows of the shuffled feature matrices and label
        matrices is returned.
        '''
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = numpy.arange(self._num_examples)
            numpy.random.shuffle(perm)
            self._shuffle_(perm, self._features)
            self._shuffle_(perm, self._labels)
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return DataSet({'features': self._next_batch_(self._features, start, end),
                        'labels': self._next_batch_(self._labels, start, end),
                        'num_examples': batch_size})

    def show(self):
        '''
        :return: void
        Pretty printing of all the data (dimensions, keys, type) in the :any:`DataSet` object
        '''
        print('%d data points' % self.num_examples)
        print('features:')
        for feature in self.features:
            print('\t %s: %s' % (feature, (self.features[feature].shape),))
        print('labels:')
        for label in self.labels:
            print('\t %s: %s' % (label, (self.labels[label].shape),))


class DataSets(object):
    '''
    A record of DataSet objects with a display function.
    '''

    def __init__(self, datasets_map):
        for k, v in datasets_map.items():
            setattr(self, k, DataSet(v))

    def show(self):
        datasets = [s for s in dir(self) if not s.startswith('__') and not s == 'show']
        for dataset in datasets:
            print tc.colored(dataset + ':', 'yellow')
            getattr(self, dataset).show()


# ===================================================================================
# ====================== I/0 ========================================================
# ===================================================================================

def import_data(filename):
    '''
    :param filename: A file of an accepted format representing a matrix.
    :return: A numpy matrix or scipy sparse csr_matrix.

    Decides how to load data into python matrices by file extension.
    Raises :any:`Unsupported_format_error` if extension is not one of the supported
    extensions (mat, sparse, binary, sparsetxt, densetxt, index).
    Data contained in .mat files should be saved in a matrix named *data*.
    '''
    extension = filename.split(slash)[-1].split('.')[-1].strip()
    if extension == 'mat':
        mat_file_map = scipy.io.loadmat(filename)
        if 'data' not in mat_file_map:
            raise Mat_format_error('Matrix in .mat file ' +
                                   filename + ' must be named "data"')
        if mat_file_map['data'].shape[0] == 1:
            return numpy.transpose(mat_file_map['data'])
        else:
            return mat_file_map['data']
    elif extension == 'index':
        return imatload(filename)
    elif extension == 'sparse':
        return smatload(filename)
    elif extension == 'binary' or extension == 'dense':
        return matload(filename)
    elif extension == 'sparsetxt':
        X = numpy.loadtxt(filename)
        if X.shape[1] != 3:
            raise Sparse_format_error('Sparse Format: row col val')
        if numpy.amin(X[:, 2]) == 1 or numpy.amin(X[:, 1] == 1):
            X[:, 0] = X[:, 0] - 1
            X[:, 1] = X[:, 1] - 1
        return sps.csr_matrix((X[:, 2], (X[:, 0], X[:, 1])))
    elif extension == 'densetxt':
        return numpy.loadtxt(filename)
    else:
        raise Unsupported_format_error('Supported extensions: '
                                       'mat, sparse, binary, sparsetxt, densetxt')


def write_int64(file_obj, num):
    """
    Writes an 8 byte integer to a file in binary format
    :param file_obj: the open file object to write to
    :param num: the integer to write, will be converted to a long int
    """
    file_obj.write(struct.pack('q', long(num)))


def read_int64(file_obj):
    """
    :param file_obj: The open file object from which to read.
    :return: The eight bytes read from the file object interpreted as a long int.
    Reads an 8 byte binary integer from a file.
    """
    return struct.unpack('q', file_obj.read(8))[0]


def matload(filename):
    """
    :param filename: file from which to read.
    :return: the matrix which has been read.
    Reads in a dense matrix from binary file filename.
    """
    f = open(filename, 'r')
    m = read_int64(f)
    n = read_int64(f)
    x = numpy.fromfile(f, numpy.dtype(numpy.float64), -1, "")
    x = x.reshape((m, n), order="FORTRAN")
    f.close()
    return numpy.mat(x)


def matsave(filename, x):
    """
    Saves the input matrix to the input file in dense format
    :param filename: file to write to
    :param x: matrix to write
    """
    f = open(filename, 'wb')
    write_int64(f, x.shape[0])
    write_int64(f, x.shape[1])
    x.astype(float, copy=False).ravel('FORTRAN').tofile(f)
    f.close()


def smatload(filename):
    """
    Reads in a sparse matrix from file
    :param filename: the file from which to read
    :return: a dense matrix created from the sparse data
    """
    f = open(filename, 'r')
    row = read_int64(f)
    col = read_int64(f)
    nnz = read_int64(f)
    S = numpy.fromfile(f, 'd', 3 * nnz)
    f.close()
    S = S.reshape((nnz, 3))
    rows = S[:, 0].astype(int) - 1
    cols = S[:, 1].astype(int) - 1
    vals = S[:, 2]
    return sps.csr_matrix((vals, (rows, cols)), shape=(row, col))


def smatsave(filename, t):
    """
    Saves the input matrix to the input file in sparse format
    :param filename:
    :param t:
    """
    f = open(filename, 'wb')
    t = numpy.mat(t)
    write_int64(f, t.shape[0])
    write_int64(f, t.shape[1])
    indices = numpy.nonzero(t)
    idxs = numpy.append(indices[0], indices[1], axis=0)
    write_int64(f, idxs.shape[1])  # might break if s is empty
    indices = numpy.append(idxs, t[indices], axis=0)
    indices[0:2, :] += 1
    indices.astype(float, copy=False).ravel('F').tofile(f)
    f.close()


def imatload(filename):
    """
    Reads in a sparse matrix from file
    :param filename: the file from which to read
    :return: a dense matrix created from the sparse data
    """
    f = open(filename, 'r')
    vec_length = read_int64(f)
    dim = read_int64(f)
    vec = numpy.fromfile(f, 'd', vec_length)
    f.close()
    vec = vec.astype(int) - 1
    return HotIndex(vec, dim)


def imatsave(filename, index_vec):
    """
    Saves the input matrix to the input file in sparse format
    :param filename:
    :param index_vec: A :any:`HotIndex` object.
    """
    f = open(filename, 'wb')
    vector = index_vec.vec
    vector = vector + 1
    write_int64(f, vector.shape[0])
    write_int64(f, index_vec.dim)
    vector.astype(float, copy=False).tofile(f)
    f.close()

class HotIndex(object):
    """
    Index vector representation of one hot matrix.
    """

    def __init__(self, matrix, dimension=None):
        if is_one_hot(matrix):
            self._dim = matrix.shape[1]
            self._vec = toIndex(matrix).flatten()
        else:
            self._dim = dimension
            self._vec = matrix.flatten()

    @property
    def dim(self):
        '''The feature dimension of the one hot vector represented as indices.'''
        return self._dim

    @property
    def vec(self):
        '''The vector of hot indices.'''
        return self._vec


def makedirs(datadirectory, sub_directory_list=('train', 'dev', 'test')):
    '''
    :param datadirectory: Name of the directory you want to create containing the subdirectory folders.
     If the directory already exists it will be populated with the subdirectory folders.
    :param sub_directory_list: The list of subdirectories you want to create
    :return: void
    '''
    if not datadirectory.endswith(slash):
        datadirectory += slash
    os.system('mkdir ' + datadirectory)
    for sub in sub_directory_list:
        os.system('mkdir ' + datadirectory + sub)


def read_data_sets(directory, folders=('train', 'dev', 'test'), hashlist=()):
    '''
    :param directory: Root directory containing train, test, and dev data folders.
    :param folders: by default there are train, dev, and test folders. If you want more you have to make a list.
        Every folder you want must be included in the list including the default train, dev, and test
    :param hashlist: If you provide a hashlist these files and only these files will be added to your DataSet objects.
        The function assumes that there will be files with these hashes (string between labels_ or features_ and
        .extensionin in each folder in the folders list. It you do not provide a hashlist then anything with
        the privileged prefixes labels_ or features_ will be loaded.
    :return: A :any:`DataSets` object.
    '''
    if not directory.endswith(slash):
        directory += slash
    dir_files = os.listdir(directory)

    datasets_map = {}
    for folder in folders:  # iterates over keys
        dataset_map = {'features': {}, 'labels': {}, 'num_examples': 0}
        print('reading ' + folder + '...')
        if folder not in dir_files:
            raise Bad_directory_structure_error('Need ' + folder + ' folder in ' + directory + ' directory.')
        file_list = os.listdir(directory + folder)
        for filename in file_list:
            prefix = filename.split('_')[0]
            if prefix == 'features' or prefix == 'labels':
                prefix_ = prefix + '_'
                descriptor = (filename.split('.')[0]).split(prefix_)[-1]
                if (not hashlist) or (descriptor in hashlist):
                    dataset_map[prefix][descriptor] = import_data(directory + folder + slash + filename)
                    if prefix == 'labels':
                        dataset_map['num_examples'] = dataset_map[prefix][descriptor].shape[0]
        datasets_map[folder] = dataset_map
    return DataSets(datasets_map)


# ===================================================================================
# ====================== DATA MANIPULATION===========================================
# ===================================================================================

def toOnehot(X, dim=None):
    '''
    :param X: Vector of indices or :any:`HotIndex` object
    :param dim: Dimension of indexing
    :return: Matrix of one hots
    '''
    if isinstance(X, HotIndex):
        dim = X.dim
    # empty one-hot matrix
    hotmatrix = numpy.zeros((X.shape[0], dim))
    # fill indice positions
    hotmatrix[numpy.arange(X.shape[0]), X] = 1
    hotmatrix = sps.csr_matrix(hotmatrix)
    return hotmatrix


def is_one_hot(A):
    '''
    :param A: A numpy array or scipy sparse matrix
    :return: True if matrix is a sparse matrix of one hot vectors, False otherwise
    '''
    isonehot = False
    if sps.issparse(A):
        (i, j, v) = sps.find(A)
        if (numpy.sum(v) == A.shape[0] and numpy.unique(i).shape[0] == A.shape[0] and
                    numpy.unique(v).shape[0] == 1 and numpy.unique(v)[0] == 1):
            isonehot = True
    return isonehot


def toIndex(A):
    '''
    :param A: A matrix of one hot row vectors.
    :return: The hot indices.
    '''
    return sps.find(A)[1]


def center(A):
    '''
    :param A: Matrix to center about its mean.
    :return: The centered matrix.
    '''
    if sps.isspmatrix_csr(A):
        (i, j, v) = sps.find(A)
        A = sps.csr_matrix((v - sps.csr_matrix.mean(v), (i, j)),
                           shape=(A.shape[0], A.shape[1]),
                           dtype='float32')
        return sps.csr_matrix((v - numpy.mean(v), (i, j)),
                              shape=(A.shape[0], A.shape[1]),
                              dtype='float32')
    else:
        return A - numpy.mean(A)
