.. _embl_code:


.. note::

    This article is copy-pasted from `ENA user manual <ftp://ftp.ebi.ac.uk/pub/databases/embl/doc/usrman.txt>`


The ENA flat-file format
========================

3.3  Structure of an Entry

The entries in the database are structured so as to be usable by human readers as well as by computer programs. The explanations, descriptions, classifications and other comments are in ordinary English, and the symbols and formatting employed for the base sequences themselves have been chosen for readability. Wherever possible, symbols familiar to molecular biologists have been used. At the same time, the structure is systematic enough to allow computer programs easily to read, identify, and manipulate the various types of data included. Each entry in the database is composed of lines. Different types of lines, each with its own format, are used to record the various types of data which make up the entry. In general, fixed format items have been kept to a minimum, and a more syntax-oriented structure adopted for the lines. The two exceptions to this are the sequence data lines and the feature table lines, for which a fixed format was felt to offer significant advantages to the user. Users who write programs to process the database entries should not make any assumptions about the column placement of items on lines other than these two: all other line types are free-format. 

Note that each line begins with a two-character line code, which indicates the type of information contained in the line. 

Example of an entry::

    ID   X56734; SV 1; linear; mRNA; STD; PLN; 1859 BP.
    XX
    AC   X56734; S46826;
    XX
    DT   12-SEP-1991 (Rel. 29, Created)
    DT   25-NOV-2005 (Rel. 85, Last updated, Version 11)
    XX
    DE   Trifolium repens mRNA for non-cyanogenic beta-glucosidase
    XX
    KW   beta-glucosidase.
    XX
    OS   Trifolium repens (white clover)
    OC   Eukaryota; Viridiplantae; Streptophyta; Embryophyta; Tracheophyta;
    OC   Spermatophyta; Magnoliophyta; eudicotyledons; core eudicotyledons; rosids;
    OC   fabids; Fabales; Fabaceae; Papilionoideae; Trifolieae; Trifolium.
    XX
    RN   [5]
    RP   1-1859
    RX   DOI; 10.1007/BF00039495.
    RX   PUBMED; 1907511.
    RA   Oxtoby E., Dunn M.A., Pancoro A., Hughes M.A.;
    RT   "Nucleotide and derived amino acid sequence of the cyanogenic
    RT   beta-glucosidase (linamarase) from white clover (Trifolium repens L.)";
    RL   Plant Mol. Biol. 17(2):209-219(1991).
    XX
    RN   [6]
    RP   1-1859
    RA   Hughes M.A.;
    RT   ;
    RL   Submitted (19-NOV-1990) to the INSDC.
    RL   Hughes M.A., University of Newcastle Upon Tyne, Medical School, Newcastle
    RL   Upon Tyne, NE2 4HH, UK
    XX
    DR   EuropePMC; PMC99098; 11752244.
    XX
    FH   Key             Location/Qualifiers
    FH
    FT   source          1..1859
    FT                   /organism="Trifolium repens"
    FT                   /mol_type="mRNA"
    FT                   /clone_lib="lambda gt10"
    FT                   /clone="TRE361"
    FT                   /tissue_type="leaves"
    FT                   /db_xref="taxon:3899"
    FT   mRNA            1..1859
    FT                   /experiment="experimental evidence, no additional details
    FT                   recorded"
    FT   CDS             14..1495
    FT                   /product="beta-glucosidase"
    FT                   /EC_number="3.2.1.21"
    FT                   /note="non-cyanogenic"
    FT                   /db_xref="GOA:P26204"
    FT                   /db_xref="InterPro:IPR001360"
    FT                   /db_xref="InterPro:IPR013781"
    FT                   /db_xref="InterPro:IPR017853"
    FT                   /db_xref="InterPro:IPR018120"
    FT                   /db_xref="UniProtKB/Swiss-Prot:P26204"
    FT                   /protein_id="CAA40058.1"
    FT                   /translation="MDFIVAIFALFVISSFTITSTNAVEASTLLDIGNLSRSSFPRGFI
    FT                   FGAGSSAYQFEGAVNEGGRGPSIWDTFTHKYPEKIRDGSNADITVDQYHRYKEDVGIMK
    FT                   DQNMDSYRFSISWPRILPKGKLSGGINHEGIKYYNNLINELLANGIQPFVTLFHWDLPQ
    FT                   VLEDEYGGFLNSGVINDFRDYTDLCFKEFGDRVRYWSTLNEPWVFSNSGYALGTNAPGR
    FT                   CSASNVAKPGDSGTGPYIVTHNQILAHAEAVHVYKTKYQAYQKGKIGITLVSNWLMPLD
    FT                   DNSIPDIKAAERSLDFQFGLFMEQLTTGDYSKSMRRIVKNRLPKFSKFESSLVNGSFDF
    FT                   IGINYYSSSYISNAPSHGNAKPSYSTNPMTNISFEKHGIPLGPRAASIWIYVYPYMFIQ
    FT                   EDFEIFCYILKINITILQFSITENGMNEFNDATLPVEEALLNTYRIDYYYRHLYYIRSA
    FT                   IRAGSNVKGFYAWSFLDCNEWFAGFTVRFGLNFVD"
    XX
    SQ   Sequence 1859 BP; 609 A; 314 C; 355 G; 581 T; 0 other;
         aaacaaacca aatatggatt ttattgtagc catatttgct ctgtttgtta ttagctcatt        60
         cacaattact tccacaaatg cagttgaagc ttctactctt cttgacatag gtaacctgag       120
         tcggagcagt tttcctcgtg gcttcatctt tggtgctgga tcttcagcat accaatttga       180
         aggtgcagta aacgaaggcg gtagaggacc aagtatttgg gataccttca cccataaata       240
         tccagaaaaa ataagggatg gaagcaatgc agacatcacg gttgaccaat atcaccgcta       300
         caaggaagat gttgggatta tgaaggatca aaatatggat tcgtatagat tctcaatctc       360
         ttggccaaga atactcccaa agggaaagtt gagcggaggc ataaatcacg aaggaatcaa       420
         atattacaac aaccttatca acgaactatt ggctaacggt atacaaccat ttgtaactct       480
         ttttcattgg gatcttcccc aagtcttaga agatgagtat ggtggtttct taaactccgg       540
         tgtaataaat gattttcgag actatacgga tctttgcttc aaggaatttg gagatagagt       600
         gaggtattgg agtactctaa atgagccatg ggtgtttagc aattctggat atgcactagg       660
         aacaaatgca ccaggtcgat gttcggcctc caacgtggcc aagcctggtg attctggaac       720
         aggaccttat atagttacac acaatcaaat tcttgctcat gcagaagctg tacatgtgta       780
         taagactaaa taccaggcat atcaaaaggg aaagataggc ataacgttgg tatctaactg       840
         gttaatgcca cttgatgata atagcatacc agatataaag gctgccgaga gatcacttga       900
         cttccaattt ggattgttta tggaacaatt aacaacagga gattattcta agagcatgcg       960
         gcgtatagtt aaaaaccgat tacctaagtt ctcaaaattc gaatcaagcc tagtgaatgg      1020
         ttcatttgat tttattggta taaactatta ctcttctagt tatattagca atgccccttc      1080
         acatggcaat gccaaaccca gttactcaac aaatcctatg accaatattt catttgaaaa      1140
         acatgggata cccttaggtc caagggctgc ttcaatttgg atatatgttt atccatatat      1200
         gtttatccaa gaggacttcg agatcttttg ttacatatta aaaataaata taacaatcct      1260
         gcaattttca atcactgaaa atggtatgaa tgaattcaac gatgcaacac ttccagtaga      1320
         agaagctctt ttgaatactt acagaattga ttactattac cgtcacttat actacattcg      1380
         ttctgcaatc agggctggct caaatgtgaa gggtttttac gcatggtcat ttttggactg      1440
         taatgaatgg tttgcaggct ttactgttcg ttttggatta aactttgtag attagaaaga      1500
         tggattaaaa aggtacccta agctttctgc ccaatggtac aagaactttc tcaaaagaaa      1560
         ctagctagta ttattaaaag aactttgtag tagattacag tacatcgttt gaagttgagt      1620
         tggtgcacct aattaaataa aagaggttac tcttaacata tttttaggcc attcgttgtg      1680
         aagttgttag gctgttattt ctattatact atgttgtagt aataagtgca ttgttgtacc      1740
         agaagctatg atcataacta taggttgatc cttcatgtat cagtttgatg ttgagaatac      1800
         tttgaattaa aagtcttttt ttattttttt aaaaaaaaaa aaaaaaaaaa aaaaaaaaa       1859
    //



