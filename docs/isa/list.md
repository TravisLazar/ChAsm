# ChAsm Modifier ISA

## **list appendrandint** (num, min, max, x_prefix, y_key)

Appends a random integer value within a given range to the end of the data list. This is most useful for generating test data with a starting array that is empty. 

| Parameter | Description |
|-----------|-------------|
|num        | Number of values to append. |
|min        | Lower bound of random numbers |
|max        | Upper bound of random numbers |
|x_prefix      | Prefix to use when creating new values for the x-axis (category) entry. An incrementing index of will be used for each element. e.g. XPRE 1, XPRE 2, XPRE 3, etc. |
|y_key      | Dictionary key to use when creation new values for y-axis (value). |

### Example Structure

```
# list appendrantint 10, 0, 100, Category, y_key
{
    "x_key": "Category 1",
    "y_key": random_value
},
{
    "x_key": "Category 2",
    "y_key": random_value
}
...
```