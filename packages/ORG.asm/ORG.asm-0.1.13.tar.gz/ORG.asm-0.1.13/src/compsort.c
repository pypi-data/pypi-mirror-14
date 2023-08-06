/*
 * sort.c
 *
 *  Created on: 14 sept. 2012
 *      Author: coissac
 */

#include "orgasm.h"
#include "_sse.h"

#include "debug.h"

#define SETSORTED(x)   ((x) | 0x80000000)
#define CLEARSORTED(x) ((x) & 0x7FFFFFFF)
#define GETSORTED(x)   ((x) & 0x80000000)

/**
 * internal function called recursively from the
 * compSortBuffer function
 *
 * buffer_t *buffer,
 * uint32_t start, uint32_t stop,
 * uint32_t shift,
 * uint32_t nextprint   // parameter used to manage printing of advancement
 * 						// of the sort algorithm
 *
 */

void partialCompSortBuffer(buffer_t *buffer,
		               uint32_t start, uint32_t stop,
		               int32_t shift,
		               uint32_t nextprint)
{
	uint32_t wordStat[256];
	uint32_t *index = buffer->order1 + start;
	uint32_t *endex = buffer->order1 + stop;

	uint8_t  word;
	uint32_t i;
	uint32_t swap;
//	uint32_t pairswap;
	uint32_t next;
	uint32_t first;
//	uint32_t pair;
//	uint32_t *pairp;
	uint32_t *swapp;
	uint32_t cumsum=start;
//	uint32_t backtolastswap=FALSE;
	int32_t shiftmax=0;

	if (shift > shiftmax) shiftmax=shift;

	if (shift==shiftmax && start > nextprint)
	{
		fprintf(stderr,"%9d sequences sorted\r",start);
		nextprint=start;
	}

	if ((stop - start)<=1 || shift<0)
		return;

	// we clear all word occurrences

	bzero((void *)wordStat, 256 * sizeof(uint32_t));

	// we count occurrences of each word in one pass

	for (; index < endex; index++)
		wordStat[complement4nuc[((uint8_t*)(buffer->records))[*index * buffer->recordSize + shift]]]++;

	for (i=0; i < 256; i++)
	{
		swap=wordStat[i];
		wordStat[i]=cumsum;
		cumsum+=swap;
	}

	// Do the count sorting by itself

	for (i=start; i < stop; i++)
	{
		while (i < stop && GETSORTED(buffer->order1[i]))
			i++;

		// No more cells to sort
		if (i==stop) continue;

		// next contains the id of the next sequence to sort
		first  = buffer->order1[i];
		next   = first;

		do
		{
			// this is the next word to sort
			word  = complement4nuc[((uint8_t*)(buffer->records))[next * buffer->recordSize + shift]];

			// I compute the destination for this word
			swapp = buffer->order1 + wordStat[word];

			// And I save the value previously stored at these locations.
			swap  = *swapp;

			// I save the new sequence id and set the SORTED flag

			*swapp= SETSORTED(next);

			// I initialize next for the following loop cycle
			next  = swap;


			wordStat[word]++;

		} while (next!=first);

	}

	for (i=start; i < stop; i++)
		buffer->order1[i]&=0x7FFFFFFF;

	for (i=0; i < 256; i++)
	{
		if (i>0 && wordStat[i] < wordStat[i-1])
			wordStat[i]=wordStat[i-1];

		stop=wordStat[i];
		if (stop - start > 1)
			partialCompSortBuffer(buffer,start,stop,shift-1,nextprint);
		start=stop;
	}

}


void compSortBuffer(buffer_t *buffer)
{
	uint32_t initialshift;
	fprintf(stderr,"\nSorting reads...\n\n");

	fillOrdored(buffer);
	initialshift = (buffer->readSize >> 2) - ((buffer->readSize & 3) ? 0:1);

	partialCompSortBuffer(buffer,0,buffer->readCount,initialshift,DISPLAYSTEP);

	fprintf(stderr,"%9zd sequences sorted\n",buffer->readCount);
}


void countEndLetterAt(buffer_t *buffer,uint32_t pos)
{
	uint32_t shift;
	uint32_t inshift;
	uint8_t  mask;
	uint8_t  *record;
	int32_t  *count=buffer->letterCount;
	uint32_t i;

	count[0]=count[1]=count[2]=count[3]=0;

	shift  = pos >> 2;
	inshift= (3 - (pos & 3)) * 2;
	mask   = (1 << inshift) | (1 << (inshift+1));

	for(record = (uint8_t*)(buffer->records) + shift, i=0;
		i < buffer->readCount;
		i++, record+=buffer->recordSize)
		count[(*record & mask) >> inshift]++;

	// DEBUG("At position %9d : A=%9d C=%9d T=%9d G=%9d",pos,count[0],count[1],count[2],count[3]);
}

