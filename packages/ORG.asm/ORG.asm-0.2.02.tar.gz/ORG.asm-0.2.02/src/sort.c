/*
 * sort.c
 *
 *  Created on: 14 sept. 2012
 *      Author: coissac
 */

#include "orgasm.h"
#include "_sse.h"

#include "debug.h"

// We used the heavyiest bit of the order1 index to
// store the sorted status of a read
// these macro are setup to manipulate this bit

#define SETSORTED(x)   ((x) | 0x80000000)
#define CLEARSORTED(x) ((x) & 0x7FFFFFFF)
#define GETSORTED(x)   ((x) & 0x80000000)


// fillOrdored function fill the two int arrays
// pointed by the members order1 and order2 with
// increasing int values from 1 to n (order1)
// and fill the order2 array in a way that link
// paired reads which are interleaved by the
// loadpair function
void fillOrdored(buffer_t *buffer)
{
	um128 counter;
	um128 pair;
	uint32_t *index;
	uint32_t *endex;
	uint32_t *index2;

	index  = buffer->order1;
	index2 = buffer->order2;
	endex  = index + buffer->readCount;

	counter.u32[0]=0;
	counter.u32[1]=1;
	counter.u32[2]=2;
	counter.u32[3]=3;

	pair.u32[0]=1;
	pair.u32[1]=0;
	pair.u32[2]=3;
	pair.u32[3]=2;


	for (; index < (endex-3) ; index+=4,index2+=4)
	{
      _MM_STORE_SI128((__m128i*)index,counter.i);
      counter.i=_MM_ADD_EPI32(counter.i,_MM_SET1_EPI32(4));

      _MM_STORE_SI128((__m128i*)index2,pair.i);
      pair.i=_MM_ADD_EPI32(pair.i,_MM_SET1_EPI32(4));

      //      DEBUG("index : %d  %d:%d:%d:%d",index-(buffer->order),
//    		        index[0],index[1],index[2],index[3]);
	}

	for (; index < endex ; index++,index2++)
	{
		*index = *(index-1)+1;
		*index2= (*index ^ 0x1);
//		DEBUG("index : %d  %d",index-(buffer->order),
//  		        index[0]);

	}

}

// partialSortBuffer, sort lexicographically the reads suffix
// stored in buffer from the position [start;stop[.
// for this function reads are indexed from 0 to n-1 with
// n the read count.
//
// This function is recursive

void partialSortBuffer(buffer_t *buffer,
		               uint32_t start, uint32_t stop,
		               uint32_t shift,
		               uint32_t nextprint)
{
	uint32_t wordStat[256];
	uint32_t *index = buffer->order1 + start;
	uint32_t *endex = buffer->order1 + stop;

	uint8_t  word;
	uint32_t i;
	uint32_t swap;
	uint32_t pairswap;
	uint32_t next;
	uint32_t first;
	uint32_t pair;
	uint32_t *pairp;
	uint32_t *swapp;
	uint32_t cumsum=start;
	uint32_t backtolastswap=FALSE;


	// Just print some stats on the sorting progress

	if (shift==1 && start > nextprint)
	{
		fprintf(stderr,"%9d sequences sorted\r",start);
		nextprint=start;
	}

	// If we sort just one sequence or a suffix of length=0
	// this is finnished

	if ((stop - start)<=1 || shift==buffer->recordSize)
		return;

	// we clear all word occurrences

	bzero((void *)wordStat, 256 * sizeof(uint32_t));

	// we count occurrences of each word in one pass

	for (; index < endex; index++)
		wordStat[((uint8_t*)(buffer->records))[*index * buffer->recordSize + shift]]++;

    // And we compute the cumulative sum of ocurences

	for (i=0; i < 256; i++)
	{
		swap=wordStat[i];
		wordStat[i]=cumsum;
		cumsum+=swap;
	}

	// Do the card sorting by itself

	for (i=start; i < stop; i++)
	{
		// I skip already ordored sequences
		while (i < stop && GETSORTED(buffer->order1[i]))
			i++;

		// No more cells to sort
		if (i==stop) continue;

		// next contains the id of the next sequence to sort
		first  = buffer->order1[i];
		next   = first;
		// pair contains the id of the paired sequence
		pair  = buffer->order2[i];

		do
		{
			// this is the next word to sort
			word  = ((uint8_t*)(buffer->records))[next * buffer->recordSize + shift];


			// Now I know where I'll store the paired read
			//    See below for understanding this comment
			if (backtolastswap)
			{
				backtolastswap=FALSE;
				buffer->order2[pair]=wordStat[word];

			}

			// I compute the destination for this word
			swapp = buffer->order1 + wordStat[word];
			pairp = buffer->order2 + wordStat[word];

			// And I save the value previously stored at these locations.
			swap  = *swapp;
			pairswap = *pairp;

			// I save the new sequence id and set the SORTED flag

			*swapp= SETSORTED(next);


			// I save the pair info

			if (pair!=wordStat[word])
			{
				// in this case we are not swapping paired reads

				// I conserve in the new place the next pair information
				*pairp= pair;

				// I store for the paired reads the new position of its pair
				buffer->order2[pair]=wordStat[word];
			}
			else
			{
				// In this case I'm swapping to paired reads

				// I'm moving the next pair so I don't know yet where il will be placed
				*pairp= 0xFFFFFFFF;

				// I remember this strange status
				backtolastswap=TRUE;
			}

			// I initialize next for the following loop cycle
			next  = swap;

			// same for pair with a special case if we are swaping paired reads
			if (pair!=wordStat[word])
				pair = pairswap;

			wordStat[word]++;

		} while (next!=first);

	}

	// Clear all the sorted status
	for (i=start; i < stop; i++)
		buffer->order1[i]&=0x7FFFFFFF;

	// Run recurcively the algorithm on each sub set
	for (i=0; i < 256; i++)
	{
		if (i>0 && wordStat[i] < wordStat[i-1])
			wordStat[i]=wordStat[i-1];

		stop=wordStat[i];
		if (stop - start > 1)
			partialSortBuffer(buffer,start,stop,shift+1,nextprint);
		start=stop;
	}

}