The currently used line types, along with their respective line codes, are listed below:

==================================== =================================
     ID - identification             (begins each entry; 1 per entry)
     AC - accession number           (>=1 per entry)
     PR - project identifier         (0 or 1 per entry)
     DT - date                       (2 per entry)
     DE - description                (>=1 per entry)
     KW - keyword                    (>=1 per entry)
     OS - organism species           (>=1 per entry)
     OC - organism classification    (>=1 per entry)
     OG - organelle                  (0 or 1 per entry)
     RN - reference number           (>=1 per entry)
     RC - reference comment          (>=0 per entry)
     RP - reference positions        (>=1 per entry)
     RX - reference cross-reference  (>=0 per entry)
     RG - reference group            (>=0 per entry)
     RA - reference author(s)        (>=0 per entry)
     RT - reference title            (>=1 per entry)
     RL - reference location         (>=1 per entry)
     DR - database cross-reference   (>=0 per entry)
     CC - comments or notes          (>=0 per entry)
     AH - assembly header            (0 or 1 per entry)   
     AS - assembly information       (0 or >=1 per entry)
     FH - feature table header       (2 per entry)
     FT - feature table data         (>=2 per entry)    
     XX - spacer line                (many per entry)
     SQ - sequence header            (1 per entry)
     CO - contig/construct line      (0 or >=1 per entry) 
     bb - (blanks) sequence data     (>=1 per entry)
     // - termination line           (ends each entry; 1 per entry)
==================================== =================================
     
Note that some entries will not contain all of the line types, and some line types occur many times in a single entry. As indicated, each entry begins with an identification line (ID) and ends with a terminator line (//). The various line types appear in entries in the order in which they are listed above (except for XX lines which may appear anywhere between the ID and SQ lines).

