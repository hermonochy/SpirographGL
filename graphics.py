from OpenGL.GL import *
from ctypes import sizeof, c_void_p

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

FRAGMENT_SHADER_SOURCE = '''
    #version 330 core
    uniform float param_radiusRatio;
    uniform float param_holePosition;

    in float coll;

    out vec4 fragColor;
    
    void main()
    {

        fragColor = vec4(1.0f, max(1.0f - max(0.0f, sin(coll/12000.0f)), sin(coll/12000.0f)), cos(coll/12000.0f), 1.0f);
    }
'''


def initOpenGL(vertices):
  # we created program object 
  program = glCreateProgram()

  # we created vertex shader
  vertex_shader = glCreateShader(GL_VERTEX_SHADER)
  # we passed vertex shader's source to vertex_shader object
  glShaderSource(vertex_shader, VERTEX_SHADER_SOURCE)
  # and we compile it
  glCompileShader(vertex_shader)


  # we created fragment shader
  fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
  # we passed fragment shader's source to fragment_shader object
  glShaderSource(fragment_shader, FRAGMENT_SHADER_SOURCE)
  # and we compile it
  glCompileShader(fragment_shader)


  # attach these shaders to program
  glAttachShader(program, vertex_shader)
  glAttachShader(program, fragment_shader)

  # link the program
  glLinkProgram(program)

  # create vbo object
  vbo = None
  vbo = glGenBuffers(1, vbo)

  # enable buffer(VBO)
  glBindBuffer(GL_ARRAY_BUFFER, vbo)

  # send the data  
  glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW)

  # create vao object
  vao = None
  vao = glGenVertexArrays(1, vao)

  # enable VAO and then finally binding to VBO object what we created before.
  glBindVertexArray(vao)

  # we activated to the slot of position in VAO (vertex array object)
  glEnableVertexAttribArray(0)

  # explaining to the VAO what data will be used for slot 0 (position slot) 
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), c_void_p(0))

  return program, vao

