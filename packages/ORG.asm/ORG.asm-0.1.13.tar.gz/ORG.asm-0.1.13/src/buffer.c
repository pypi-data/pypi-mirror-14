/*
 * buffer.c
 *
 *  Created on: 12 sept. 2012
 *      Author: coissac
 */


#include "orgasm.h"

buffer_t *newBuffer(size_t maxsize,size_t readSize, size_t maxread)
{
#define MASK  ((size_t)0xF)
#define CLEAN ((size_t)~MASK)
#define MIN(x,y) (((x) > (y)) ? (y):(x))

	buffer_t* rep;
	size_t rsize=round16(readSize)/4 + 2 * sizeof(uint32_t);

	if (((maxsize-48) / rsize) > (size_t)0xFFFFFFFF)
		maxsize = (size_t)0xFFFFFFFF * rsize + 48;

	if (maxread>0)
		maxsize = MIN(maxread*rsize+48,maxsize);


	rep = MALLOC(sizeof(buffer_t));
	rep->arena  = MALLOC(maxsize);

	if ((size_t)(rep->arena) & MASK)
		rep->records = (char*)PTR16(rep->arena);
	else
		rep->records=rep->arena;

	maxsize = maxsize - (rep->arena - rep->records);

	rep->maxrecord = maxsize / rsize;

	if (rep->maxrecord > 0x7FFFFFFF)
		rep->maxrecord = 0x7FFFFFFF;

	rep->readSize=readSize;
	rep->recordSize=round16(readSize)/4;
	rep->readCount=0;
	rep->order1 = (uint32_t*) PTR16(rep->records + rep->maxrecord * rep->recordSize);
	rep->order2 = (uint32_t*) PTR16(rep->order1 + rep->maxrecord);

	rep->index1 = MALLOC(sizeof(uint32_t) * (1 << 16));
	rep->index2 = MALLOC(sizeof(uint32_t) * (1 << 16));

	rep->complement = NULL;

	return rep;

#undef MASK
#undef CLEAN

};

void freeBuffer(buffer_t *buffer)
{
	if (buffer!=NULL)
	{
		FREE(buffer->arena);
		FREE(buffer->index1);
		FREE(buffer->index2);

		if (buffer->complement)
			FREE(buffer->complement);
		FREE(buffer);
	}
};

void swapOrder(buffer_t *buffer)
{
	uint32_t *order;

	order = buffer->order1;
	buffer->order1=buffer->order2;
	buffer->order2=order;

}

