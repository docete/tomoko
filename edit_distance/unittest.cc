/*
 * =====================================================================================
 *
 *       Filename:  unittest.cc
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  05/04/2012 04:59:36 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zavier Gao (), Docete AT gmail DOT com
 *        Company:  
 *
 * =====================================================================================
 */

#include "levenshtein_distance.h"
#include "gtest/gtest.h"
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <ctime>

char * 
cstringGenerator(unsigned int n)
{
    static char alphabet[] = "abcdefghijklmnopqrstuvwxyz0123456789";
    char * s = new char[n+1];
    s[n] = '\0';
    srand(time(NULL));
    for (int i = 0; i < n; i++) {
        s[i] = alphabet[rand()%36];
    }
    return s;
}

// mock test: test normal case
TEST(levenshtein_distance_test, mock) {
    EXPECT_EQ(1, levenshtein_distance("abcd", "abc"));
    EXPECT_EQ(1, levenshtein_distance("abc", "abd"));
    EXPECT_EQ(1, levenshtein_distance("abc", "ab"));
}

// boundary test: test boundary conditions
TEST(levenshtein_distance_test, bound) {
    char *s = cstringGenerator(rand()%1000 + 1);
    EXPECT_EQ(strlen(s), levenshtein_distance("", s));
    EXPECT_EQ(0, levenshtein_distance("", ""));
    EXPECT_EQ(0, levenshtein_distance(s, s));
    delete [] s;
}

// random test: test lots of random case
TEST(levenshtein_distance_test, random) {
    int attempt = 1000;
    int min_length = 10;
    while (attempt --) {
        char *s = cstringGenerator(rand()%1000 + min_length);
        char *t = cstringGenerator(rand()%1000 + min_length);

        char *s_minus = new char[strlen(s)];
        char *t_minus = new char[strlen(t)];

        strncpy(s_minus, s, strlen(s)-1);
        s_minus[strlen(s)-1] = '\0';

        strncpy(t_minus, t, strlen(t)-1);
        t_minus[strlen(t)-1] = '\0';

        int min = MIN(levenshtein_distance(s, t_minus), levenshtein_distance(s_minus, t));
        min = MIN(levenshtein_distance(s_minus, t_minus), min);
        EXPECT_TRUE(min+1 >= levenshtein_distance(s, t));

        delete [] s;
        delete [] t;
        delete [] s_minus;
        delete [] t_minus;
    }
}

int main(int argc, char ** argv)
{
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
