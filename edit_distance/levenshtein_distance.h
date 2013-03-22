/*
 * =====================================================================================
 *
 *       Filename:  levenshtein_distance.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  05/04/2012 04:57:52 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Zavier Gao (), Docete AT gmail DOT com
 *        Company:  
 *
 * =====================================================================================
 */

#ifndef _LEVENSHTEIN_DISTANCE_H_
#define _LEVENSHTEIN_DISTANCE_H_

#define MIN(a,b) ((a) < (b) ? a : b)

unsigned int levenshtein_distance(const char *, const char *);

#endif
