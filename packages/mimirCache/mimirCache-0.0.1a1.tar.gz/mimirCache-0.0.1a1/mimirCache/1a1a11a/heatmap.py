
from mimirCache.CacheReader.vscsiReader import vscsiCacheReader
from mimirCache.CacheReader.plainReader import plainCacheReader
from mimirCache.CacheReader.csvReader import csvCacheReader
from mimirCache.Cache.LRU import LRU
from mimirCache.Profiler.parda import parda
import pickle
import numpy as np
import sys
from matplotlib import pyplot as plt
from multiprocessing import Process, Queue


def prepare_heatmap_dat(bin_size=1000, cache_size = 2000):
    reader = csvCacheReader("../Data/trace_CloudPhysics_txt", 4)
    total_line = reader.get_num_total_lines()
    p = parda(LRU, 30000, reader)
    c_reuse_dist_long_array = p.get_reuse_distance()

    array_len = len(c_reuse_dist_long_array)//bin_size
    result = np.empty((array_len-1, array_len), dtype=np.float32)
    result[:] = np.nan
    # (x, y) -> heat, x, y is the left, lower point of heat square
    # (x,y) means from time x to time y

    print(len(c_reuse_dist_long_array))
    # print((c_reuse_dist_long_array))


    with open('reuse.dat', 'w') as ofile:
        for i in c_reuse_dist_long_array:
            print(i)
            ofile.write(str(i)+'\n')
    sys.exit(1)

    for (x,y) in _get_xy_distribution(bin_size, len(c_reuse_dist_long_array)):
        print('({},{})'.format(x,y))
        hr = _calc_hit_rate(c_reuse_dist_long_array, cache_size, x, y)
        result[x//bin_size][y//bin_size] = hr

    print(result)
    with open('temp2', 'wb') as ofile:
        pickle.dump(result, ofile)


def prepare_heatmap_dat_multiprocess(bin_size=1000, cache_size = 2000, num_of_process=8):
    reader = plainCacheReader("../Data/parda.trace")
    total_line = reader.get_num_total_lines()
    p = parda(LRU, 30000, reader)
    c_reuse_dist_long_array = p.get_reuse_distance()

    array_len = len(c_reuse_dist_long_array)//bin_size
    result = np.empty((array_len-1, array_len), dtype=np.float32)
    result[:] = np.nan
    # (x, y) -> heat, x, y is the left, lower point of heat square
    # (x,y) means from time x to time y

    print(len(c_reuse_dist_long_array))
    # print((c_reuse_dist_long_array[-2]))



    # for i in c_reuse_dist_long_array:
    #     print(i)

    l = _get_xy_distribution_list(bin_size, len(c_reuse_dist_long_array))
    divided_len = len(l)//num_of_process
    q = Queue()
    process_list = []
    for i in range(num_of_process):
        if i!=num_of_process-1:
            p = Process(target=_calc_hit_rate_multiprocess,
                        args=(c_reuse_dist_long_array, cache_size, l[divided_len*i:divided_len*(i+1)], q))
            process_list.append(p)
            p.start()
        else:
            p = Process(target=_calc_hit_rate_multiprocess,
                        args=(c_reuse_dist_long_array, cache_size, l[divided_len*i:len(l)], q))
            process_list.append(p)
            p.start()

    num_left = len(l)
    while (num_left):
        t = q.get()
        result[t[0]//bin_size][t[1]//bin_size] = t[2]
        num_left -= 1
        print(num_left)


    print(result)
    with open('temp', 'wb') as ofile:
        pickle.dump(result, ofile)



def _get_xy_distribution(bin_size, total_length):
    for i in range(0, total_length-bin_size+1, bin_size):
        # if the total length is not multiple of bin_size, discard the last partition
        for j in range(i+bin_size, total_length-bin_size+1, bin_size):
            yield(i, j)


def _get_xy_distribution_list(bin_size, total_length):
    l = []
    for i in range(0, total_length-bin_size+1, bin_size):
        # if the total length is not multiple of bin_size, discard the last partition
        for j in range(i+bin_size, total_length-bin_size+1, bin_size):
            l.append((i, j))
    return l



def _calc_hit_rate(reuse_dist_array, cache_size, begin_pos, end_pos):
    hit_count = 0
    miss_count = 0
    for i in range(begin_pos, end_pos):
        if reuse_dist_array[i] == -1:
            # never appear
            miss_count += 1
            continue
        if reuse_dist_array[i]- (i-begin_pos) < 0 and reuse_dist_array[i]<cache_size:
            # hit
            hit_count += 1
        else:
            # miss
            miss_count += 1
    # print("hit+miss={}, total size:{}, hit rage:{}".format(hit_count+miss_count, end_pos-begin_pos, hit_count/(end_pos-begin_pos)))
    return hit_count/(end_pos-begin_pos)


def _calc_hit_rate_multiprocess(reuse_dist_array, cache_size, pos_list, q):
    for (begin_pos, end_pos) in pos_list:
        hr = _calc_hit_rate(reuse_dist_array, cache_size, begin_pos, end_pos)
        print('({},{}): {}'.format(begin_pos, end_pos, hr))
        q.put((begin_pos, end_pos, hr))




def draw():
    with open('temp', 'rb') as ofile:
        result = pickle.load(ofile)
    print(result)

    masked_array = np.ma.array (result, mask=np.isnan(result))

    print(masked_array)
    cmap = plt.cm.jet
    cmap.set_bad('w',1.)

    heatmap = plt.pcolor(masked_array.T, cmap=cmap)

    # heatmap = plt.pcolor(result2.T, cmap=plt.cm.Blues, vmin=np.min(result2[np.nonzero(result2)]), vmax=result2.max())
    try:
        heatmap = plt.pcolorfast(masked_array.T, cmap=cmap)
        # heatmap = plt.pcolor(result2.T, cmap=plt.cm.Blues, vmin=np.min(result2[np.nonzero(result2)]), vmax=result2.max())
        plt.show()
    except:
        import matplotlib
        matplotlib.use('pdf')
        heatmap = plt.pcolorfast(masked_array.T, cmap=cmap)
        plt.savefig("heatmap.pdf")



import os
print(os.getcwd())
prepare_heatmap_dat(3000, 200)
# prepare_heatmap_dat_multiprocess(3000, 200, 4)
draw()
# for i in _get_xy_distribution(1000, 10000):
#     print(i)