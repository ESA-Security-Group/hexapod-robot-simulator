import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import plotly.graph_objs as go

from hexapod import Point, Linkage, Hexagon, VirtualHexapod, HexapodPlot
from app import app


# -----------
# Sliders 
# -----------
SLIDER_ANGLE_MARKS = {tick: str(tick) for tick in [-90, -45, 0, 45, 90]}

SLIDER_ALPHA = dcc.Slider(id='slider-alpha', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_BETA = dcc.Slider(id='slider-beta', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)
SLIDER_GAMMA = dcc.Slider(id='slider-gamma', min=-90, max=90, marks=SLIDER_ANGLE_MARKS, value=0, step=5)

SLIDER_MARKS = {tick: str(tick) for tick in [20, 40, 60, 80, 100]}

SLIDER_FRONT = dcc.Slider(id='slider-front', min=20, max=100, marks=SLIDER_MARKS, value=70, step=5)
SLIDER_SIDE = dcc.Slider(id='slider-side', min=20, max=100, marks=SLIDER_MARKS, value=70, step=5)
SLIDER_MIDDLE = dcc.Slider(id='slider-middle', min=20, max=100, marks=SLIDER_MARKS, value=70, step=5)

SLIDER_COXIA = dcc.Slider(id='slider-coxia', min=20, max=100, marks=SLIDER_MARKS, value=70, step=5)
SLIDER_FEMUR = dcc.Slider(id='slider-femur', min=20, max=100, marks=SLIDER_MARKS, value=70, step=5)
SLIDER_TIBIA = dcc.Slider(id='slider-tibia', min=20, max=100, marks=SLIDER_MARKS, value=70, step=5)

# -----------
# SECTION AND LAYOUT
# -----------
section_sliders_body = html.Div([
  html.Div([ html.Label('Front Length'), SLIDER_FRONT], style={'width': '33%'}),
  html.Div([ html.Label('Side Length'), SLIDER_SIDE], style={'width': '33%'}),
  html.Div([ html.Label('Middle Length'), SLIDER_MIDDLE], style={'width': '33%'}),
  ],
  style={'display': 'flex'})

section_sliders_leg = html.Div([
  html.Div([ html.Label('Coxia Length'), SLIDER_COXIA], style={'width': '33%'}),
  html.Div([ html.Label('Femur Length'), SLIDER_FEMUR], style={'width': '33%'}),
  html.Div([ html.Label('Tibia Length'), SLIDER_TIBIA], style={'width': '33%'}),
  ],
  style={'display': 'flex'})

section_sliders_angles = html.Div([
  html.Div([ html.Label('Alpha'), SLIDER_ALPHA], style={'width': '33%'}),
  html.Div([ html.Label('Beta'), SLIDER_BETA], style={'width': '33%'}),
  html.Div([ html.Label('Gamma'), SLIDER_GAMMA], style={'width': '33%'}),
  ],
  style={'display': 'flex'})


section_hexapod = html.Div([
  html.Div(dcc.Graph(id='hexapod-plot'), style={'width': '50%'}),
  html.Div([section_sliders_body, section_sliders_leg, section_sliders_angles], style={'width': '40%'}),
  html.Div(id='display-variables', style={'width': '10%'}),
  ], 
  style={'display': 'flex'})

layout = html.Div([
  html.H3('Customization'),
  section_hexapod,
  html.Div(id='variables', style={'display': 'none'}),
])

# -----------
# CALLBACKS
# -----------
SLIDER_IDs = [
  'slider-alpha', 
  'slider-beta', 
  'slider-gamma',
  'slider-front', 
  'slider-side', 
  'slider-middle',
  'slider-coxia', 
  'slider-femur', 
  'slider-tibia',
]
@app.callback(
  Output('variables', 'children'),
  [Input(i, 'value') for i in SLIDER_IDs]
)
def update_variable(alpha, beta, gamma, f, s, m, h, k, a):
  return json.dumps({
    'alpha': alpha,
    'beta': beta,
    'gamma': gamma,
    'front': f,
    'side': s,
    'middle': m,
    'coxia': h,
    'femur': k,
    'tibia': a,
  })

@app.callback(
  Output('display-variables', 'children'),
  [Input('variables', 'children')]
)
def display_variables(pose_params):
  p = json.loads(pose_params)
  s = ""
  for k, v in p.items():
    s += "- `{}: {}` \n".format(k, v)
  
  return dcc.Markdown(s)

@app.callback(
  Output('hexapod-plot', 'figure'),
  [Input(slider_id, 'value') for slider_id in SLIDER_IDs]
)
def update_hexapod_plot(alpha, beta, gamma, f, s, m, h, k, a):
  virtual_hexapod = VirtualHexapod(h, k, a, f, m, s)
  hexaplot = HexapodPlot(virtual_hexapod)

  for leg in virtual_hexapod.legs:
    leg.change_pose(alpha, beta, gamma)
  fig = hexaplot.update(virtual_hexapod)
  return fig
