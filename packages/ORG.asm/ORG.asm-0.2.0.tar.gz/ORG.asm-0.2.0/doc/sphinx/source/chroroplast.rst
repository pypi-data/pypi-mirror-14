In [111]: r = Index('../../samples/AA')

Loading global data...

Done.

Reading indexed sequence reads...

 25553356 sequences read

Reading indexed pair data...

Done.

Loading reverse index...

Done.

Indexing reverse complement sequences ...


Fast indexing forward reads...


Fast indexing reverse reads...

Done.

In [113]: p.keys()
Out[113]: 
['petD', 'petG', 'psbN', 'petA', 'rpl2', 'petB', 'petL',
 'ndhC', 'petN', 'ycf2', 'ycf3', 'rpl23', 'rpl22', 'ndhE',
 'psaI', 'psaJ', 'ndhI', 'psaA', 'psaB', 'psaC', 'psbT',
 'accD', 'matK', 'rpl14', 'rpl36', 'rpl16', 'clpP', 'cemA',
 'ndhA', 'psbB', 'ycf4', 'rbcL', 'ndhB', 'ccsA', 'rps15',
 'ndhD', 'psbD', 'rpoC1', 'rpl32', 'rpoC2', 'ndhF', 'rpl33',
 'rpl20', 'rpoB', 'atpI', 'atpH', 'rpoA', 'atpB', 'atpA',
 'ycf1', 'atpF', 'atpE', 'ndhG', 'psbE', 'rps12', 'rps11',
 'psbF', 'psbA', 'rps16', 'psbC', 'rps14', 'psbM', 'ndhK',
 'rps19', 'rps18', 'psbI', 'psbH', 'psbK', 'psbJ', 'rps7',
 'ndhJ', 'rps4', 'rps3', 'rps2', 'psbL', 'rps8', 'ndhH',
 'psbZ']

In [113]: gp = ['rbcL','matK','ndhA',
      'rpoA','atpA','atpH',
      'rpoA','atpB','psbN',
      'psbT','psbB','psbD',
      'psbE','psbF','psbA',
      'psbC','psbM','psbI',
      'psbH','psbK','psbJ',
      'psbL','psbZ']


In [114]: p2=dict(x for x in protChloroArabidopsis.items() if x[0] in gp)

In [115]: p2=dict(x for x in p.items() if x[0] in gp)

In [116]: m = r.lookForSeeds(p2)
  99.9 % |#################################################/ ] remain : 00:00:00
In [117]: s = matchtoseed(m,r)

In [118]: asm = Assembler(r)

In [119]: a = tango(asm,s,mincov=1,minread=10,minoverlap=40)
Cycle :        3  (4 nodes /  0.0% fake) Waiting points :     3209 / 3208.00  Gene: None 

JumpGap on read 25547928

Cycle :       47  (88 nodes /  4.5% fake) Waiting points :     3212 / 3208.72  Gene: None 

JumpGap on read 2724088

Cycle :   109930  (218736 nodes /  9.5% fake) Waiting points :     3211 / 3358.00  Gene: None 

JumpGap on read 4432167

Cycle :   109939  (218750 nodes /  9.5% fake) Waiting points :     3211 / 3354.77  Gene: None 

JumpGap on read 24209366

Cycle :   160894  (320346 nodes / 10.0% fake) Waiting points :     3208 / 3476.05  Gene: None 

JumpGap on read 15356408

Cycle :   162299  (321604 nodes / 10.3% fake) Waiting points :     2443 / 2761.28  Gene: None 

JumpGap on read 11509091

Cycle :   162316  (321634 nodes / 10.3% fake) Waiting points :     2443 / 2745.91  Gene: None 

JumpGap on read 24781220

Cycle :   163703  (324406 nodes / 10.8% fake) Waiting points :     2436 / 2447.49  Gene: None 

JumpGap on read 25245800

Cycle :   166921  (330508 nodes / 12.0% fake) Waiting points :     2266 / 2458.52  Gene: atpA 
In [120]: asm.cleanDeadBranches()

Remaining edges : 292066 node : 292020
Out[120]: 19931