int8_t cmpCompSuffix(buffer_t *buffer,uint32_t r1,uint32_t r2,uint32_t pos)
{
	uint32_t shift;
	uint8_t  mask;
	uint8_t  *pr1;
	uint8_t  *pr2;
	uint8_t  vr1=0;
	uint8_t  vr2=0;

	shift  = pos >> 2;
	mask= (1 << ((4 - (pos & 3)) * 2))-1;

	// DEBUG("pos : %d mask : %d,%x",pos,shift,mask);

	pr1 = ((uint8_t*)(buffer->records)) + shift + buffer->recordSize * r1;
	pr2 = ((uint8_t*)(buffer->records)) + shift + buffer->recordSize * r2;

	vr1 = *pr1 & mask;
	vr2 = *pr2 & mask;

	while(shift < buffer->recordSize  && vr1==vr2)
	{
	//	DEBUG("Shift:%d  %d  %d",shift,vr1,vr2);

		shift++;
		pr1++,
		pr2++,

		vr1 = *pr1;
		vr2 = *pr2;
	}

	return (vr1==vr2) ? 0 : (vr1 < vr2) ? -1:1;

}

uint32_t minCompSuffix(buffer_t *buffer,uint32_t pos)
{
	int32_t  mini;
	uint32_t current;
	int32_t  *count=buffer->letterCount;
	uint32_t *order = buffer->order1;

	mini=0;

	if (count[1]>=0)
	{
		if (count[mini] < 0)
			mini= 1;
		else
		{
			current= 1;
			// DEBUG("1 : mini=%d  current=%d (%d)",mini,current,cmpSuffix(buffer,order[count[mini]],order[count[current]],pos));
			if (cmpSuffix(buffer,order[count[mini]],order[count[current]],pos) > 0)
				mini = current;
		}
	}

	if (count[2]>=0)
	{
		if (count[mini] < 0)
			mini= 2;
		else
		{
			current= 2;
			// DEBUG("2 : mini=%d  current=%d (%d)",mini,current,cmpSuffix(buffer,order[count[mini]],order[count[current]],pos));
			if (cmpSuffix(buffer,order[count[mini]],order[count[current]],pos) > 0)
				mini = current;
		}
	}

	if (count[3]>=0)
	{
		if (count[mini] < 0)
			mini= 3;
		else
		{
			current= 3;
			// DEBUG("3 : mini=%d  current=%d (%d)",mini,current,cmpSuffix(buffer,order[count[mini]],order[count[current]],pos));
			if (cmpSuffix(buffer,order[count[mini]],order[count[current]],pos) > 0)
				mini = current;
		}
	}

	// DEBUG("4 : seqid=%d  current=%d (%d)",order[count[mini]],mini,cmpSuffix(buffer,order[count[mini]],order[count[current]],pos));
	return mini;
}

void sortCompSuffix(buffer_t *buffer,uint32_t pos)
{
	uint32_t nextmini;
	int32_t count[4];
	int32_t  *cumsum = buffer->letterCount;
	int32_t  max=0;
	int32_t  i;
	uint32_t nextprint=DISPLAYSTEP;

	fprintf(stderr,"\nSorting suffix @ %d...\n\n",pos);


	countLetterAt(buffer,pos);
	countLetterAt(buffer,pos-1);

	count[0]=cumsum[0];
	cumsum[0]= (count[0]) ? max:-1;
	max+=count[0];

	count[1]=cumsum[1];
	cumsum[1]= (count[1]) ? max:-1;
	max+=count[1];

	count[2]=cumsum[2];
	cumsum[2]= (count[2]) ? max:-1;
	max+=count[2];

	count[3]=cumsum[3];
	cumsum[3]= (count[3]) ? max:-1;

	// DEBUG("Cumsum    @ %9d : A=%9d C=%9d T=%9d G=%9d",pos,cumsum[0],cumsum[1],cumsum[2],cumsum[3]);


	for (i=0; i < (int32_t)buffer->readCount; i++)
	{
		nextmini = minSuffix(buffer,pos);
		buffer->order2[i]=buffer->order1[buffer->letterCount[nextmini]];
		cumsum[nextmini]++;
		count[nextmini]--;
		if (count[nextmini]==0)
			cumsum[nextmini]=-1;

		if (i > nextprint)
		{
			fprintf(stderr,"%9d suffixes sorted\r",nextprint);
			nextprint+=DISPLAYSTEP;
		}

	}

	fprintf(stderr,"%9d suffixes sorted\n",i);


	// DEBUG("Minimum read @ pos = %4d is %9d",pos,nextmini);
}
