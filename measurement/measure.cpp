/*
 * =====================================================================================
 *
 *       Filename:  measure.cpp
 *
 *    Description:  measurement for hbase thrift client R/W performance
 *    
 *        Version:  1.0
 *        Created:  07/20/2011 07:10:22 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zavier Gao (mn), docete (AT) gmail.com
 *        Company:  HitHink
 *
 * =====================================================================================
 */
#include <sys/time.h>
#include <cstdlib>
#include <iostream>
#include <unistd.h>
#include "measure.h"
#include "log.h"

using std::cout;
using std::endl;

Measurement::Measurement(int granularity, int buckets)
    : _granularity(granularity), _buckets(buckets), start(0), 
    currentunit(0), histogramoverflow(0), operations(0),
    totallatency(0), min(-1), max(-1),
    sum(0), count(0)
{
    mutex_unit = PTHREAD_MUTEX_INITIALIZER;
    mutex_maxmin = PTHREAD_MUTEX_INITIALIZER;
    start = getTimeOfMilli();
    histogram.resize(_buckets);
}

void Measurement::measure(int latency)
{
    checkEndOfUnit(false);

    // common:
    __sync_add_and_fetch(&totallatency,latency);
    __sync_add_and_fetch(&operations, 1);

    pthread_mutex_lock(&mutex_maxmin);
    if (latency > max)
        max = latency;
    if (latency < min || min < 0)
        min = latency;
    pthread_mutex_unlock(&mutex_maxmin);

    // time series:
    __sync_add_and_fetch(&count, 1);
    __sync_add_and_fetch(&sum, latency);

    // histogram:
    if (latency >= _buckets)
        __sync_add_and_fetch(&histogramoverflow, 1);
    else
        __sync_add_and_fetch(&(histogram[latency]), 1);
}

inline void Measurement::checkEndOfUnit(bool forceend)
{
    long now = getTimeOfMilli();
    long unit = ((now - start)/_granularity)*_granularity;
    //cout << "logging: " << now << "\t" << unit << endl;

    pthread_mutex_lock(&mutex_unit);
    if ((unit > currentunit) || forceend) {
        double avg = ((double)sum) / ((double)count);
        _measurements.push_back(SeriesUnit(currentunit, avg));

        currentunit = unit;
        
        count = 0;
        sum = 0;
    }
    pthread_mutex_unlock(&mutex_unit);
}

inline long Measurement::getTimeOfMilli()
{
    struct timeval m_time;
    gettimeofday(&m_time, 0);
    return (long)(m_time.tv_sec * 1000 + m_time.tv_usec / 1000);
}

void Measurement::report()
{
    cout << "Report" << endl;
    cout << "Max: " << max << " (ms)" << endl;
    cout << "Min: " << min << " (ms)" << endl;
    cout << "Total Lantency: " << totallatency << " (ms); Operations: " << operations << endl;
    
    vector<int>::iterator it = histogram.begin();
    size_t i = 0;
    cout << "\nHistogram Report:" << endl;
    for ( ; it != histogram.end(); ++it, ++i) {
        cout << i << "," << *it << endl;
    }
    cout << ">=" << i << "," << histogramoverflow << endl;

    vector<SeriesUnit>::iterator iter = _measurements.begin();
    cout << "\nTime Series Report:" << endl;
    for ( ; iter != _measurements.end(); ++iter) {
        cout << iter->time << "," << iter->average << endl;
    }
}

#ifdef _UNIT_TEST_
int main()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    srand(tv.tv_sec * tv.tv_usec);
    Measurement measurement(1000, 100);
    for (size_t i = 0; i < 1000; ++i) {
        long usecs = rand() % 150 * 1000;
        usleep(usecs);
        measurement.measure(usecs/1000);
    }
    measurement.report();
    return 0;
}
#endif
