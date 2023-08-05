#!/usr/bin/env python
from __future__ import division, print_function

import sys
import h5py
import numpy as np
from scipy import sparse
from functools import partial
from hdf5_matlab_reader.empty_matrix import EmptyMatrix

def loadmat(f):
    h5_file = h5py.File(f, 'r')
    return extract_file(h5_file)

def extract_file(f):
    def avoid_refs(kv):
        #refs are extracted under the structures they correspond to
        k, v = kv
        return not k.startswith(u'#refs#')

    return {k:extract_element(f, v) for k, v in filter(avoid_refs, f.items())}

def extract_element(f, element):
    if type(element) is h5py._hl.dataset.Dataset:
        return extract_dataset(f, element)
    elif type(element) is h5py._hl.group.Group:
        return extract_group(f, element)
    else:
        raise NotImplementedError('Unimplemented HDF5 structure')

def extract_group(f, group):
    if 'MATLAB_sparse' in group.attrs:
        return extract_sparse(f, group)

    return {k:extract_element(f, v) for k, v in group.items()}

def extract_dataset(f, dataset):
    if 'MATLAB_class' not in dataset.attrs:
        #this occurs in sparse arrays, which can be special cased to do
        #sparse representations. this case is still wise.
        return dataset.value

    data_class = dataset.attrs['MATLAB_class']

    if data_class == 'struct' and 'MATLAB_empty' in dataset.attrs:
        #empty struct
        return {}

    elif 'MATLAB_empty' in dataset.attrs and dataset.attrs['MATLAB_empty'] == 1:
        #empty matrix if shape in 0xN, Nx0
        #size of empty matrix encoded as its value. several strategies possible
        #1. Ignore size of empty matrix, return None. Probably acceptable
        #2. Return np.empty(shape=shape). Causes odd behavior if the
        #   shape is actually desired, for instance 138x6 cell array of empty
        #   matrices (0 by 0) returns as 138x6x0x0 np.ndarray
        #3. Return placeholder empty matrix class which correctly conveys
        #   matrix size

        #type of empty can be numerical, or canonical_empty
        return EmptyMatrix(shape=dataset.value, dtype=data_class)

    elif data_class in ('double', 'single', 'int8', 'uint8', 'int16', 'uint16',
                      'int32', 'uint32', 'int64', 'uint64'):
        #numerical arrays
        return dataset.value

    elif data_class == 'logical':
        #encoded in matlab as ubyte, we force as bool
        return dataset.value.astype(bool)

    elif data_class == 'cell':
        return extract_cell(f, dataset)

    elif data_class == 'char':
        return extract_string(dataset)

    # don't really know what to do with these datatypes, they require
    # considerable parsing to do something smart. For now we import their 
    # HDF5 structure in big unwieldy objects and let the user deal with them
    elif data_class in ('categorical', 'datetime', 'containers.Map', 'table'):
        return dataset.value

    elif data_class == 'FileWrapper__':
        return extract_cell(f, dataset)

def extract_sparse(f, group):
    data = group['data'].value
    rows = group['ir'].value
    cols = group['jc'].value

    mtype = group.attrs['MATLAB_class']

    nr = group.attrs['MATLAB_sparse']       #nr_rows
    nc = len(cols) - 1                      #nr_cols
    ne = len(rows)                          #nr_elements

    #convert col to indptr from dense ptr
    compress_col = [np.where(cols == i)[0][-1] for i in np.arange(ne)]

    #if encoded as matlab as ubyte, we enforce bool
    return sparse.coo_matrix((data, (rows, compress_col)), shape=(nr, nc),
        dtype=bool if mtype == 'logical' else None)

def indexarg(f, arg):
    '''
    clearly it is more important to be pythonic than straightforward
    '''
    return f[arg]

def extract_cell(f, dataset):
    '''
    behold the elegance and simplicity of recursion
    '''
    return np.squeeze(
            map_ndlist(
             partial(extract_element, f),
             map(partial(map_ndarray,
                         partial(indexarg, f)),
                 dataset.value)))

def bytearray_to_string(z):
    return ''.join(map(unichr, z))

def is_ndim_list(ndlist):
    return list in map(type, ndlist)

def extract_string(dataset):
    string_k = partial(map_ndarrays, bytearray_to_string)
    #char arrays are transposed in matlab representation
    #column and row are opposite, but not in terms of order on disk
    str_array = string_k(np.transpose(dataset.value))

    #if the result is a single string, return just the single string
    #otherwise, return the full character array
    if len(str_array) == 1:
        return str_array[0]
    else:
        return str_array

def map_ndlist(k, ndlist):
    '''
    like map, but operates on every element of n-dimensional python list
    '''
    if type(ndlist) == list:
        return map(partial(map_ndlist, k), ndlist)
    else:
        return k(ndlist)

def map_ndarray(k, ndarray):
    '''
    like map, but operates on every element of n-dimensional np.ndarray
    '''
    if ndarray.ndim > 1:
        return map(partial(map_ndarray, k), ndarray)
    else:
        return map(k, ndarray)

def map_ndlists(k, ndlists):
    '''
    like map, but operates on every lowest-dim list of n-dimensional list
    '''
    if is_ndim_list(ndlists):
        return map(partial(map_ndlist, k), ndlist)
    else:
        return k(ndlist)

def map_ndarrays(k, ndarray):
    '''
    like map, but operates on every lowest-dim list of n-dimensional np.ndarray
    '''
    if ndarray.ndim > 1:
        return map(partial(map_ndarrays, k), ndarray)
    else:
        return k(ndarray)


if __name__ == '__main__':
    matfile = sys.argv[1]

    try:
        h5_file = h5py.File(matfile, 'r')
        mat_out = extract_file(h5_file)

        print(mat_out)

        for k, v in mat_out.items():
            print(k, np.shape(v))

        import pdb
        pdb.set_trace()
    except Exception as e:
        print('{0}: {1}'.format(type(e), e))
        import pdb
        pdb.set_trace()
