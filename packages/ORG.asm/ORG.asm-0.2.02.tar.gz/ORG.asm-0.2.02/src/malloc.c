/*
 * malloc.c
 *
 *  Created on: 12 sept. 2012
 *      Author: coissac
 */

#include "orgasm.h"

//#include "debug.h"

void   *util_malloc(int32_t chunksize, const char *filename, int32_t line)
{
	void * chunk;

	chunk = calloc(1,chunksize);

	if (!chunk)
		GENERICERROR(filename,line,"MEMORY ERROR",MEM_ALLOC_ERROR,
				     "Could not allocate a chunk pf %d bytes.",chunksize);

	DEBUG("Malloc Call from %s@%d : %p for %d bytes",filename,line,chunk,chunksize);
	return chunk;
}

/*
 * Function Name: util_realloc(void *chunk, int32_t newsize, const char *filename, int32_t line)
 * Description:   Overloading realloc funstion, changes the size of the memory object pointed to by chunk
 * to the size specified by newsize. If memory cannot be allocated, gives the error on stderr and aborts.
 */
void   *util_realloc(void *chunk, int32_t newsize, const char *filename, int32_t    line)
{
	void *newchunk;

	newchunk = realloc(chunk,newsize);

	if (!newchunk)
		GENERICERROR(filename,line,"MEMORY ERROR",MEM_ALLOC_ERROR,
				     "Could not reallocate chunk %p to %d bytes.",chunk,newsize);

	DEBUG("Realloc Call from %s@%d : %p -> %p for %d bytes",filename,line,chunk,newchunk,newsize);
	return newchunk;
}

/*
 * Function Name: util_free(void *chunk)
 * Description:   Returns the memory specified by chunk back to operating syste.
 */
void    util_free(void *chunk, const char *filename, int32_t    line)
{
	DEBUG("Free Call from %s@%d : %p",filename,line,chunk);
	free(chunk);
}
