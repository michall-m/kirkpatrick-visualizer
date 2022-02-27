

# Point location visualizer

Kirkpatrick's Algorithm visualizer for log(n) point location in given planar subdivision based on triangulation refinement.

## Kirkpatrick's algorithm description

Kirkpatrick's algorithm for point location is also termed triangulation refinement method, because
it consists in triangulating newly created polygon (by currently the lowest degree vertex deletion)
till we delete all the vertices. 

Given subdivision (set of polygons) is enclosed by a triangle. This way, by creating triangulation's tree where the root is the triangle
which edges given subdivision, its children are overlapping triangles of the preceding triangulation
and the leaves are triangles composing initial triangulation, we can easily locate given points in log(n) time complexity.

## Instalation
This program uses the following python modules:

* Matplotlib
```
pip install matplotlib
```

* NumPy
```
pip install numpy
```

Clone this repository:

```
git clone https://github.com/michall-m/kirkpatrick-visuzalizer.git
```

## Running visualizer

### Executing program

```
python main.py <polygon_name>
```


<br />

### Drawing
Draw polygon, split it by edges and add some points to locate.

<p align="center">
  <img width="600" height="480" src="https://raw.githubusercontent.com/michall-m/kirkpatrick-visuzalizer/main/drawing.gif?token=GHSAT0AAAAAABRUYPOFFQZGWUGF2JE4FF2MYQ3RVTA">
</p>

<br />

### Vertex types
There are 5 types of vertices in various colors:


![#32CD32](https://via.placeholder.com/11/32CD32/000000?text=+) 
 **start** -   both neighbours are below and interior angle is less than π,

![#f03c15](https://via.placeholder.com/11/f03c15/000000?text=+)
 **end** -     both neighbours are above and interior angle is less than π,

![#0000FF](https://via.placeholder.com/11/0000FF/000000?text=+)
 **merge** -   both neighbours are above and interior angle is greater than π,

![#B0C4DE](https://via.placeholder.com/11/B0C4DE/000000?text=+)
 **split** -   both neighbours are below and interior angle is greater than π,

![#A0522D](https://via.placeholder.com/11/A0522D/000000?text=+) 
 **regular** - otherwise




<p align="center">
  <img width="600" height="480" src="https://raw.githubusercontent.com/michall-m/kirkpatrick-visuzalizer/main/vertex_types.png?token=GHSAT0AAAAAABRUYPOEPN7K6K4PPF26376EYQ3RYRA">
</p>

<br />


### Kirkpatrick's triangulation refinement method
Vertex selected to be deleted is marked as <span style="color:red;">red</span>, as well as all the triangles containing it.
After it's deletion, newly created polygon is triangulated and those triangles are marked as
<span style="color:green;">green</span>.



<p align="center">
  <img width="600" height="480" src="https://raw.githubusercontent.com/michall-m/kirkpatrick-visuzalizer/main/vertices_deleting.gif?token=GHSAT0AAAAAABRUYPOFKWLVXDK7COYUIRFSYQ3RY7Q">
</p>


<br />

### Point locating
<span style="color:yellow;">Yellow</span> means currently processed triangle, if it's correct it changes to <span style="color:green;">green</span>. 

<p align="center">
  <img width="600" height="480" src="https://raw.githubusercontent.com/michall-m/kirkpatrick-visuzalizer/main/first_point_locating.gif?token=GHSAT0AAAAAABRUYPOFHAKS43P7H7YNIJPMYQ3R2VA">
</p>

<p align="center">
  <img width="600" height="480" src="https://raw.githubusercontent.com/michall-m/kirkpatrick-visuzalizer/main/second_point_locating.gif?token=GHSAT0AAAAAABRUYPOF3R2VJXXKYP2ASD2AYQ3R26A">
</p>





<br />

## Acknowledgments

* [Kirkpatrick's point location](http://cgm.cs.mcgill.ca/~athens/cs507/Projects/2002/PaulSandulescu/)


