/*
 * =====================================================================================
 *
 *       Filename:  measure.h
 *
 *    Description:  measurement for hbase thrift client R/W performance
 *
 *        Version:  1.0
 *        Created:  07/20/2011 03:05:59 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zavier Gao (mn), docete (AT) gmail.com
 *        Company:  HitHink
 *
 * =====================================================================================
 */

#ifndef _MEASURE_H_
#define _MEASURE_H_

#include <vector>
#include <map>
#include <pthread.h>

using std::vector;
using std::map;

class Measurement {
public:
    Measurement(int granularity, int buckets);
    ~Measurement() {}
    void measure(int latency);
    void report();

private:
    inline void checkEndOfUnit(bool forceend);
    inline long getTimeOfMilli();

private:
    typedef struct _SeriesUnit {
        long time;
        double average;
        _SeriesUnit(long time, double average)
            : time(time), average(average) {}
    } SeriesUnit;

    pthread_mutex_t mutex;

    // time series measurement:
    int _granularity;
    vector<SeriesUnit> _measurements;
    long start;
    long currentunit;
    int sum;
    int count;

    // histogram measurement:
    int _buckets;
    vector<int> histogram;
    int histogramoverflow;

    // common measurement:
    int operations;
    long totallatency;
    map<int, int> returncodes;
    
    int min;
    int max;
};

#endif
