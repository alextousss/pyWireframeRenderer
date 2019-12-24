# pyWireframeRenderer
Renders .obj files in 3D.  
It doesn't use any OpenGL and is self-contained in 200LOC.  
Its only dependencies are Numpy for matrix multiplications and Pygame to render to the screen. 
## Screenshots
### Teapot
![teapot rendered with pyWireframeRenderer](https://raw.githubusercontent.com/belzebalex/pyWireframeRenderer/master/images/teapot.png "Teapot Render")

### Cube
![Cube rendered with pyWireframeRenderer](https://raw.githubusercontent.com/belzebalex/pyWireframeRenderer/master/images/cube_demo.png "Cube Render")

## Install
```
git clone https://github.com/belzebalex/pyWireframeRenderer/
cd pyWireframeRenderer
pip3 install pygame numpy
```

## Usage
```
python3 renderer.py cube.obj
```

Use zqsdae to translate and uiojkl to rotate.


