---
hide-toc: true
---

# EtherLyzer

**Ethernet address intelligence, analysis, and forensics.**

{{ version_badge }} {bdg-light}`Python 3.12+` {bdg-light}`MIT License` {bdg-light}`CLI & Python API`

EtherLyzer is an open-source Python toolkit for Ethernet address intelligence and analysis. It combines offline IEEE registry lookups with detailed MAC address inspection, structural classification, representation analysis, and address extraction from packet captures. Available through both a command-line interface and Python API, EtherLyzer provides the tools to investigate Ethernet identifiers beyond conventional vendor lookups.

## Beyond the Traditional OUI Lookup

Ethernet addressing is considerably more complex than the familiar assumption that the first 24 bits of a MAC address identify its manufacturer. IEEE defines multiple allocation schemes with different prefix lengths, overlapping organizational namespaces, legacy assignments, and distinct rules governing individual, group, and locally administered addresses. Correct interpretation requires an understanding of allocation boundaries, identifier structures, address-bit semantics, and the standards governing their use.

EtherLyzer brings these concepts together through **standards-aware classification, precise registry resolution, and detailed address analysis**. Rather than simply returning a vendor name, it examines what an identifier represents, how it is constructed, which allocations or registrations it relates to, and what can reliably be established from the available evidence.

## Where Conventional Lookups Fall Short

The complexity of IEEE addressing introduces subtle edge cases that conventional MAC address lookups can overlook or misinterpret. A 36-bit MA-S or legacy IAB allocation may exist within an enclosing 24-bit OUI, potentially causing a simple OUI lookup to attribute an address to the wrong organization. Group addresses may be derived from registered allocations by manipulating the I/G bit, but the applicable rules differ between MA-L, MA-M, MA-S, IAB, and CID assignments. Locally administered addresses introduce further complexity through the **Structured Local Address Plan (SLAP)**, while incomplete MAC prefixes can make allocation resolution ambiguous.

EtherLyzer addresses these cases through **longest-prefix matching, allocation-aware lookup rules, conditional exclusions, and explicit identifier classifications**. It distinguishes verified registry matches from structural interpretations, respects the limitations of individual allocation schemes, and avoids treating incomplete or ambiguous evidence as definitive. The result is a more accurate and transparent interpretation of Ethernet identifiers, including cases where traditional OUI lookups may produce incomplete or misleading results.

## A Comprehensive Ethernet Analysis Toolkit

Beyond these specialized analyses, EtherLyzer provides a broader collection of tools for working with Ethernet identifiers. Its capabilities extend to MAC address validation and formatting, alternative representations and bit-level analysis, EtherType and company identifier inspection, vendor allocation statistics, bulk processing, and address extraction from packet captures. With locally maintained IEEE registry data, synchronization utilities, and both a command-line interface and Python API, EtherLyzer supports everything from individual identifier investigations to automated network inventory analysis and forensic workflows. Whether identifying an unfamiliar address, examining a protocol assignment, or processing thousands of network identifiers, EtherLyzer brings these capabilities together in a consistent, extensible toolkit designed for practical network engineering.

## Documentation

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} {octicon}`rocket;1em` Getting Started
:link: getting-started/index
:link-type: doc

Installation, setup, and first steps.
:::

:::{grid-item-card} {octicon}`book;1em` Concepts
:link: concepts/index
:link-type: doc

Ethernet addressing fundamentals, IEEE registries, and identifier structures.
:::

:::{grid-item-card} {octicon}`tools;1em` Guides
:link: guides/index
:link-type: doc

Detailed command usage, options, and analytical behavior.
:::

:::{grid-item-card} {octicon}`terminal;1em` Cookbook
:link: cookbook/index
:link-type: doc

Practical examples, troubleshooting, and investigative workflows.
:::

:::{grid-item-card} {octicon}`code;1em` API Reference
:link: api/index
:link-type: doc

Python modules, classes, functions, and programmatic usage.
:::

::::

```{toctree}
:hidden:
:maxdepth: 2
:titlesonly:

getting-started/index
concepts/index
guides/index
cookbook/index
api/index
```
