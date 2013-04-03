#!/usr/bin/env python
# coding: utf8

import sys
import random

BIG_PRIME = 9223372036854775783

def random_parameter():
    return random.randrange(0, 9223372036854775783-1)

class BloomFilter():
    """
    Bloom Filter是由Burton Howard Bloom于1970年提出的一种概率数据结构。
    主要用来判断元素是否存在于一个集合中。
    节省了大量空间，可能会产生False Positive，但杜绝了False Negative。
    https://en.wikipedia.org/wiki/Bloom_filter

    其原理是：
    1. 创建一个m位的位数组bitmap，并初始化所有位为0；
    2. 选择k个hash函数，其值域为[0, m)
    3. 初始化BloomFilter，对集合S中的任意字符串s，计算一组hash值 
                H = {hi(s)} (i=0...m-1)
       令 bitmap[hi(s)] (bitmap的hi(s)位) 为1
    5. 查询，对于任意字符串s，
       若 所有 bitmap[hi(s)]为1，则 s 可能存在于S中
       若 有一 bitmap[hi(s)]为0，则 s 一定不存在于S中

    6. FNR (false negative rate) = (1-e^kn/m))^k
       当 k = ln 2 * m/n 时，右边的等式值最小，为 (0.6185)^(m/n)

       取 m/n = 20, k=14, FNR已经足够小
       http://pages.cs.wisc.edu/~cao/papers/summary-cache/node8.html#SECTION00053000000000000000
       (上文中n为bloomfilter中插入的字符串数目)

    缺陷: 
    1. 无法删除元素，解决方案 Counting Bloom Filter
       在原始的BloomFilter中使用计数器而非一个bit。插入字符串时，增加计数器，反之亦反。

    2. 无法动态扩展，解决方案 Scalable bloom Filter
       使用一组BloomFilter替代一个大的Bloom Filter。
       若字符串s存在于某一Bloom Filter中，则s可能存在于S中；
       若字符串不存在于所有Bloom Filter中，则s一定不存在于S中。
    """
    def __init__(self, num_byte, num_probe=14):
        self.num_byte = num_byte
        self.bitmap = bytearray(self.num_byte)
        self.num_probe = num_probe
        self.hash_functions = [self.__hash_function_generate() \
                for i in xrange(self.num_probe)]
        self.key_count = 0
        
    def update(self, key):
        for probe in self.get_probes(key):
            self.bitmap[probe // 8] |= 0x1 << (probe % 8)
        self.key_count += 1

    def lookup(self, key):
        if not self.__contains__(key):
            return "Nope"
        return "Probably"
            
    def get_probes(self, key):
        return (self.hash_functions[i](abs(hash(key))) \
                for i in xrange(self.num_probe))

    def get_density(self):
        c = ''.join(format(x, '08b') for x in self.bitmap)
        return c.count('1') / float(len(c))

    def get_keycount(self):
        return self.key_count

    def __contains__(self, key):
        return all(self.bitmap[probe // 8] & (0x1 << (probe % 8)) \
                for probe in self.get_probes(key))

    def __hash_function_generate(self):
        a, b = random_parameter(), random_parameter()
        return lambda x: (a * x + b) % BIG_PRIME % (self.num_byte * 8)

class CountingBloomFilter():
    pass

class ScalableBloomFilter():
    def __init__(self, num_byte=1024, num_probe=14):
        self.num_byte = num_byte
        self.num_probe = num_probe
        self.max_key_count = self.num_byte * 8 // 30
        self.bloomfilters = [BloomFilter(self.num_byte,self.num_probe)]
        self.key_count = 0
        self.bloomfilter_num = 0

    def update(self, key):
        if (self.bloomfilters[self.bloomfilter_num].get_keycount() \
                >= self.max_key_count):
            self.bloomfilters.append(BloomFilter(self.num_byte, self.num_probe))
            self.bloomfilter_num += 1
        self.bloomfilters[self.bloomfilter_num].update(key)
        self.key_count += 1

    def __contains__(self, key):
        return any(bloomfilter.__contains__(key) \
                for bloomfilter in self.bloomfilters)

if __name__ == '__main__':

    sbf = ScalableBloomFilter(1024, 14);
    
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        sbf.update(line.strip())

    states = '''Alabama Alaska Arizona Arkansas California Colorado Connecticut
        Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas
        Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota
        Mississippi Missouri Montana Nebraska Nevada NewHampshire NewJersey
        NewMexico NewYork NorthCarolina NorthDakota Ohio Oklahoma Oregon
        Pennsylvania RhodeIsland SouthCarolina SouthDakota Tennessee Texas Utah
        Vermont Virginia Washington WestVirginia Wisconsin Wyoming'''.split()
        

    for state in states:
        sbf.update(state)

    print sbf.bloomfilter_num, sbf.key_count
    for bf in sbf.bloomfilters:
        print bf.get_keycount(), bf.get_density()

    m = sum(state in sbf for state in states)
    print '%d true positive and %d false negative out of %d trials' \
            % (m, len(states)-m, len(states))


    from random import sample
    from string import ascii_letters
    trials = 100000
    m = sum(''.join(sample(ascii_letters, 8)).lower() in sbf \
            for i in xrange(trials))
    print '%d true negative and %d false positive out of %d trials' \
            % (trials-m, m, trials)
