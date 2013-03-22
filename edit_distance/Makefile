CFLAGS = -c -Wall
CC = g++
GTEST_DIR = $(HOME)/3rd_party/gtest
CFLAGS += -I$(GTEST_DIR)/include
GTEST_LIBS = -L$(GTEST_DIR)/lib -lgtest

all:distance

clean:
	rm -rf *.o *.s distance

unittest.o : unittest.cc levenshtein_distance.h
	$(CC) $(CFLAGS) -c unittest.cc

levenshtein_distance.o : levenshtein_distance.cc levenshtein_distance.h
	$(CC) $(CFLAGS) -c levenshtein_distance.cc

distance : unittest.o levenshtein_distance.o
	$(CC) -lpthread $(GTEST_LIBS) $^ -o $@