void sortBuffer(buffer_t *buffer)
{
	fprintf(stderr,"\nSorting reads...\n\n");

	fillOrdored(buffer);
	partialSortBuffer(buffer,0,buffer->readCount,0,DISPLAYSTEP);

	fprintf(stderr,"%9zd sequences sorted\n",buffer->readCount);
}


void countLetterAt(buffer_t *buffer,uint32_t pos)
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

int8_t cmpSuffix(buffer_t *buffer,uint32_t r1,uint32_t r2,uint32_t pos)
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

uint32_t minSuffix(buffer_t *buffer,uint32_t pos)
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
			// DEBUG("1 : mini=%d  current=%d (%d)",
			//            mini,
			//            current,
			//            cmpSuffix(buffer,order[count[mini]],order[count[current]],pos));
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

void sortSuffix(buffer_t *buffer,uint32_t pos)
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

// indexForward function fill the int array pointed by the member index1
// of the structure buffer with a hash index of the reads based on the
// eight first bases of the sequences

void indexForward(buffer_t *buffer)
{
	int32_t i;
	uint16_t hash;
	uint32_t swap;
	uint32_t cumsum=0;
	int32_t imax = 1 << 16;

	bzero((void *)(buffer->index1), imax * sizeof(uint32_t));

	for (i=0; i < buffer->readCount; i++)
	{
		hash=*((uint16_t*)(buffer->records + i * buffer->recordSize));
#ifdef LITTLE_END
		hash = ((hash & 0xFF) << 8) | (hash >> 8);
#endif
		buffer->index1[hash]++;
	}

	for (i=0; i < imax; i++)
	{
		swap=buffer->index1[i];
		buffer->index1[i]=cumsum;
		cumsum+=swap;
	}
}

// indexReverse function fill the int array pointed by the member index2
// of the structure buffer with a hash index of the reads based on the
// eight first bases of the reverse complement of the sequences


void indexReverse(buffer_t *buffer)
{
	int32_t i;
	uint16_t hash;
	uint32_t swap;
	uint32_t cumsum=0;
	int32_t imax = 1 << 16;


	bzero((void *)(buffer->index2), imax * sizeof(uint32_t));

	for (i=0; i < buffer->readCount; i++)
	{
		hash = *((uint16_t*)(buffer->records + i * buffer->recordSize + CODELENGTH(buffer->readSize))-1);
#ifdef LITTLE_END
		hash = complement4nuc[hash & 0x00FF] | (complement4nuc[(hash >> 8) & 0x00FF] << 8);
#else
		hash = (complement4nuc[hash & 0x00FF] << 8) | complement4nuc[(hash >> 8) & 0x00FF];
#endif
		buffer->index2[hash]++;
	}

	for (i=0; i < imax; i++)
	{
		swap=buffer->index2[i];
		buffer->index2[i]=cumsum;
		cumsum+=swap;
	}
}
