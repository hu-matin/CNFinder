
<div align="center">
  [فارسی](README_FA.md)
</div>

# CNFinder

**CNFinder** is a lightweight CNAME enumeration tool built for web pentesters and security researchers.

> It automates repetitive DNS lookup commands, allowing you to quickly check a list of domains and identify their CNAME records without manually running `dig` or `nslookup` for every target.

>[!TIP]
> This script doesn't need anything to install, just run the `cnfinfer.py` to get the result.

## Usage

### Input

Specify a `.txt` file containing domains:

```bash
python cnfinder.py -i domains.txt
```

### Output

Save only domains with found CNAME records to a `.txt` file:

```bash
python cnfinder.py -i domains.txt -o results.txt
```

## Flags

| Flag             | Description                                |
| ---------------- | ------------------------------------------ |
| `-i`, `--input`  | Input `.txt` file containing domains       |
| `-o`, `--output` | Output `.txt` file for found CNAME records |

## Features

* CNAME enumeration
* Automates repetitive DNS lookups
* TXT input/output
* Supports Windows & Linux & Mac
* No external Python dependencies
