# SpirographGL

## Demo

A demo to compute a spirograph curve with PyOpenGL on vertex shaders, passing in parameters.

![](data/spirographDemo.gif)

A spirograph is a toy to create pretty curves with a pen and cogs with holes.

`spirograph.py` is a demo demonstrating usage of vertex shaders in Python to compute and visualize these curves, depending on the geometry of the cogs and the location of the hole within the cog.

A `GL_LINE_STRIP` of fixed length is loaded onto the OpenGL device to render a [Hypotrochoid curve](https://en.wikipedia.org/wiki/Hypotrochoid) modelling the spirograph behaviour.
The position of each vertex is computed within the vertex shader, using the formulas explained in the [Spirograph article in wikipedia](https://en.wikipedia.org/wiki/Spirograph#Mathematical_basis).

The vertex shader implementation in Python is this:
```
VERTEX_SHADER_SOURCE = '''
    #version 330 core
    layout (location = 0) in vec3 aPos;
    
    uniform float param_radiusRatio;
    uniform float param_holePosition;
    
    out float coll;
    
    void main()
    {
        float t = aPos[2]/36;
        float coeff = ((1-param_radiusRatio)/param_radiusRatio)*t;
        float xt = (1.0-param_radiusRatio) * cos(t) + param_radiusRatio * param_holePosition * cos(coeff);
        float yt = (1.0-param_radiusRatio) * sin(t) + param_radiusRatio * param_holePosition * sin(coeff);
    
        //gl_Position = vec4(aPos[0],param_radiusRatio,0.0, 1.0);
        
        gl_Position = vec4(xt, yt,0.0, 1.0);
        
        coll = aPos[2];

    }
'''
```


The program `spirograph.py` keeps the line length fixed, and also fixes one of the spirograph parameters, while itering through the other one in small steps within the range 0 to 1.

## Interactive plotter

For more freedom to to explore the parameter space, `spirograph.py` is split into a slave code `spirographSlave.py` receiving these parameters, and a controller code generating the parameter. These two are running in separate processes, and communicate via sockets on port 6123 on `localhost`. 
Parameters are sent as string-encoded tuples for: line length, relative cog size, and relative hole position.
Now, the change of curve can be controlled from different controller programs, including GUIs.

The slave program is started by the controller with multiprocessing command `Popen`. Both run in parallel. The slave is then polling parameter values from the socket, and passes these parameters to the vertex shades once received.

