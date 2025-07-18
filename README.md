# ChartAssembler (ChAsm)

I absolutely love data visualization, but I hate the boilerplate of many visualization libraries and I often find it cumbersome to setup my charting workflow. Maybe it's skill diff and I'm just a poor quality developer, but I still wanted a solution to the workflow of creating charts and visualizations. I also want a place to wrappers for special chart types (like Gantt, timeline, etc) and share them with others who have may have similar pain points.  

And thus, ChartAssembler was born. A library that is fully focused on the _workflow_ of creating charts and visualizations - both from the command line and from within any Python script you desire. This library doesn't replace existing charting libraries (like Plotly), it augments them. Under the hood this library currently uses Plotly with additional rendering options planned. 

## The Basic Architecture of ChAsm

If you really break down the fundamentals of a chart, there are three core components:

1. The Data
2. The Chart Details
3. The Design

ChartAssembler interacts with these components in a few different ways. 


### The Data

All data inputs into ChartAssembler are expected to be a list of dictionaries. This might sound dumb and limiting (I may very well discover that it is), but it makes a lot of other things simpler and solves one of my biggest annoyances with creating new charts. 

The Data is then augmented through 0 or more manipulators, which tell ChAsm how to morph or interpret the raw data. While this is somewhat of an optional step, I often find that data formatting is a task I repeat for every different chart, so why not create some standard options for 90% of scenarios? 

In a fake example, we might have some input data that looks like this:

```
[
    {
        "x": "Category 1",
        "y": 412.50
    },
    ... a bunch of other objects
]
```

And we can then render it into a chart using a command like this:

```
chasm bar --data "$(cat simple_bar.data.json)"
```

What if we actually want this bar chart to represent the accumulated values instead of raw values? In a normal world, you could have to write some kind of script to modify your data in a place that makes sense and then modify your charting code to use this new data. Instead, what if you could do something like:

```
# Shell Command
chasm bar --data "$(cat simple_bar.data.json)" --manipulate accumulator.yaml

# accumulator.chasm File
add y, -1, y
```

You can view the .chasm files as a sort of assembly code for chart data. The chart data will be iterated over, in order, and the .chasm code will be run on each data point. This lets us do some pretty cool things. And it lets us build up a collection of useful data manipulation layers. 

In this example the `add y, -1, y` instruction will add the value at key `y` to the value in the previous index (if it exists), and then store it in `y`. 

All data manipulators are run in order, and they're run before any chart layering is performed. 


### The Chart Details

One could easily win an argument claiming that the chart details and the chart design are the same thing, but I view them as critically different in terms of how we work with them in a day-to-day workflow. 

The chart details define the core constructs of a chart. For example, a bar chart is composed of one or more series of data plotted along a category x-axis and a numeric y-axis. Most chart libraries have layers of abstraction that let you (kind of) treat every chart like every other chart, but I'm looking for the simplest possible instantiation at this layer. I would rather have 20 different chart types than infinite flexibility in how we mix and match charts. 


### The Design

The design aspects of charting are actually where the idea for this library originated. I'm hugely particular when it comes to exactly how many pixels sit between the title and the chart area, the precise color scheme, and all other details pertaining to the look and feel. But I hate sitting down and re-writing boilerplate for removing axis titles, updating spacing, adding borders, and all other aesthetic elements. 

So we treat the design of the chart like layers of paint on a wall. Take this simple command:

```
chasm bar --data "$(cat simple_bar.data.json)"
```

This will render a bar chart with default values across the board. Now take this command:

```
chasm bar --data "$(cat simple_bar.data.json)" --layer remove_axis_titles.yaml

# Contents of remove_axis_titles.yaml
chart_yaxis_visible: false
chart_xaxis_visible: false
```

The chart will be built but not rendered, and then all layers will be iterated over to modify chart configuration values before the final rendering. This lets us create a library of styling elements that we can reuse however we want. This also lets us add some interesting markup for flexible behavior. This is a totally made-up example, but is an example of what this layering system could achieve. 

```
chasm bar --data "$(cat simple_bar.data.json)" --layer scale_up.yaml

# Contents of scale_up.yaml
chart_height: "^*1.5"
chart_width: "^*1.5"
chart_title_font_size: "^*1.1"
```

The `^*` syntax tells the ChAsm chart compiler to find the value in the previous layer and mutiply it by the number provided. This creates an environment where maybe I want to render the same data in different ways depending on my audience, and I don't want to write any code to do so. 

## What's Next?

This library is brand spankin new and I make no guarantees of code quality, stability, or any other attribute of good development. I don't plan to add testing as I go because TDD is for my day job; this is currently a fun hackery project to prove to myself that this workflow isn't totally dumb. 

I'll keep a document with the list of supported syntaxes for the variously mentioned filetypes. Until then, assume nothing is actually supported. 

I'll also keep this README up to date with the library. And feel free to submit any issues or PRs as you encounter things. 

While this library is in development mode I'll leave the version < 1.0.0.
