/*
 * orgasm.h
 *
 *  Created on: 11 juil. 2012
 *      Author: coissac
 */

#ifndef ORGASM_H_
#define ORGASM_H_

#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>

#ifdef __SSE2__
#define __intel__
#endif

#define DISPLAYSTEP 10000  // Print long on screen every DISPLAYSTEP events
#define MAXREADLEN  512    // Maximum length of a read

#define MEM_ALLOC_ERROR (1)
#define FATAL_ERROR     (2)
#define ASSERTION_ERROR (3)

#define DEBUG(format,...)

#define GENERICERROR(file,line,error,code,format,...) { fprintf(stderr,"[%s:%d] "error" : "format"\n",__FILE__,__LINE__,__VA_ARGS__); \
	                                     exit(code); \
                                       }

#define FATALERROR(format,...) GENERICERROR(__FILE__, __LINE__,"ERROR",FATAL_ERROR,format,__VA_ARGS__)
#define ASSERT(predicat,format,...) if (!(predicat)) GENERICERROR(__FILE__, __LINE__,"ASSERTION ERROR",ASSERTION_ERROR,format,__VA_ARGS__)

#define MALLOC(size)        util_malloc((size),__FILE__, __LINE__)
#define REALLOC(chunk,size) util_realloc((chunk), (size),__FILE__,__LINE__)
#define FREE(chunk)         util_free((chunk),__FILE__, __LINE__)

#define PTR16(p) (void*)(((size_t)(p) & ((size_t)~((size_t)0xF))) + (((size_t)(p) & 0xF) ? (0x10):0))
#define PTR8(p) (void*)(((size_t)(p) & ((size_t)~((size_t)0x7))) + (((size_t)(p) & 0x7) ? (0x8):0))
#define CODELENGTH(x) (((x)>>2) + (((x) & 3) ? 1:0))
#define READSTART(buf,id) ((pnuc)((buf)->records + (buf)->recordSize * (id)))
#define READEND(buf,id) (READSTART((buf),(id))+CODELENGTH((buf)->readSize)-1)

#ifndef TRUE
#define TRUE (3==3)
#define FALSE (!TRUE)
#endif

typedef char* pnuc;

typedef struct {
	size_t 		readSize;		// Size of one read in base pair
	size_t 		readCount;      // count of reads. One pair of reads counts for 2
	size_t 		recordSize;		// Size in bytes of one compressed read
	size_t      maxrecord;      // Maximum count of read storable in the arena
								// maxrecord have to be sotrable in an uint32_t
	int32_t     letterCount[4]; // count for each of the four nucleotide at one position
	char*  		arena;          // start of the memory arena
	char*  		records;        // the start of the first record [0].
								// correspond to the first adress in arena aligned on 16
								// -> byte array of recordSize*maxrecord (but only readCount stored in it)
								// -> lexicographically ordered on direct sequence on all reads (no paired info)
	uint32_t*   order1;         // a pointer used to point on a int array indicating an order
								// over the records.
								// -> order of the read in records if lexicographically ordered on the revcomp sequence : maxrecord (but only readCount stored in it)
	uint32_t*   order2;         // a pointer used to point on a int array indicating an order
								// over the records.
								// -> num of paired read : maxrecord (but only readCount stored in it)
								// ex: gives the num of the pair in records pair(n) => records[order2[n]]
	uint32_t*   index1;
	uint32_t*   index2;
	uint32_t*   complement;     // convert index to reverse complement sequence
	uint32_t    minword;        // minimal size of word to consider
	uint32_t    suffixidx;      // count of suffix indices stored on disk
} buffer_t;

typedef struct {
	size_t	i;
} wordindex_t;


/* Macros */


void    util_free(void *chunk, const char *filename, int32_t    line);
void *util_realloc(void *chunk, int32_t newsize, const char *filename, int32_t    line);
void *util_malloc(int32_t chunksize, const char *filename, int32_t    line);

uint32_t  readPairedFastq(char* dest,
						  FILE* forward, FILE* reverse,
						  int32_t maxsize, uint32_t readLength);

uint32_t round2(uint32_t x);
uint32_t round4(uint32_t x);
uint32_t round8(uint32_t x);
uint32_t round16(uint32_t x);

uint8_t  encode4nuc(const char* seq);
uint32_t encode16nuc(const char* seq);
uint8_t is16ACGT(const char* seq);

char *decode(buffer_t *buffer, uint32_t recordid, uint32_t begin, int32_t length, char *dest);
char *decodeComp(buffer_t *buffer, uint32_t recordid, uint32_t begin, int32_t length, char *dest);
char *getRead(buffer_t *buffer, int32_t recordid, uint32_t begin, int32_t length, char *dest);
char *decodeSequence(pnuc buffer, uint32_t begin, int32_t length, char *dest);

buffer_t *loadPairedFastq(FILE* forward,
	       	   	   	      FILE* reverse,
  		 	 	 	 	  size_t maxread,
	       	   	   	      size_t maxbuffersize,
	       	   	   	      uint32_t readLength
		                 );

buffer_t *buildIndex(const char *forwardFileName, const char* reverseFileName,
					    const char *indexname,
		 	 	 	 	uint32_t minword,
		 	 	 	 	size_t maxread,
					    size_t maxbuffersize,
					    uint32_t readLength
					   );

buffer_t *newBuffer(size_t maxsize,size_t readSize,size_t maxread);
void freeBuffer(buffer_t *buffer);
void swapOrder(buffer_t *buffer);

void writeOrdoredSequences(buffer_t *buffer,FILE* output);
void writePairData(buffer_t *buffer,FILE* output);
void writeOrderData(buffer_t *buffer,FILE* output);
void writeGeneralData(buffer_t *buffer,FILE* output);

void loadSequences(buffer_t *buffer,FILE* input);
void loadPairData(buffer_t *buffer,FILE* input);
void loadGeneralData(buffer_t *buffer,FILE* input);
uint32_t loadOrder1(buffer_t *buffer,FILE* input);


void fillOrdored(buffer_t *buffer);
void sortBuffer(buffer_t *buffer);
void compSortBuffer(buffer_t *buffer);

uint8_t checkACGT(const char* src, size_t size);

void sortSuffix(buffer_t *buffer,uint32_t pos);

int8_t cmpSuffix(buffer_t *buffer,uint32_t r1,uint32_t r2,uint32_t pos);

void indexForward(buffer_t *buffer);
void indexReverse(buffer_t *buffer);

buffer_t *loadIndexedReads(const char *indexname);

int32_t lookForReads(buffer_t *buffer, pnuc key, size_t length, int32_t* endoflist);
int32_t lookForString(buffer_t *buffer, char *key, size_t length, int32_t* endoflist);
int32_t fastLookForString(buffer_t *buffer, char *key, size_t length, int32_t* fcount, int32_t* rcount, int32_t* fpos, int32_t* rpos);
int32_t nextRead(buffer_t *buffer, int32_t current, size_t length, int32_t* endoflist);
int32_t lookForReadsIds(buffer_t *buffer, int32_t key, int32_t* endoflist);
int32_t nextReadIds(buffer_t *buffer, int32_t current, int32_t* endoflist);

extern uint64_t decode16bitsnuc[];
extern uint8_t complement4nuc[];
extern uint32_t expanded8bitsnuc[];

pnuc encodeSequence(pnuc dest, char* src, uint32_t length);
pnuc shiftKey(pnuc dest, pnuc key,uint32_t shift, uint32_t keyLength);

void countLetterAt(buffer_t *buffer,uint32_t pos);
uint32_t minSuffix(buffer_t *buffer,uint32_t pos);



#endif /* ORGASM_H_ */
