# Mushikuizan

## What is Mushikuizan

![mushikuizan](mushikuizan.png)

The above is an example of Mushikuizan.
Each 'x' is filled with a digit from 0 to 9 to complete
the process of a multiplication. The answer for this Mushikuizan
is 678 × 25 = 3390 + 13560 = 16950.

## Usage

```
python main.py [-v | --verbose] [<mushikuizan>]
```

The format of `<mushikuizan>` is `<first row> <second row>|[<row>...]|<last row>`. The command to solve the Mushikuizan
used in the previous section would be as follows:

```
python main.py "x7x x5|xx9x 1x56|16xxx"
```

To see how it solves the mushikuizan, use `--verbose` option.
