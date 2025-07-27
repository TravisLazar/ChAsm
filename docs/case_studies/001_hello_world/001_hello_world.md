# Hello World

ChAsm as a library is designed to use sane and logical defaults for every single configuration option. The only two things required for basic chart generation are a chart type and data, which takes the form of a ChAsm command like this:

```bash
# Passing Data Directly
chasm bar --data '[{"x0":"Point1", "y0":10},{"x0":"Point2", "y0":15}]' -o path/chart1.svg

# Passing Data as a File
chasm bar --data data/simple_bar.data.json -o path/chart1.svg

# Passing Data Using Bash Evaluation
chasm bar --data "$(cat data/simple_bar.data.json)" -o path/chart1.svg
```

Each of these commands would produce a default chart that looks like this.

![chart1](chart1.svg)

A couple things to notice.

The `--data` argument must always evaluate to a list of dictionaries. This is non-negotiable in ChAsm, and many of the features included in this library depend on this base assumption that the root data structure is a list of dictionaries. 

The `--data` argument may also be a string representation of JSON or a pointer to a file that contains valid JSON. ChAsm will figure out which one you've used, so no need to be specific. 

Additionally, `x0` and `y0` are assumed to be the default keys for the x and y coordinates of our data, no need to specify x and y keys if they follow this default naming. Additional enumerations of x and y (x1, x2, x3, etc.) are used when multiple series are included in our dataset. 

