# MAC Validation

EtherLyzer can validate and normalize MAC-address input and produce character-level diagnostics for malformed values.

Validation and formatting are intentionally separate operations:

- `validate` interprets input and reports problems without typo correction.
- `format --fix-typos` may correct supported typo-like substitutions.

## Validation masks

Validation diagnostics use a compact character-by-character mask.

| Character itself        | Position          | Flag |
|-------------------------|-------------------|------|
| Valid hexadecimal digit | Valid             | `v`  |
| Valid hexadecimal digit | Overflow          | `V`  |
| Relaxed substitution    | Valid             | `r`  |
| Relaxed substitution    | Overflow          | `R`  |
| Lenient substitution    | Valid             | `l`  |
| Lenient substitution    | Overflow          | `L`  |
| Invalid character       | Anywhere          | `I`  |
| Missing character       | Expected position | `M`  |

Lowercase substitution flags indicate a substitution candidate in a valid position.

Uppercase substitution flags indicate a substitution candidate in an overflow position (except M and I).

## Examples

```text
001a2b3c4d5     => vvvvvvvvvvvM
001a2b3c4d5e6   => vvvvvvvvvvvvV
0x1a2b3c4d5O    => vIvvvvvvvvvrM
001a2b3c4d5I    => vvvvvvvvvvvl
```

### Missing digit

```text
001a2b3c4d5     => vvvvvvvvvvvM
```

The input contains 11 hexadecimal digits. One hexadecimal digit is missing.

### Overflow

```text
001a2b3c4d5e6   => vvvvvvvvvvvvV
```

The first 12 hexadecimal digits occupy valid positions. The final digit exceeds the 12-digit EUI-48 length and is marked as overflow.

### Invalid character and missing digit

```text
0x1a2b3c4d5O    => vIvvvvvvvvvrM
```

The `x` is invalid and is marked with `I`.

The final `O` is recognized as a relaxed substitution candidate and marked with `r`. This leaves 11 usable hexadecimal positions, so the mask ends with `M` to indicate one missing digit.

### Lenient substitution

```text
001a2b3c4d5I    => vvvvvvvvvvvl
```

The first 11 characters are valid hexadecimal digits. The final character is recognized as a lenient substitution candidate and marked with `l`.
