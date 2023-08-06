/*
 * orgasmi.c
 *
 *  Created on: 11 juil. 2012
 *      Author: coissac
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

#include "orgasm.h"

#include "debug.h"

#define LARGE_TEST
#define LOAD_ONLY

#define VERSION "0.1"

/* ----------------------------------------------- */
/* printout help                                   */
/* ----------------------------------------------- */
#define PP fprintf(stdout,

static void PrintHelp()
{
        PP      "------------------------------------------\n");
        PP      " ORGanel ASseMbler Version %s\n", VERSION);
        PP      "------------------------------------------\n");
        PP      "synopsis : Index lexicographicaly a set of paired Illumina reads in fastq format\n");
        PP      "usage: orgasmi -o <index> <forward_fastq_file> <reverse_fastq_file>\n");
        PP      "------------------------------------------\n");
        PP      "options:\n");
        PP      "-o    : The name of the index ouput files");
        PP      "        orgasmi creates four files  :\n");
        PP      "            <index>.ogx : contains information concerning the index\n");
        PP      "            <index>.ofx : contains the sequences themselves and the forward index\n");
        PP      "            <index>.orx : contains reverse index\n");
        PP      "            <index>.opx : contains read pairing data\n\n");
        PP      "        The assembler will need all these file to process assembling\n\n");
        PP      "-M    : If specified the count in million of reads to index\n\n");
        PP      "-l    : read length to consider (must be an odd length)\n\n");
        PP      "-h    : [H]elp - print <this> help\n\n");
        PP      "\n");
        PP      "------------------------------------------\n");
        PP		" http://www.metabarcoding.org/\n");
        PP      "------------------------------------------\n\n");
        PP      "\n");

}

#undef PP

/* ----------------------------------------------- */
/* printout usage and exit                         */
/* ----------------------------------------------- */

#define PP fprintf(stderr,

static void ExitUsage(stat)
        int stat;
{
        PP      "usage: orgasmi [-o <indexname>] <forward.fastq> <reverse.fastq>\n");
        PP      "type \"orgasmi -h\" for help\n");

        if (stat)
            exit(stat);
}

#undef  PP


int main(int argc, char *argv[])
{
	buffer_t* reads;
	char* indexfiles=NULL;
	size_t toread=0;
	uint32_t readLength=0;

	int           carg;
	int       errflag=0;

	char* forwardFileName;
	char* reverseFileName;

#define CMPLENGTH 100




while ((carg = getopt(argc, argv, "hM:o:l:")) != -1) {

 switch (carg) {
                            /* -------------------- */
    case 'h':               /* help                 */
                            /* -------------------- */
       PrintHelp();
       exit(0);
       break;

       	   	   	   	   	   /* -------------------- */
    case 'o':              /* index name           */
    					   /* -------------------- */
    	indexfiles = MALLOC(strlen(optarg)+1);
    	strcpy(indexfiles,(const char*)optarg);
    	break;

    					   /* -------------------- */
    case 'M':              /* sequence to index    */
    					   /* -------------------- */
    	toread = atoll((const char*)optarg) * 1000000;
    	break;

		   	   	   	   	   /* -------------------- */
    case 'l':              /* index name           */
		   	   	   	   	   /* -------------------- */

    	readLength = atoll((const char*)optarg);
    	break;

	case '?':               /* bad option           */
                            /* -------------------- */
        errflag++;
        break;
		}

}

/**
 * check the path to the database is given as last argument
 */


if ((argc -= optind) == 2)
{

	forwardFileName = MALLOC(strlen(argv[optind])+1);
	strcpy(forwardFileName,argv[optind]);
	optind++;
	reverseFileName = MALLOC(strlen(argv[optind])+1);
	strcpy(reverseFileName,argv[optind]);
}
else
{
	errflag++;
	forwardFileName=NULL;
	reverseFileName=NULL;
}


if (indexfiles == NULL)
	errflag++;

if (errflag)
	ExitUsage(errflag);

#define MAXREAD 2000000000

	reads = buildIndex(forwardFileName,reverseFileName,indexfiles,95,toread,MAXREAD,readLength);

	freeBuffer(reads);

	return 0;
}