In [121]: cg = asm.compactAssembling()
Compacting graph :
 Stem           1 :    251 bp (total :    251) coverage : 458.51
 Stem           2 :   1119 bp (total :   1370) coverage :  31.47
 Stem           3 :     31 bp (total :   1401) coverage :  18.94
 Stem           4 :     98 bp (total :   1499) coverage :  47.95
 Stem           5 :     20 bp (total :   1519) coverage :   0.00
 Stem           6 :      1 bp (total :   1520) coverage : 404.00
 Stem           7 :     39 bp (total :   1559) coverage :  20.20
 Stem           8 :     12 bp (total :   1571) coverage :   0.00
 Stem           9 :   1750 bp (total :   3321) coverage : 604.10
 Stem          10 :      2 bp (total :   3323) coverage : 168.33
 Stem          11 :   1568 bp (total :   4891) coverage : 1055.90
 Stem          12 :     27 bp (total :   4918) coverage : 331.86
 Stem          13 :     27 bp (total :   4945) coverage : 216.43
 Stem          14 :    124 bp (total :   5069) coverage :  54.94
 Stem          15 :   1574 bp (total :   6643) coverage : 604.72
 Stem          16 :     35 bp (total :   6678) coverage : 1388.75
 Stem          17 :      2 bp (total :   6680) coverage : 437.67
 Stem          18 :     39 bp (total :   6719) coverage :  83.32
 Stem          19 :    279 bp (total :   6998) coverage : 778.42
 Stem          20 :     17 bp (total :   7015) coverage : 162.72
 Stem          21 :    902 bp (total :   7917) coverage : 1140.75
 Stem          22 :     76 bp (total :   7993) coverage :  20.99
 Stem          23 :     88 bp (total :   8081) coverage : 204.27
 Stem          24 :     87 bp (total :   8168) coverage :  25.25
 Stem          25 :     13 bp (total :   8181) coverage :  43.29
 Stem          26 :     10 bp (total :   8191) coverage : 707.00
 Stem          27 :    107 bp (total :   8298) coverage :  54.24
 Stem          28 :    102 bp (total :   8400) coverage : 1092.37
 Stem          29 :   2289 bp (total :  10689) coverage : 619.01
 Stem          30 :     27 bp (total :  10716) coverage : 292.18
 Stem          31 :     12 bp (total :  10728) coverage :  15.54
 Stem          32 :     19 bp (total :  10747) coverage :   0.00
 Stem          33 :     17 bp (total :  10764) coverage :  72.94
 Stem          34 :   3415 bp (total :  14179) coverage : 599.41
 Stem          35 :    351 bp (total :  14530) coverage : 645.88
 Stem          36 :    696 bp (total :  15226) coverage :  24.20
 Stem          37 :     12 bp (total :  15238) coverage :   7.77
 Stem          38 :     76 bp (total :  15314) coverage : 472.21
 Stem          39 :     76 bp (total :  15390) coverage :  32.79
 Stem          40 :    100 bp (total :  15490) coverage :  48.00
 Stem          -3 :     31 bp (total :  15521) coverage :  18.94
 Stem          41 :     88 bp (total :  15609) coverage :  41.99
 Stem          42 :      8 bp (total :  15617) coverage :   0.00
 Stem          43 :      8 bp (total :  15625) coverage : 123.44
 Stem          44 :     91 bp (total :  15716) coverage :  27.45
 Stem          45 :     19 bp (total :  15735) coverage : 409.05
 Stem          46 :     13 bp (total :  15748) coverage : 165.93
 Stem          47 :     15 bp (total :  15763) coverage :  88.38
 Stem          48 :      9 bp (total :  15772) coverage : 424.20
 Stem          49 :   1258 bp (total :  17030) coverage :  30.89
 Stem          50 :   1557 bp (total :  18587) coverage : 1162.54
 Stem          51 :     21 bp (total :  18608) coverage :  18.36
 Stem          52 :     91 bp (total :  18699) coverage :  25.25
 Stem          53 :   1090 bp (total :  19789) coverage : 550.36
 Stem          54 :     21 bp (total :  19810) coverage :  22.95
 Stem          55 :     21 bp (total :  19831) coverage : 211.18
 Stem          56 :     20 bp (total :  19851) coverage : 625.24
 Stem          57 :     33 bp (total :  19884) coverage :  83.18
 Stem          58 :     12 bp (total :  19896) coverage : 963.38
 Stem         -46 :     13 bp (total :  19909) coverage : 165.93
 Stem          59 :     16 bp (total :  19925) coverage : 112.88
 Stem          60 :      1 bp (total :  19926) coverage : 151.50
 Stem          61 :     91 bp (total :  20017) coverage :  38.42
 Stem          62 :      1 bp (total :  20018) coverage : 353.50
 Stem          63 :   1740 bp (total :  21758) coverage : 689.31
 Stem          64 :      5 bp (total :  21763) coverage : 589.17
 Stem          65 :     93 bp (total :  21856) coverage : 487.81
 Stem          66 :     14 bp (total :  21870) coverage : 107.73
 Stem          67 :     11 bp (total :  21881) coverage : 185.17
 Stem          68 :     90 bp (total :  21971) coverage : 546.07
 Stem          69 :     91 bp (total :  22062) coverage :  52.70
 Stem          70 :    101 bp (total :  22163) coverage :  75.25
 Stem          71 :    303 bp (total :  22466) coverage : 896.04
 Stem          72 :     12 bp (total :  22478) coverage : 116.54
 Stem          73 :     40 bp (total :  22518) coverage : 906.54
 Stem          -8 :     12 bp (total :  22530) coverage :   0.00
 Stem          74 :     51 bp (total :  22581) coverage : 275.81
 Stem          75 :     20 bp (total :  22601) coverage : 105.81
 Stem          76 :     86 bp (total :  22687) coverage :  32.51
 Stem          77 :    752 bp (total :  23439) coverage : 648.79
 Stem          78 :   1879 bp (total :  25318) coverage : 580.05
 Stem          79 :      8 bp (total :  25326) coverage : 404.00
 Stem          80 :   1170 bp (total :  26496) coverage : 719.68
 Stem          81 :     20 bp (total :  26516) coverage :  76.95
 Stem          82 :     11 bp (total :  26527) coverage :  42.08
 Stem          83 :      6 bp (total :  26533) coverage : 144.29
 Stem          84 :      6 bp (total :  26539) coverage : 591.57
 Stem          85 :     12 bp (total :  26551) coverage :  15.54
 Stem          86 :     19 bp (total :  26570) coverage : 323.20
 Stem          87 :     67 bp (total :  26637) coverage : 851.07
 Stem          88 :     91 bp (total :  26728) coverage :  27.45
 Stem          89 :     28 bp (total :  26756) coverage :  66.17
 Stem          90 :      1 bp (total :  26757) coverage : 353.50
 Stem         -73 :     40 bp (total :  26797) coverage : 906.54
 Stem          91 :     29 bp (total :  26826) coverage : 117.83
 Stem          92 :     91 bp (total :  26917) coverage :  26.35
 Stem          93 :   1481 bp (total :  28398) coverage : 556.39
 Stem          94 :      5 bp (total :  28403) coverage : 353.50
 Stem         -25 :     13 bp (total :  28416) coverage :  43.29
 Stem          95 :    257 bp (total :  28673) coverage : 647.50
 Stem         -42 :      8 bp (total :  28681) coverage :   0.00
 Stem          96 :     12 bp (total :  28693) coverage :  23.31
 Stem          97 :     90 bp (total :  28783) coverage :  33.30
 Stem         -52 :     91 bp (total :  28874) coverage :  25.25
 Stem          98 :      1 bp (total :  28875) coverage : 404.00
 Stem          -7 :     39 bp (total :  28914) coverage :  20.20
 Stem          99 :      2 bp (total :  28916) coverage : 202.00
 Stem         100 :     26 bp (total :  28942) coverage :  48.63
 Stem         101 :     72 bp (total :  29014) coverage : 893.78
 Stem         102 :   2986 bp (total :  32000) coverage : 612.39
 Stem         -28 :    102 bp (total :  32102) coverage : 1092.37
 Stem         103 :     89 bp (total :  32191) coverage :  35.91
 Stem         104 :      1 bp (total :  32192) coverage : 303.00
 Stem         105 :    189 bp (total :  32381) coverage : 726.67
 Stem         106 :     20 bp (total :  32401) coverage : 168.33
 Stem         107 :     84 bp (total :  32485) coverage : 508.56
 Stem         108 :    199 bp (total :  32684) coverage : 466.62
 Stem          -2 :   1119 bp (total :  33803) coverage :  31.47
 Stem         -56 :     20 bp (total :  33823) coverage : 625.24
 Stem         109 :    188 bp (total :  34011) coverage : 789.30
 Stem         110 :     36 bp (total :  34047) coverage :  27.30
 Stem         111 :     18 bp (total :  34065) coverage : 122.26
 Stem         112 :    517 bp (total :  34582) coverage : 844.85
 Stem         113 :   1436 bp (total :  36018) coverage : 572.26
 Stem         114 :     15 bp (total :  36033) coverage :  88.38
 Stem         115 :    240 bp (total :  36273) coverage : 945.04
 Stem         116 :     23 bp (total :  36296) coverage :  42.08
 Stem         117 :     83 bp (total :  36379) coverage :  50.50
 Stem         118 :      2 bp (total :  36381) coverage : 505.00
 Stem         119 :    324 bp (total :  36705) coverage : 1034.24
 Stem         -65 :     93 bp (total :  36798) coverage : 487.81
 Stem         120 :    218 bp (total :  37016) coverage : 728.21
 Stem         121 :     25 bp (total :  37041) coverage :  38.85
 Stem         122 :     21 bp (total :  37062) coverage :  50.50
 Stem         123 :    627 bp (total :  37689) coverage : 1244.17
 Stem         124 :     33 bp (total :  37722) coverage : 130.71
 Stem         125 :   2631 bp (total :  40353) coverage : 653.31
 Stem        -122 :     21 bp (total :  40374) coverage :  50.50
 Stem         126 :   2818 bp (total :  43192) coverage : 532.05
 Stem         127 :     22 bp (total :  43214) coverage :  74.65
 Stem         128 :     76 bp (total :  43290) coverage :  31.48
 Stem         129 :     76 bp (total :  43366) coverage : 502.38
 Stem         130 :     13 bp (total :  43379) coverage :   0.00
 Stem         131 :     13 bp (total :  43392) coverage :   0.00
 Stem         132 :     75 bp (total :  43467) coverage : 462.47
 Stem         133 :     75 bp (total :  43542) coverage : 127.58
 Stem         134 :     20 bp (total :  43562) coverage :   0.00
 Stem         -54 :     21 bp (total :  43583) coverage :  22.95
 Stem         135 :    232 bp (total :  43815) coverage : 965.79
 Stem         136 :    777 bp (total :  44592) coverage : 545.11
 Stem         137 :     36 bp (total :  44628) coverage :  40.95
 Stem         138 :   2471 bp (total :  47099) coverage : 564.73
 Stem         -43 :      8 bp (total :  47107) coverage : 123.44
 Stem         -79 :      8 bp (total :  47115) coverage : 404.00
 Stem         139 :   4312 bp (total :  51427) coverage : 558.02
 Stem        -133 :     75 bp (total :  51502) coverage : 127.58
 Stem         140 :     26 bp (total :  51528) coverage :  86.04
 Stem         141 :   1673 bp (total :  53201) coverage : 596.11
 Stem         142 :     84 bp (total :  53285) coverage :  61.79
 Stem         143 :    396 bp (total :  53681) coverage : 934.44
 Stem         -55 :     21 bp (total :  53702) coverage : 211.18
 Stem         144 :     22 bp (total :  53724) coverage :  21.96
 Stem         145 :     31 bp (total :  53755) coverage : 123.09
 Stem         146 :   2647 bp (total :  56402) coverage : 551.08
 Stem         147 :     28 bp (total :  56430) coverage :  24.38
 Stem         148 :    224 bp (total :  56654) coverage :  35.91
 Stem         149 :     12 bp (total :  56666) coverage :  38.85
 Stem         150 :     97 bp (total :  56763) coverage :  39.16
 Stem         151 :    102 bp (total :  56865) coverage :  92.17
 Stem         152 :    102 bp (total :  56967) coverage : 910.96
 Stem         153 :     12 bp (total :  56979) coverage :  93.23
 Stem         154 :     30 bp (total :  57009) coverage : 387.71
 Stem        -117 :     83 bp (total :  57092) coverage :  50.50
 Stem         155 :     83 bp (total :  57175) coverage : 520.63
 Stem         156 :     18 bp (total :  57193) coverage : 574.11
 Stem         157 :     19 bp (total :  57212) coverage : 131.30
 Stem         158 :    114 bp (total :  57326) coverage :  25.47
 Stem         159 :   1039 bp (total :  58365) coverage :  28.94
 Stem         160 :     18 bp (total :  58383) coverage :  58.47
 Stem        -135 :    232 bp (total :  58615) coverage : 965.79
 Stem         161 :   3912 bp (total :  62527) coverage : 608.53
 Stem         162 :    135 bp (total :  62662) coverage : 565.15
 Stem         163 :     25 bp (total :  62687) coverage :  23.31
 Stem         164 :     13 bp (total :  62700) coverage :  14.43
 Stem         165 :     13 bp (total :  62713) coverage :  50.50
 Stem         166 :     16 bp (total :  62729) coverage :   5.94
 Stem         -96 :     12 bp (total :  62741) coverage :  23.31
 Stem         167 :      4 bp (total :  62745) coverage : 303.00
 Stem         168 :    102 bp (total :  62847) coverage : 465.78
 Stem         169 :     28 bp (total :  62875) coverage : 132.34
 Stem         170 :      9 bp (total :  62884) coverage : 707.00
 Stem         171 :     78 bp (total :  62962) coverage :  39.63
 Stem         172 :     91 bp (total :  63053) coverage :  40.62
 Stem         173 :     68 bp (total :  63121) coverage : 404.00
 Stem         174 :     25 bp (total :  63146) coverage :  73.81
 Stem         -76 :     86 bp (total :  63232) coverage :  32.51
 Stem         175 :     82 bp (total :  63314) coverage :  48.67
 Stem        -155 :     83 bp (total :  63397) coverage : 520.63
 Stem         176 :    401 bp (total :  63798) coverage : 1015.78
 Stem         177 :     27 bp (total :  63825) coverage : 133.46
 Stem         178 :     90 bp (total :  63915) coverage :  16.65
 Stem         179 :    852 bp (total :  64767) coverage : 1030.72
 Stem         180 :     15 bp (total :  64782) coverage :  63.12
 Stem         181 :     70 bp (total :  64852) coverage : 303.00
 Stem         182 :     23 bp (total :  64875) coverage :  67.33
 Stem         183 :     14 bp (total :  64889) coverage :  40.40
 Stem         -97 :     90 bp (total :  64979) coverage :  33.30
 Stem         184 :     91 bp (total :  65070) coverage : 473.16
 Stem         185 :     92 bp (total :  65162) coverage :  33.67
 Stem         186 :     91 bp (total :  65253) coverage : 577.46
 Stem         187 :    379 bp (total :  65632) coverage : 590.32
 Stem         188 :   2992 bp (total :  68624) coverage : 671.90
 Stem         189 :      6 bp (total :  68630) coverage : 129.86
 Stem        -139 :   4312 bp (total :  72942) coverage : 558.02
 Stem         190 :    234 bp (total :  73176) coverage : 706.14
 Stem          -9 :   1750 bp (total :  74926) coverage : 604.10
 Stem         191 :   1353 bp (total :  76279) coverage : 472.70
 Stem         192 :      4 bp (total :  76283) coverage : 222.20
 Stem         193 :     83 bp (total :  76366) coverage :  98.60
 Stem         194 :     90 bp (total :  76456) coverage :  45.51
 Stem         195 :      8 bp (total :  76464) coverage : 224.44
 Stem         196 :     15 bp (total :  76479) coverage :  69.44
 Stem         197 :     16 bp (total :  76495) coverage : 932.76
 Stem         198 :    107 bp (total :  76602) coverage : 665.85
 Stem         199 :     27 bp (total :  76629) coverage :  82.96
 Stem         200 :   2040 bp (total :  78669) coverage : 1145.64
 Stem         201 :    665 bp (total :  79334) coverage : 732.02
 Stem         202 :     99 bp (total :  79433) coverage :  38.38
 Stem         -58 :     12 bp (total :  79445) coverage : 963.38
 Stem        -192 :      4 bp (total :  79449) coverage : 222.20
 Stem         203 :   1014 bp (total :  80463) coverage : 1168.02
 Stem        -150 :     97 bp (total :  80560) coverage :  39.16
 Stem         204 :     67 bp (total :  80627) coverage :  29.71
 Stem         205 :     70 bp (total :  80697) coverage : 539.14
 Stem         206 :     88 bp (total :  80785) coverage :  43.12
 Stem         -95 :    257 bp (total :  81042) coverage : 647.50
 Stem         207 :      7 bp (total :  81049) coverage : 151.50
 Stem         208 :     97 bp (total :  81146) coverage :  29.89
 Stem         209 :     60 bp (total :  81206) coverage :  23.18
 Stem         210 :     91 bp (total :  81297) coverage : 610.39
 Stem         -68 :     90 bp (total :  81387) coverage : 546.07
 Stem         -69 :     91 bp (total :  81478) coverage :  52.70
 Stem         211 :    100 bp (total :  81578) coverage :  35.00
 Stem         212 :     92 bp (total :  81670) coverage : 1095.80
 Stem         213 :     93 bp (total :  81763) coverage :  41.90
 Stem         214 :    226 bp (total :  81989) coverage : 755.05
 Stem         -13 :     27 bp (total :  82016) coverage : 216.43
 Stem         -80 :   1170 bp (total :  83186) coverage : 719.68
 Stem         215 :     24 bp (total :  83210) coverage :   4.04
 Stem         216 :     15 bp (total :  83225) coverage :  12.62
 Stem        -123 :    627 bp (total :  83852) coverage : 1244.17
 Stem         217 :     90 bp (total :  83942) coverage :  27.75
 Stem         218 :   7045 bp (total :  90987) coverage : 554.35
 Stem         -75 :     20 bp (total :  91007) coverage : 105.81
 Stem         219 :     74 bp (total :  91081) coverage : 802.61
 Stem         220 :     76 bp (total :  91157) coverage :  48.53
 Stem         221 :     24 bp (total :  91181) coverage : 113.12
 Stem         -57 :     33 bp (total :  91214) coverage :  83.18
 Stem         -16 :     35 bp (total :  91249) coverage : 1388.75
 Stem        -148 :    224 bp (total :  91473) coverage :  35.91
 Stem         222 :   2289 bp (total :  93762) coverage : 605.65
 Stem         223 :     92 bp (total :  93854) coverage :  35.84
 Stem         224 :     91 bp (total :  93945) coverage : 686.14
 Stem         225 :     88 bp (total :  94033) coverage : 1089.44
 Stem         226 :     23 bp (total :  94056) coverage :  71.54
 Stem        -224 :     91 bp (total :  94147) coverage : 686.14
 Stem        -223 :     92 bp (total :  94239) coverage :  35.84
 Stem         -62 :      1 bp (total :  94240) coverage : 353.50
 Stem         227 :     27 bp (total :  94267) coverage :  46.89
 Stem         228 :      1 bp (total :  94268) coverage : 606.00
 Stem         229 :     91 bp (total :  94359) coverage : 178.95
 Stem         -82 :     11 bp (total :  94370) coverage :  42.08
 Stem        -214 :    226 bp (total :  94596) coverage : 755.05
 Stem        -149 :     12 bp (total :  94608) coverage :  38.85
 Stem         -61 :     91 bp (total :  94699) coverage :  38.42
 Stem         230 :     38 bp (total :  94737) coverage : 567.15
 Stem         231 :     32 bp (total :  94769) coverage :  91.82
 Stem         232 :    245 bp (total :  95014) coverage : 1204.61
 Stem         233 :     35 bp (total :  95049) coverage :  89.78
 Stem         234 :     23 bp (total :  95072) coverage :  88.38
 Stem         235 :     73 bp (total :  95145) coverage : 768.42
 Stem        -154 :     30 bp (total :  95175) coverage : 387.71
 Stem         236 :    202 bp (total :  95377) coverage : 529.88
 Stem        -187 :    379 bp (total :  95756) coverage : 590.32
 Stem         237 :     35 bp (total :  95791) coverage : 471.33
 Stem         238 :     24 bp (total :  95815) coverage :  72.72
 Stem         239 :     17 bp (total :  95832) coverage : 527.44
 Stem         240 :     16 bp (total :  95848) coverage :  65.35
 Stem         -48 :      9 bp (total :  95857) coverage : 424.20
 Stem         241 :     17 bp (total :  95874) coverage :  84.17
 Stem        -118 :      2 bp (total :  95876) coverage : 505.00
 Stem         242 :     25 bp (total :  95901) coverage : 101.00
 Stem         243 :     74 bp (total :  95975) coverage :  29.63
 Stem        -151 :    102 bp (total :  96077) coverage :  92.17
 Stem        -152 :    102 bp (total :  96179) coverage : 910.96
 Stem        -230 :     38 bp (total :  96217) coverage : 567.15
 Stem        -169 :     28 bp (total :  96245) coverage : 132.34
 Stem         244 :    170 bp (total :  96415) coverage : 907.82
 Stem         245 :     17 bp (total :  96432) coverage : 129.06
 Stem         246 :      1 bp (total :  96433) coverage : 404.00
 Stem        -194 :     90 bp (total :  96523) coverage :  45.51
 Stem         247 :     19 bp (total :  96542) coverage : 792.85
 Stem         248 :     33 bp (total :  96575) coverage :  71.29
 Stem         249 :     11 bp (total :  96586) coverage :  58.92
 Stem        -193 :     83 bp (total :  96669) coverage :  98.60
 Stem        -124 :     33 bp (total :  96702) coverage : 130.71
 Stem         250 :     74 bp (total :  96776) coverage :  41.75
 Stem         251 :      2 bp (total :  96778) coverage : 370.33
 Stem        -203 :   1014 bp (total :  97792) coverage : 1168.02
 Stem         252 :     29 bp (total :  97821) coverage :  13.47
 Stem         253 :     94 bp (total :  97915) coverage :  36.15
 Stem        -119 :    324 bp (total :  98239) coverage : 1034.24
 Stem         254 :   2448 bp (total : 100687) coverage : 602.54
 Stem        -105 :    189 bp (total : 100876) coverage : 726.67
 Stem         255 :     18 bp (total : 100894) coverage :  74.42
 Stem         256 :    936 bp (total : 101830) coverage : 749.15
 Stem         -98 :      1 bp (total : 101831) coverage : 404.00
 Stem         -60 :      1 bp (total : 101832) coverage : 151.50
 Stem        -114 :     15 bp (total : 101847) coverage :  88.38
 Stem        -219 :     74 bp (total : 101921) coverage : 802.61
 Stem         257 :     98 bp (total : 102019) coverage : 628.44
 Stem         258 :    465 bp (total : 102484) coverage :  27.74
 Stem        -208 :     97 bp (total : 102581) coverage :  29.89
 Stem         259 :     22 bp (total : 102603) coverage : 114.17
 Stem         260 :     22 bp (total : 102625) coverage :   0.00
 Stem        -144 :     22 bp (total : 102647) coverage :  21.96
 Stem         261 :   2359 bp (total : 105006) coverage : 571.08
 Stem         -78 :   1879 bp (total : 106885) coverage : 580.05
 Stem         262 :   1640 bp (total : 108525) coverage : 646.50
 Stem        -245 :     17 bp (total : 108542) coverage : 129.06
 Stem         263 :     18 bp (total : 108560) coverage :  85.05
 Stem         -45 :     19 bp (total : 108579) coverage : 409.05
 Stem        -120 :    218 bp (total : 108797) coverage : 728.21
 Stem        -255 :     18 bp (total : 108815) coverage :  74.42
 Stem         264 :     32 bp (total : 108847) coverage : 664.15
 Stem         265 :   5963 bp (total : 114810) coverage : 557.80
 Stem        -202 :     99 bp (total : 114909) coverage :  38.38
 Stem        -215 :     24 bp (total : 114933) coverage :   4.04
 Stem        -107 :     84 bp (total : 115017) coverage : 508.56
 Stem         266 :   1296 bp (total : 116313) coverage : 1153.99
 Stem         267 :    102 bp (total : 116415) coverage :  77.47
 Stem         268 :    102 bp (total : 116517) coverage : 983.52
 Stem         269 :    280 bp (total : 116797) coverage : 597.73
 Stem         270 :     23 bp (total : 116820) coverage : 130.46
 Stem         271 :     71 bp (total : 116891) coverage : 1233.04
 Stem         -77 :    752 bp (total : 117643) coverage : 648.79
 Stem        -132 :     75 bp (total : 117718) coverage : 462.47
 Stem         272 :     12 bp (total : 117730) coverage :  69.92
 Stem         273 :     33 bp (total : 117763) coverage :  68.32
 Stem          -5 :     20 bp (total : 117783) coverage :   0.00
 Stem         274 :     19 bp (total : 117802) coverage :   0.00
 Stem         275 :     31 bp (total : 117833) coverage : 691.22
 Stem        -228 :      1 bp (total : 117834) coverage : 606.00
 Stem         276 :     77 bp (total : 117911) coverage :  25.90
 Stem         277 :    101 bp (total : 118012) coverage :  36.64
 Stem         278 :      4 bp (total : 118016) coverage : 787.80
 Stem         279 :   1183 bp (total : 119199) coverage : 691.73
 Stem         280 :      2 bp (total : 119201) coverage : 101.00
 Stem         281 :     15 bp (total : 119216) coverage :  69.44
 Stem         282 :     11 bp (total : 119227) coverage :  42.08
 Stem        -129 :     76 bp (total : 119303) coverage : 502.38
 Stem         -38 :     76 bp (total : 119379) coverage : 472.21
 Stem        -249 :     11 bp (total : 119390) coverage :  58.92
 Stem         283 :    878 bp (total : 120268) coverage : 610.02
 Stem        -243 :     74 bp (total : 120342) coverage :  29.63
 Stem         284 :     21 bp (total : 120363) coverage : 123.95
 Stem         -83 :      6 bp (total : 120369) coverage : 144.29
 Stem         285 :     16 bp (total : 120385) coverage :  95.06
 Stem        -239 :     17 bp (total : 120402) coverage : 527.44
 Stem         -10 :      2 bp (total : 120404) coverage : 168.33
 Stem         286 :    647 bp (total : 121051) coverage : 538.98
 Stem         287 :     62 bp (total : 121113) coverage :  22.44
 Stem         -44 :     91 bp (total : 121204) coverage :  27.45
 Stem        -113 :   1436 bp (total : 122640) coverage : 572.26
 Stem         288 :     74 bp (total : 122714) coverage : 203.35
 Stem         289 :     73 bp (total : 122787) coverage :  17.74
 Stem         290 :    104 bp (total : 122891) coverage :  44.25
 Stem         291 :    327 bp (total : 123218) coverage : 1131.02
 Stem         292 :     90 bp (total : 123308) coverage :  42.18
 Stem        -248 :     33 bp (total : 123341) coverage :  71.29
 Stem         293 :     13 bp (total : 123354) coverage :   7.21
 Stem         294 :   1686 bp (total : 125040) coverage : 566.91
 Stem         295 :   1369 bp (total : 126409) coverage : 594.57
 Stem         296 :      1 bp (total : 126410) coverage : 656.50
 Stem         297 :     38 bp (total : 126448) coverage :  77.69
 Stem        -264 :     32 bp (total : 126480) coverage : 664.15
 Stem         298 :     14 bp (total : 126494) coverage : 134.67
 Stem         299 :     25 bp (total : 126519) coverage :  11.65
 Stem        -121 :     25 bp (total : 126544) coverage :  38.85
 Stem         300 :     90 bp (total : 126634) coverage :  32.19
 Stem         301 :    231 bp (total : 126865) coverage : 1318.66
 Stem         302 :     61 bp (total : 126926) coverage : 568.53
 Stem         -18 :     39 bp (total : 126965) coverage :  83.32
 Stem         -30 :     27 bp (total : 126992) coverage : 292.18
 Stem         303 :   1213 bp (total : 128205) coverage : 659.66
 Stem         304 :     69 bp (total : 128274) coverage :  54.83
 Stem         305 :    102 bp (total : 128376) coverage : 289.27
 Stem        -256 :    936 bp (total : 129312) coverage : 749.15
 Stem         -94 :      5 bp (total : 129317) coverage : 353.50
 Stem        -299 :     25 bp (total : 129342) coverage :  11.65
 Stem         -32 :     19 bp (total : 129361) coverage :   0.00
 Stem         306 :     11 bp (total : 129372) coverage :  25.25
 Stem         307 :      1 bp (total : 129373) coverage : 101.00
 Stem        -180 :     15 bp (total : 129388) coverage :  63.12
 Stem        -250 :     74 bp (total : 129462) coverage :  41.75
 Stem         308 :    126 bp (total : 129588) coverage : 1031.47
 Stem         309 :    901 bp (total : 130489) coverage : 571.29
 Stem        -160 :     18 bp (total : 130507) coverage :  58.47
 Stem         310 :    159 bp (total : 130666) coverage :  35.35
 Stem         311 :     13 bp (total : 130679) coverage : 101.00
 Stem         312 :    513 bp (total : 131192) coverage : 843.37
 Stem         -67 :     11 bp (total : 131203) coverage : 185.17
 Stem        -115 :    240 bp (total : 131443) coverage : 945.04
 Stem         313 :     58 bp (total : 131501) coverage : 616.27
 Stem         314 :     12 bp (total : 131513) coverage :  93.23
 Stem        -201 :    665 bp (total : 132178) coverage : 732.02
 Stem         315 :     77 bp (total : 132255) coverage :  58.27
 Stem        -106 :     20 bp (total : 132275) coverage : 168.33
 Stem         316 :     29 bp (total : 132304) coverage :  33.67
 Stem        -306 :     11 bp (total : 132315) coverage :  25.25
 Stem         317 :     91 bp (total : 132406) coverage :  43.91
 Stem         318 :     64 bp (total : 132470) coverage :  20.20
 Stem         319 :     18 bp (total : 132488) coverage :  95.68
 Stem         -26 :     10 bp (total : 132498) coverage : 707.00
 Stem        -210 :     91 bp (total : 132589) coverage : 610.39
 Stem        -100 :     26 bp (total : 132615) coverage :  48.63
 Stem         -11 :   1568 bp (total : 134183) coverage : 1055.90
 Stem        -259 :     22 bp (total : 134205) coverage : 114.17
 Stem         320 :    280 bp (total : 134485) coverage : 719.22
 Stem         321 :     68 bp (total : 134553) coverage :  36.59
 Stem         322 :     12 bp (total : 134565) coverage :   7.77
 Stem         323 :     14 bp (total : 134579) coverage : 269.33
 Stem        -310 :    159 bp (total : 134738) coverage :  35.35
 Stem         324 :     20 bp (total : 134758) coverage :  76.95
 Stem         325 :     88 bp (total : 134846) coverage :  34.04
 Stem        -188 :   2992 bp (total : 137838) coverage : 671.90
 Stem        -279 :   1183 bp (total : 139021) coverage : 691.73
 Stem         326 :    156 bp (total : 139177) coverage : 517.22
 Stem         327 :     27 bp (total : 139204) coverage :  21.64
 Stem         328 :     14 bp (total : 139218) coverage :  67.33
 Stem         329 :     38 bp (total : 139256) coverage : 145.03
 Stem         330 :     26 bp (total : 139282) coverage :  26.19
 Stem        -109 :    188 bp (total : 139470) coverage : 789.30
 Stem        -158 :    114 bp (total : 139584) coverage :  25.47
 Stem         331 :   1868 bp (total : 141452) coverage :  31.78
 Stem        -325 :     88 bp (total : 141540) coverage :  34.04
 Stem         332 :    374 bp (total : 141914) coverage : 398.07
 Stem        -179 :    852 bp (total : 142766) coverage : 1030.72
 Stem        -182 :     23 bp (total : 142789) coverage :  67.33
 Stem        -265 :   5963 bp (total : 148752) coverage : 557.80
 Stem         -24 :     87 bp (total : 148839) coverage :  25.25
 Stem         -36 :    696 bp (total : 149535) coverage :  24.20
 Stem         333 :   2610 bp (total : 152145) coverage : 467.90
 Stem        -116 :     23 bp (total : 152168) coverage :  42.08
 Stem         334 :     15 bp (total : 152183) coverage : 643.88
 Stem        -301 :    231 bp (total : 152414) coverage : 1318.66
 Stem         335 :     70 bp (total : 152484) coverage : 1330.07
 Stem         336 :   1997 bp (total : 154481) coverage : 601.35
 Stem         -70 :    101 bp (total : 154582) coverage :  75.25
 Stem        -198 :    107 bp (total : 154689) coverage : 665.85
 Stem        -314 :     12 bp (total : 154701) coverage :  93.23
 Stem         337 :    512 bp (total : 155213) coverage : 838.91
 Stem         338 :     14 bp (total : 155227) coverage :  40.40
 Stem         -71 :    303 bp (total : 155530) coverage : 896.04
 Stem         339 :     14 bp (total : 155544) coverage : 262.60
 Stem        -257 :     98 bp (total : 155642) coverage : 628.44
 Stem        -285 :     16 bp (total : 155658) coverage :  95.06
 Stem        -177 :     27 bp (total : 155685) coverage : 133.46
 Stem         340 :    102 bp (total : 155787) coverage :  62.76
 Stem         341 :    102 bp (total : 155889) coverage : 1118.84
 Stem        -103 :     89 bp (total : 155978) coverage :  35.91
 Stem        -190 :    234 bp (total : 156212) coverage : 706.14
 Stem        -242 :     25 bp (total : 156237) coverage : 101.00
 Stem         342 :    101 bp (total : 156338) coverage :  61.39
 Stem        -319 :     18 bp (total : 156356) coverage :  95.68
 Stem         343 :     17 bp (total : 156373) coverage : 555.50
 Stem         344 :    262 bp (total : 156635) coverage : 216.98
 Stem         345 :     20 bp (total : 156655) coverage :   0.00
 Stem        -292 :     90 bp (total : 156745) coverage :  42.18
 Stem         346 :     91 bp (total : 156836) coverage : 454.50
 Stem        -172 :     91 bp (total : 156927) coverage :  40.62
 Stem         347 :      1 bp (total : 156928) coverage : 303.00
 Stem         348 :   1228 bp (total : 158156) coverage : 604.52
 Stem        -153 :     12 bp (total : 158168) coverage :  93.23
 Stem         349 :     85 bp (total : 158253) coverage :  37.58
 Stem         350 :     28 bp (total : 158281) coverage :  69.66
 Stem        -303 :   1213 bp (total : 159494) coverage : 659.66
 Stem        -317 :     91 bp (total : 159585) coverage :  43.91
 Stem        -174 :     25 bp (total : 159610) coverage :  73.81
 Stem        -104 :      1 bp (total : 159611) coverage : 303.00
 Stem        -200 :   2040 bp (total : 161651) coverage : 1145.64
 Stem        -284 :     21 bp (total : 161672) coverage : 123.95
 Stem        -195 :      8 bp (total : 161680) coverage : 224.44
 Stem        -305 :    102 bp (total : 161782) coverage : 289.27
 Stem         351 :     21 bp (total : 161803) coverage :  87.23
 Stem         352 :     15 bp (total : 161818) coverage :  50.50
 Stem        -263 :     18 bp (total : 161836) coverage :  85.05
 Stem         353 :     13 bp (total : 161849) coverage :  57.71
 Stem         -29 :   2289 bp (total : 164138) coverage : 619.01
 Stem        -205 :     70 bp (total : 164208) coverage : 539.14
 Stem         354 :    213 bp (total : 164421) coverage :  34.93
 Stem        -332 :    374 bp (total : 164795) coverage : 398.07
 Stem        -171 :     78 bp (total : 164873) coverage :  39.63
 Stem        -156 :     18 bp (total : 164891) coverage : 574.11
 Stem         355 :      4 bp (total : 164895) coverage : 909.00
 Stem         356 :     23 bp (total : 164918) coverage :  75.75
 Stem        -297 :     38 bp (total : 164956) coverage :  77.69
 Stem        -101 :     72 bp (total : 165028) coverage : 893.78
 Stem        -339 :     14 bp (total : 165042) coverage : 262.60
 Stem         357 :     45 bp (total : 165087) coverage : 814.59
 Stem         -41 :     88 bp (total : 165175) coverage :  41.99
 Stem         358 :      1 bp (total : 165176) coverage : 252.50
 Stem         359 :     91 bp (total : 165267) coverage :  40.62
 Stem         360 :     90 bp (total : 165357) coverage : 543.85
 Stem        -302 :     61 bp (total : 165418) coverage : 568.53
 Stem        -307 :      1 bp (total : 165419) coverage : 101.00
 Stem        -253 :     94 bp (total : 165513) coverage :  36.15
 Stem        -260 :     22 bp (total : 165535) coverage :   0.00
 Stem         -51 :     21 bp (total : 165556) coverage :  18.36
 Stem        -108 :    199 bp (total : 165755) coverage : 466.62
 Stem         361 :     13 bp (total : 165768) coverage :   0.00
 Stem         362 :     89 bp (total : 165857) coverage : 350.13
 Stem         363 :     89 bp (total : 165946) coverage :  68.46
 Stem        -313 :     58 bp (total : 166004) coverage : 616.27
 Stem        -356 :     23 bp (total : 166027) coverage :  75.75
 Stem        -345 :     20 bp (total : 166047) coverage :   0.00
 Stem         364 :     21 bp (total : 166068) coverage :   4.59
 Stem         365 :     15 bp (total : 166083) coverage :  69.44
 Stem         366 :     11 bp (total : 166094) coverage :  92.58
 Stem        -236 :    202 bp (total : 166296) coverage : 529.88
 Stem        -218 :   7045 bp (total : 173341) coverage : 554.35
 Stem         367 :     12 bp (total : 173353) coverage :  54.38
 Stem        -186 :     91 bp (total : 173444) coverage : 577.46
 Stem        -185 :     92 bp (total : 173536) coverage :  33.67
 Stem        -365 :     15 bp (total : 173551) coverage :  69.44
 Stem         368 :     12 bp (total : 173563) coverage : 124.31
 Stem        -355 :      4 bp (total : 173567) coverage : 909.00
 Stem        -315 :     77 bp (total : 173644) coverage :  58.27
 Stem        -350 :     28 bp (total : 173672) coverage :  69.66
 Stem         369 :   1210 bp (total : 174882) coverage : 482.06
 Stem         370 :     20 bp (total : 174902) coverage :  81.76
 Stem         371 :     11 bp (total : 174913) coverage : 126.25
 Stem         372 :    373 bp (total : 175286) coverage : 1088.86
 Stem         373 :     74 bp (total : 175360) coverage :  35.01
 Stem         -99 :      2 bp (total : 175362) coverage : 202.00
 Stem         374 :     29 bp (total : 175391) coverage :  13.47
 Stem        -348 :   1228 bp (total : 176619) coverage : 604.52
 Stem        -166 :     16 bp (total : 176635) coverage :   5.94
 Stem         375 :    158 bp (total : 176793) coverage : 1076.70
 Stem         -20 :     17 bp (total : 176810) coverage : 162.72
 Stem         -12 :     27 bp (total : 176837) coverage : 331.86
 Stem        -207 :      7 bp (total : 176844) coverage : 151.50
 Stem        -281 :     15 bp (total : 176859) coverage :  69.44
 Stem        -375 :    158 bp (total : 177017) coverage : 1076.70
 Stem        -145 :     31 bp (total : 177048) coverage : 123.09
 Stem         376 :    125 bp (total : 177173) coverage : 1115.01
 Stem         377 :     20 bp (total : 177193) coverage :   0.00
 Stem        -364 :     21 bp (total : 177214) coverage :   4.59
 Stem        -308 :    126 bp (total : 177340) coverage : 1031.47
 Stem         -84 :      6 bp (total : 177346) coverage : 591.57
 Stem         378 :      1 bp (total : 177347) coverage :  50.50
 Stem         379 :     21 bp (total : 177368) coverage : 128.55
 Stem         380 :     36 bp (total : 177404) coverage :  19.11
 Stem        -112 :    517 bp (total : 177921) coverage : 844.85
 Stem        -378 :      1 bp (total : 177922) coverage :  50.50
 Stem         381 :     88 bp (total : 178010) coverage :  23.83
 Stem         382 :    816 bp (total : 178826) coverage : 608.84
 Stem         -74 :     51 bp (total : 178877) coverage : 275.81
 Stem         383 :     16 bp (total : 178893) coverage : 118.82
 Stem         -35 :    351 bp (total : 179244) coverage : 645.88
 Stem        -206 :     88 bp (total : 179332) coverage :  43.12
 Stem        -362 :     89 bp (total : 179421) coverage : 350.13
 Stem        -229 :     91 bp (total : 179512) coverage : 178.95
 Stem        -342 :    101 bp (total : 179613) coverage :  61.39
 Stem         384 :      1 bp (total : 179614) coverage : 1313.00
 Stem         385 :     91 bp (total : 179705) coverage : 489.63
 Stem         386 :     92 bp (total : 179797) coverage :  36.92
 Stem        -269 :    280 bp (total : 180077) coverage : 597.73
 Stem        -173 :     68 bp (total : 180145) coverage : 404.00
 Stem         387 :    556 bp (total : 180701) coverage : 757.59
 Stem         388 :     17 bp (total : 180718) coverage :  67.33
 Stem        -196 :     15 bp (total : 180733) coverage :  69.44
 Stem         389 :    188 bp (total : 180921) coverage :  32.60
 Stem        -110 :     36 bp (total : 180957) coverage :  27.30
 Stem         390 :     35 bp (total : 180992) coverage :  33.67
 Stem         -15 :   1574 bp (total : 182566) coverage : 604.72
 Stem        -286 :    647 bp (total : 183213) coverage : 538.98
 Stem        -341 :    102 bp (total : 183315) coverage : 1118.84
 Stem        -340 :    102 bp (total : 183417) coverage :  62.76
 Stem         391 :     11 bp (total : 183428) coverage :  58.92
 Stem         -27 :    107 bp (total : 183535) coverage :  54.24
 Stem         -19 :    279 bp (total : 183814) coverage : 778.42
 Stem         392 :   5221 bp (total : 189035) coverage : 543.74
 Stem        -143 :    396 bp (total : 189431) coverage : 934.44
 Stem        -213 :     93 bp (total : 189524) coverage :  41.90
 Stem        -212 :     92 bp (total : 189616) coverage : 1095.80
 Stem        -322 :     12 bp (total : 189628) coverage :   7.77
 Stem         393 :     12 bp (total : 189640) coverage :   7.77
 Stem        -380 :     36 bp (total : 189676) coverage :  19.11
 Stem        -141 :   1673 bp (total : 191349) coverage : 596.11
 Stem        -111 :     18 bp (total : 191367) coverage : 122.26
 Stem        -274 :     19 bp (total : 191386) coverage :   0.00
 Stem        -349 :     85 bp (total : 191471) coverage :  37.58
 Stem         394 :     96 bp (total : 191567) coverage :  59.35
 Stem         -17 :      2 bp (total : 191569) coverage : 437.67
 Stem         395 :      2 bp (total : 191571) coverage : 269.33
 Stem        -288 :     74 bp (total : 191645) coverage : 203.35
 Stem        -373 :     74 bp (total : 191719) coverage :  35.01
 Stem        -374 :     29 bp (total : 191748) coverage :  13.47
 Stem        -164 :     13 bp (total : 191761) coverage :  14.43
 Stem        -254 :   2448 bp (total : 194209) coverage : 602.54
 Stem        -125 :   2631 bp (total : 196840) coverage : 653.31
 Stem        -258 :    465 bp (total : 197305) coverage :  27.74
 Stem         396 :     39 bp (total : 197344) coverage :  42.92
 Stem        -333 :   2610 bp (total : 199954) coverage : 467.90
 Stem        -291 :    327 bp (total : 200281) coverage : 1131.02
 Stem        -354 :    213 bp (total : 200494) coverage :  34.93
 Stem        -126 :   2818 bp (total : 203312) coverage : 532.05
 Stem        -336 :   1997 bp (total : 205309) coverage : 601.35
 Stem        -246 :      1 bp (total : 205310) coverage : 404.00
 Stem        -235 :     73 bp (total : 205383) coverage : 768.42
 Stem         397 :     12 bp (total : 205395) coverage : 108.77
 Stem        -272 :     12 bp (total : 205407) coverage :  69.92
 Stem        -167 :      4 bp (total : 205411) coverage : 303.00
 Stem        -277 :    101 bp (total : 205512) coverage :  36.64
 Stem         398 :    271 bp (total : 205783) coverage : 801.32
 Stem         399 :     12 bp (total : 205795) coverage :  62.15
 Stem        -247 :     19 bp (total : 205814) coverage : 792.85
 Stem         -87 :     67 bp (total : 205881) coverage : 851.07
 Stem        -189 :      6 bp (total : 205887) coverage : 129.86
 Stem         400 :    408 bp (total : 206295) coverage : 511.67
 Stem         -59 :     16 bp (total : 206311) coverage : 112.88
 Stem        -270 :     23 bp (total : 206334) coverage : 130.46
 Stem        -199 :     27 bp (total : 206361) coverage :  82.96
 Stem          -1 :    251 bp (total : 206612) coverage : 458.51
 Stem        -379 :     21 bp (total : 206633) coverage : 128.55
 Stem         -91 :     29 bp (total : 206662) coverage : 117.83
 Stem        -136 :    777 bp (total : 207439) coverage : 545.11
 Stem        -234 :     23 bp (total : 207462) coverage :  88.38
 Stem        -335 :     70 bp (total : 207532) coverage : 1330.07
 Stem         401 :     20 bp (total : 207552) coverage :   4.81
 Stem        -293 :     13 bp (total : 207565) coverage :   7.21
 Stem        -238 :     24 bp (total : 207589) coverage :  72.72
 Stem        -371 :     11 bp (total : 207600) coverage : 126.25
 Stem         402 :     96 bp (total : 207696) coverage :  51.02
 Stem        -394 :     96 bp (total : 207792) coverage :  59.35
 Stem        -377 :     20 bp (total : 207812) coverage :   0.00
 Stem         403 :     19 bp (total : 207831) coverage :  75.75
 Stem        -278 :      4 bp (total : 207835) coverage : 787.80
 Stem        -276 :     77 bp (total : 207912) coverage :  25.90
 Stem         -22 :     76 bp (total : 207988) coverage :  20.99
 Stem        -368 :     12 bp (total : 208000) coverage : 124.31
 Stem        -161 :   3912 bp (total : 211912) coverage : 608.53
 Stem         404 :     22 bp (total : 211934) coverage :  43.91
 Stem         -40 :    100 bp (total : 212034) coverage :  48.00
 Stem         405 :    128 bp (total : 212162) coverage : 1197.12
 Stem         406 :     26 bp (total : 212188) coverage :  52.37
 Stem         407 :   2350 bp (total : 214538) coverage : 584.22
 Stem         408 :     28 bp (total : 214566) coverage : 303.00
 Stem         409 :     35 bp (total : 214601) coverage :  53.31
 Stem        -184 :     91 bp (total : 214692) coverage : 473.16
 Stem        -300 :     90 bp (total : 214782) coverage :  32.19
 Stem        -406 :     26 bp (total : 214808) coverage :  52.37
 Stem         410 :     23 bp (total : 214831) coverage : 887.96
 Stem         -85 :     12 bp (total : 214843) coverage :  15.54
 Stem        -282 :     11 bp (total : 214854) coverage :  42.08
 Stem         411 :     12 bp (total : 214866) coverage :  77.69
 Stem        -331 :   1868 bp (total : 216734) coverage :  31.78
 Stem        -389 :    188 bp (total : 216922) coverage :  32.60
 Stem        -400 :    408 bp (total : 217330) coverage : 511.67
 Stem         412 :     29 bp (total : 217359) coverage :  80.80
 Stem         413 :    839 bp (total : 218198) coverage : 1196.97
 Stem         414 :     39 bp (total : 218237) coverage :  55.55
 Stem        -401 :     20 bp (total : 218257) coverage :   4.81
 Stem         415 :     53 bp (total : 218310) coverage : 353.50
 Stem        -178 :     90 bp (total : 218400) coverage :  16.65
 Stem        -287 :     62 bp (total : 218462) coverage :  22.44
 Stem        -176 :    401 bp (total : 218863) coverage : 1015.78
 Stem        -165 :     13 bp (total : 218876) coverage :  50.50
 Stem        -330 :     26 bp (total : 218902) coverage :  26.19
 Stem        -361 :     13 bp (total : 218915) coverage :   0.00
 Stem        -217 :     90 bp (total : 219005) coverage :  27.75
 Stem        -346 :     91 bp (total : 219096) coverage : 454.50
 Stem        -130 :     13 bp (total : 219109) coverage :   0.00
 Stem         416 :    815 bp (total : 219924) coverage :  33.67
 Stem         417 :    580 bp (total : 220504) coverage : 1134.29
 Stem        -413 :    839 bp (total : 221343) coverage : 1196.97
 Stem         -49 :   1258 bp (total : 222601) coverage :  30.89
 Stem        -271 :     71 bp (total : 222672) coverage : 1233.04
 Stem         418 :     89 bp (total : 222761) coverage : 435.42
 Stem         419 :     90 bp (total : 222851) coverage :  47.73
 Stem        -231 :     32 bp (total : 222883) coverage :  91.82
 Stem        -387 :    556 bp (total : 223439) coverage : 757.59
 Stem        -283 :    878 bp (total : 224317) coverage : 610.02
 Stem        -267 :    102 bp (total : 224419) coverage :  77.47
 Stem        -268 :    102 bp (total : 224521) coverage : 983.52
 Stem        -385 :     91 bp (total : 224612) coverage : 489.63
 Stem        -386 :     92 bp (total : 224704) coverage :  36.92
 Stem         420 :     96 bp (total : 224800) coverage :  73.93
 Stem        -162 :    135 bp (total : 224935) coverage : 565.15
 Stem        -221 :     24 bp (total : 224959) coverage : 113.12
 Stem        -312 :    513 bp (total : 225472) coverage : 843.37
 Stem        -352 :     15 bp (total : 225487) coverage :  50.50
 Stem        -382 :    816 bp (total : 226303) coverage : 608.84
 Stem        -388 :     17 bp (total : 226320) coverage :  67.33
 Stem        -170 :      9 bp (total : 226329) coverage : 707.00
 Stem        -157 :     19 bp (total : 226348) coverage : 131.30
 Stem        -409 :     35 bp (total : 226383) coverage :  53.31
 Stem         -90 :      1 bp (total : 226384) coverage : 353.50
 Stem         421 :   1048 bp (total : 227432) coverage : 884.83
 Stem        -326 :    156 bp (total : 227588) coverage : 517.22
 Stem        -127 :     22 bp (total : 227610) coverage :  74.65
 Stem         -64 :      5 bp (total : 227615) coverage : 589.17
 Stem         -81 :     20 bp (total : 227635) coverage :  76.95
 Stem        -311 :     13 bp (total : 227648) coverage : 101.00
 Stem        -392 :   5221 bp (total : 232869) coverage : 543.74
 Stem        -262 :   1640 bp (total : 234509) coverage : 646.50
 Stem         422 :   1202 bp (total : 235711) coverage : 510.88
 Stem        -321 :     68 bp (total : 235779) coverage :  36.59
 Stem        -360 :     90 bp (total : 235869) coverage : 543.85
 Stem        -359 :     91 bp (total : 235960) coverage :  40.62
 Stem        -381 :     88 bp (total : 236048) coverage :  23.83
 Stem         -23 :     88 bp (total : 236136) coverage : 204.27
 Stem        -275 :     31 bp (total : 236167) coverage : 691.22
 Stem         423 :     13 bp (total : 236180) coverage :  28.86
 Stem        -220 :     76 bp (total : 236256) coverage :  48.53
 Stem        -147 :     28 bp (total : 236284) coverage :  24.38
 Stem          -4 :     98 bp (total : 236382) coverage :  47.95
 Stem        -168 :    102 bp (total : 236484) coverage : 465.78
 Stem         -63 :   1740 bp (total : 238224) coverage : 689.31
 Stem        -397 :     12 bp (total : 238236) coverage : 108.77
 Stem         -21 :    902 bp (total : 239138) coverage : 1140.75
 Stem        -391 :     11 bp (total : 239149) coverage :  58.92
 Stem         424 :      3 bp (total : 239152) coverage : 833.25
 Stem        -338 :     14 bp (total : 239166) coverage :  40.40
 Stem         425 :    102 bp (total : 239268) coverage : 390.27
 Stem        -137 :     36 bp (total : 239304) coverage :  40.95
 Stem         -66 :     14 bp (total : 239318) coverage : 107.73
 Stem        -273 :     33 bp (total : 239351) coverage :  68.32
 Stem        -384 :      1 bp (total : 239352) coverage : 1313.00
 Stem        -232 :    245 bp (total : 239597) coverage : 1204.61
 Stem        -138 :   2471 bp (total : 242068) coverage : 564.73
 Stem         426 :   2321 bp (total : 244389) coverage : 511.22
 Stem        -309 :    901 bp (total : 245290) coverage : 571.29
 Stem         -92 :     91 bp (total : 245381) coverage :  26.35
 Stem        -266 :   1296 bp (total : 246677) coverage : 1153.99
 Stem        -411 :     12 bp (total : 246689) coverage :  77.69
 Stem        -329 :     38 bp (total : 246727) coverage : 145.03
 Stem         -47 :     15 bp (total : 246742) coverage :  88.38
 Stem        -290 :    104 bp (total : 246846) coverage :  44.25
 Stem        -142 :     84 bp (total : 246930) coverage :  61.79
 Stem        -233 :     35 bp (total : 246965) coverage :  89.78
 Stem        -351 :     21 bp (total : 246986) coverage :  87.23
 Stem         -53 :   1090 bp (total : 248076) coverage : 550.36
 Stem        -421 :   1048 bp (total : 249124) coverage : 884.83
 Stem        -211 :    100 bp (total : 249224) coverage :  35.00
 Stem        -251 :      2 bp (total : 249226) coverage : 370.33
 Stem        -131 :     13 bp (total : 249239) coverage :   0.00
 Stem        -334 :     15 bp (total : 249254) coverage : 643.88
 Stem        -240 :     16 bp (total : 249270) coverage :  65.35
 Stem        -183 :     14 bp (total : 249284) coverage :  40.40
 Stem        -280 :      2 bp (total : 249286) coverage : 101.00
 Stem        -227 :     27 bp (total : 249313) coverage :  46.89
 Stem        -347 :      1 bp (total : 249314) coverage : 303.00
 Stem        -366 :     11 bp (total : 249325) coverage :  92.58
 Stem        -367 :     12 bp (total : 249337) coverage :  54.38
 Stem         427 :      1 bp (total : 249338) coverage : 656.50
 Stem         428 :      4 bp (total : 249342) coverage : 808.00
 Stem        -181 :     70 bp (total : 249412) coverage : 303.00
 Stem         429 :     90 bp (total : 249502) coverage :  46.62
 Stem        -252 :     29 bp (total : 249531) coverage :  13.47
 Stem        -296 :      1 bp (total : 249532) coverage : 656.50
 Stem         430 :     91 bp (total : 249623) coverage :  24.15
 Stem         431 :   1000 bp (total : 250623) coverage : 1247.11
 Stem        -369 :   1210 bp (total : 251833) coverage : 482.06
 Stem        -128 :     76 bp (total : 251909) coverage :  31.48
 Stem         -39 :     76 bp (total : 251985) coverage :  32.79
 Stem        -327 :     27 bp (total : 252012) coverage :  21.64
 Stem        -244 :    170 bp (total : 252182) coverage : 907.82
 Stem        -175 :     82 bp (total : 252264) coverage :  48.67
 Stem        -140 :     26 bp (total : 252290) coverage :  86.04
 Stem        -418 :     89 bp (total : 252379) coverage : 435.42
 Stem        -419 :     90 bp (total : 252469) coverage :  47.73
 Stem        -372 :    373 bp (total : 252842) coverage : 1088.86
 Stem        -316 :     29 bp (total : 252871) coverage :  33.67
 Stem         432 :   2513 bp (total : 255384) coverage : 1097.34
 Stem        -261 :   2359 bp (total : 257743) coverage : 571.08
 Stem        -289 :     73 bp (total : 257816) coverage :  17.74
 Stem        -416 :    815 bp (total : 258631) coverage :  33.67
 Stem        -357 :     45 bp (total : 258676) coverage : 814.59
 Stem        -430 :     91 bp (total : 258767) coverage :  24.15
 Stem         -72 :     12 bp (total : 258779) coverage : 116.54
 Stem        -295 :   1369 bp (total : 260148) coverage : 594.57
 Stem        -407 :   2350 bp (total : 262498) coverage : 584.22
 Stem        -393 :     12 bp (total : 262510) coverage :   7.77
 Stem        -163 :     25 bp (total : 262535) coverage :  23.31
 Stem        -222 :   2289 bp (total : 264824) coverage : 605.65
 Stem        -412 :     29 bp (total : 264853) coverage :  80.80
 Stem         433 :     91 bp (total : 264944) coverage :  40.62
 Stem          -6 :      1 bp (total : 264945) coverage : 404.00
 Stem        -417 :    580 bp (total : 265525) coverage : 1134.29
 Stem         -50 :   1557 bp (total : 267082) coverage : 1162.54
 Stem        -225 :     88 bp (total : 267170) coverage : 1089.44
 Stem        -146 :   2647 bp (total : 269817) coverage : 551.08
 Stem        -304 :     69 bp (total : 269886) coverage :  54.83
 Stem        -134 :     20 bp (total : 269906) coverage :   0.00
 Stem         -88 :     91 bp (total : 269997) coverage :  27.45
 Stem        -422 :   1202 bp (total : 271199) coverage : 510.88
 Stem        -433 :     91 bp (total : 271290) coverage :  40.62
 Stem        -159 :   1039 bp (total : 272329) coverage :  28.94
 Stem        -408 :     28 bp (total : 272357) coverage : 303.00
 Stem        -323 :     14 bp (total : 272371) coverage : 269.33
 Stem        -343 :     17 bp (total : 272388) coverage : 555.50
 Stem        -370 :     20 bp (total : 272408) coverage :  81.76
 Stem        -320 :    280 bp (total : 272688) coverage : 719.22
 Stem        -431 :   1000 bp (total : 273688) coverage : 1247.11
 Stem        -324 :     20 bp (total : 273708) coverage :  76.95
 Stem        -404 :     22 bp (total : 273730) coverage :  43.91
 Stem        -318 :     64 bp (total : 273794) coverage :  20.20
 Stem        -425 :    102 bp (total : 273896) coverage : 390.27
 Stem        -358 :      1 bp (total : 273897) coverage : 252.50
 Stem         -89 :     28 bp (total : 273925) coverage :  66.17
 Stem         -33 :     17 bp (total : 273942) coverage :  72.94
 Stem        -423 :     13 bp (total : 273955) coverage :  28.86
 Stem        -428 :      4 bp (total : 273959) coverage : 808.00
 Stem        -328 :     14 bp (total : 273973) coverage :  67.33
 Stem        -426 :   2321 bp (total : 276294) coverage : 511.22
 Stem        -402 :     96 bp (total : 276390) coverage :  51.02
 Stem        -237 :     35 bp (total : 276425) coverage : 471.33
 Stem        -390 :     35 bp (total : 276460) coverage :  33.67
 Stem        -420 :     96 bp (total : 276556) coverage :  73.93
 Stem        -241 :     17 bp (total : 276573) coverage :  84.17
 Stem        -216 :     15 bp (total : 276588) coverage :  12.62
 Stem        -197 :     16 bp (total : 276604) coverage : 932.76
 Stem        -398 :    271 bp (total : 276875) coverage : 801.32
 Stem        -405 :    128 bp (total : 277003) coverage : 1197.12
 Stem        -415 :     53 bp (total : 277056) coverage : 353.50
 Stem        -414 :     39 bp (total : 277095) coverage :  55.55
 Stem        -395 :      2 bp (total : 277097) coverage : 269.33
 Stem        -376 :    125 bp (total : 277222) coverage : 1115.01
 Stem         -93 :   1481 bp (total : 278703) coverage : 556.39
 Stem        -337 :    512 bp (total : 279215) coverage : 838.91
 Stem        -191 :   1353 bp (total : 280568) coverage : 472.70
 Stem        -353 :     13 bp (total : 280581) coverage :  57.71
 Stem         -86 :     19 bp (total : 280600) coverage : 323.20
 Stem        -429 :     90 bp (total : 280690) coverage :  46.62
 Stem        -383 :     16 bp (total : 280706) coverage : 118.82
 Stem        -424 :      3 bp (total : 280709) coverage : 833.25
 Stem        -344 :    262 bp (total : 280971) coverage : 216.98
 Stem        -363 :     89 bp (total : 281060) coverage :  68.46
 Stem        -427 :      1 bp (total : 281061) coverage : 656.50
 Stem        -204 :     67 bp (total : 281128) coverage :  29.71
 Stem         -31 :     12 bp (total : 281140) coverage :  15.54
 Stem        -403 :     19 bp (total : 281159) coverage :  75.75
 Stem        -102 :   2986 bp (total : 284145) coverage : 612.39
 Stem         -34 :   3415 bp (total : 287560) coverage : 599.41
 Stem        -399 :     12 bp (total : 287572) coverage :  62.15
 Stem        -396 :     39 bp (total : 287611) coverage :  42.92
 Stem         -37 :     12 bp (total : 287623) coverage :   7.77
 Stem        -226 :     23 bp (total : 287646) coverage :  71.54
 Stem        -432 :   2513 bp (total : 290159) coverage : 1097.34
 Stem        -294 :   1686 bp (total : 291845) coverage : 566.91
 Stem        -410 :     23 bp (total : 291868) coverage : 887.96
 Stem        -298 :     14 bp (total : 291882) coverage : 134.67
 Stem         -14 :    124 bp (total : 292006) coverage :  54.94
 Stem        -209 :     60 bp (total : 292066) coverage :  23.18

Minimum stem coverage = 0


