# Examples

This section collects practical EtherLyzer workflows.

## Identify a vendor

**Command**
```text
etherlyzer whois 00:00:0c:12:34:56
```

**Output** 
```text
MA-L    00000C  Cisco Systems, Inc
```
## Inspect the complete IEEE allocation

Vendor identification tells you who owns an address. `inspect` shows what the
address actually belongs to.

**Command**
```shell
etherlyzer inspect 00:00:0c:12:34:56
```

**Output**
```text
Organization
  Name            : Cisco Systems
  Full Name       : Cisco Systems, Inc

Registry
  IEEE Type       : MA-L [MAC Address Block Large]
  Assignment      : 00-00-0c
  Range           : 00-00-0c-00-00-00 - 00-00-0c-ff-ff-ff
  Legacy          : False
  Prefix Bits     : 24 bits
  Address Bits    : 24 bits
  Addresses       : 16,777,216
  
Vendor Blocks
  Total Blocks    : 1258
  Address Capacity
    Total         : 21,105,737,728
    MA-L          : 21,105,737,728
    MA-M          : 0
    MA-S          : 0
    IAB           : 0
    Registered Blocks (B=IAB, S=MA-S, M=MA-M, L=MA-L)
      [L] 00-00-0c      [L] 00-01-42      [L] 00-01-43      [L] 00-01-63      [L] 00-01-64
      [L] 00-01-96      [L] 00-01-97      [L] 00-01-c7      [L] 00-01-c9      [L] 00-02-16
      [L] 00-02-17      [L] 00-02-3d      [L] 00-02-4a      [L] 00-02-4b      [L] 00-02-7d
      ...
      <omitted for bevity>
```

Etherlyzer also correlates other known IEEE MAC allocations belonging to the same organization.

## Validate without Silently Fixing Input

**Command**
```shell
etherlyzer validate 001a2b3c4d5O
```

**Output**
```text
ERR 001a2b3c4d5O => vvvvvvvvvvvr
```

Validation reports the problem rather than modifying the value.

To explicitly repair supported typo-like input:

**Command**
```shell
etherlyzer format 001a2b3c4d5O --fix-typos
```

**Output**
```text
00:1a:2b:3c:4d:50
```

## Bulk Validation

**Command**
```shell
etherlyzer validate --bulk --linenumbers --show-info --show-originals
```

**Input**
```text
Paste MAC addresses. Type ;;; and press <Enter> when done:
00:1a:2b:3c:4d:5e:6f:70
00-1a-2b-3c-4d-5e-6f
00-1a-2b-3c
001a.2b3c.4d
001a.2b3c.4d5

001a2b3c4d5k
001a2b3c4d5l
001a2b3c4d5m
00-1a-2b-3c-4d-5g
001a.2b3c.4d5g
001a2O3c4d5e
001a2bOc4d5e
001a2b3O4d5e
00:1a:2b:3c:4d:5O
001a2b3c4d5D{
001a2b3c4d5A
00:1a:2b:@3c:4d:5e
00-1a-2b-3c-4d-5@
001a.2b#c.4d5e}
'001a2b3c4d5e'
'00:1a:2b:3c:4d:5e'
;;;
```

**Output**
```terminaloutput

1.  ERR 001a2b3c4d5e6f. => vvvvvvvvvvvvVVVV
2.  ERR 001a2b3c4d5e6f  => vvvvvvvvvvvvVV
3.  ERR 001a2b3c        => vvvvvvvvMMMM
4.  ERR 001a2b3c4d      => vvvvvvvvvvMM
5.  ERR 001a2b3c4d5     => vvvvvvvvvvvM
6.  ERR 001a2b3c4d5k    => vvvvvvvvvvvi
7.  ERR 001a2b3c4d5l    => vvvvvvvvvvvl
8.  ERR 001a2b3c4d5m    => vvvvvvvvvvvi
9.  ERR 001a2b3c4d5g    => vvvvvvvvvvvi
10. ERR 001a2b3c4d5g    => vvvvvvvvvvvi
11. ERR 001a2O3c4d5e    => vvvvvrvvvvvv
12. ERR 001a2bOc4d5e    => vvvvvvrvvvvv
13. ERR 001a2b3O4d5e    => vvvvvvvrvvvv
14. ERR 001a2b3c4d5O    => vvvvvvvvvvvr
15. OK  001a2b3c4d5d    <~ 001a2b3c4d5D{
16. OK  001a2b3c4d5a    <~ 001a2b3c4d5A
17. OK  001a2b3c4d5e    <~ 00:1a:2b:@3c:4d:5e
18. ERR 001a2b3c4d5     => vvvvvvvvvvvM
19. ERR 001a2bc4d5e     => vvvvvvvvvvvM
20. OK  001a2b3c4d5e    <~ '001a2b3c4d5e'
21. OK  001a2b3c4d5e    <~ '00:1a:2b:3c:4d:5e'

Normalized 5/21 MAC addresses. Invalid MAC addresses identified: 16/21
```

## Repair Badly Formatted Input

Formatting can optionally correct supported typo-like character substitutions.

**Command**
```shell
etherlyzer format "l..iIdOØ1!23-4oo.." --fix-typos --casing upper --block-size 4 --separator .
```

**Output**
```text
111D.0012.3400
```

## Bulk Format MAC addresses

**Command**
```shell
etherlyzer format --bulk --separator . --block-size 4 --casing lower
```

**Input**
```text
Paste MAC addresses. Type ;;; and press <Enter> when done:
01:1A:2B:3C:4D:5E
02-1a-2b-3c-4d-5e
031A.2B3C.4D5E
041a2b3c4d5e
05 1A 2B 3C 4D 5E
08:00:27:AA:bb:CC
10-9A-DD-4F-7c-21
18D6.C7A1.B204
20:4E:7F-9a:BC-01
28 6F B9 33 A0 7D
30:5A:3A:11:22:33
38-2C-4A-9F-00-01
40F2.E9AB.CD10
48:2A:E3:7B-91:0F
50 7B 9D 2A 44 8C
58:EF:68:AA:01:BC
60-45-BD-7e-19-A2
68A3.C4D5.E6F7
70:88:6B-1C:2D-3E
78 24 AF 9B C0 D1
;;;
```

**Output**
```text
011a.2b3c.4d5e
021a.2b3c.4d5e
031a.2b3c.4d5e
041a.2b3c.4d5e
051a.2b3c.4d5e
0800.27aa.bbcc
109a.dd4f.7c21
18d6.c7a1.b204
204e.7f9a.bc01
286f.b933.a07d
305a.3a11.2233
382c.4a9f.0001
40f2.e9ab.cd10
482a.e37b.910f
507b.9d2a.448c
58ef.68aa.01bc
6045.bd7e.19a2
68a3.c4d5.e6f7
7088.6b1c.2d3e
7824.af9b.c0d1
```

## Cisco-style formatting

**Command**
```text
etherlyzer format 001122334455 -p . -s 4
```
## Windows-style formatting

**Command**
```text
etherlyzer format 001122334455 -p - -s 2
```

## Bulk vendor lookup from a file

**Command**
```text
etherlyzer whois -f ./macs.txt
```

## Synchronize registries

**Command**
```text
etherlyzer sync
```
