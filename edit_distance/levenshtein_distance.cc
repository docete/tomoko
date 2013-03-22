/*
 * =====================================================================================
 *
 *       Filename:  levenshtein_distance.cc
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  05/04/2012 02:17:51 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zavier Gao (), Docete AT gmail DOT com
 *        Company:  
 *
 * =====================================================================================
 */
#include <cstring>
#include "levenshtein_distance.h"

unsigned int
levenshtein_distance(const char *s, const char *t)
{
    unsigned int m = strlen(s);
    unsigned int n = strlen(t);
    
    unsigned int **d= new unsigned int * [m+1];
    for (unsigned int i = 0; i <= m; i++) {
        d[i] = new unsigned int[n+1];
    }

    for (unsigned int i = 0; i <= m; i++) {
        d[i][0] = i;
    }
    for (unsigned int i = 0; i <= n; i++) {
        d[0][i] = i;
    }

    for (unsigned int i = 1; i <= m; i++) {
        for (unsigned int j = 1; j <=n; j++) {
            if (*(s+i) == *(t+j))
                d[i][j] = d[i-1][j-1];
            else {
                unsigned int tmp = MIN(d[i-1][j], d[i][j-1]);
                d[i][j] = MIN(d[i-1][j-1], tmp) + 1;
            }
        }
    }
    
    unsigned int ret = d[m][n];

    for (unsigned int i = 0; i <= m; i++) {
        delete [] d[i];
    }
    delete [] d;

    return ret;
}

