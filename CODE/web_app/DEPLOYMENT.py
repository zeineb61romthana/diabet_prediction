import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import joblib  # Add this import statement

# Load the trained model
model = joblib.load('random_forest_model.pkl')

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Diabetes Predictor', style={'color': '#004d99', 'text-align': 'center', 'font-size': '3em', 'font-family': 'Arial, sans-serif'}),
        html.Hr(),
    ], style={'margin': '20px'}),
    
    # Prediction form
    html.Div([
        html.H2('Enter Patient Information', style={'color': '#004d99', 'margin-bottom': '20px', 'font-size': '2em'}),
        html.Div([
            html.Label('Number of Pregnancies', style={'font-weight': 'bold'}),
            dcc.Input(id='pregnancies', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Plasma Glucose Concentration (mg/dL)', style={'font-weight': 'bold'}),
            dcc.Input(id='glucose', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Diastolic Blood Pressure (mm Hg)', style={'font-weight': 'bold'}),
            dcc.Input(id='blood_pressure', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Skin Thickness (mm)', style={'font-weight': 'bold'}),
            dcc.Input(id='skin_thickness', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Serum Insulin (mu U/ml)', style={'font-weight': 'bold'}),
            dcc.Input(id='insulin', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('BMI (kg/m^2)', style={'font-weight': 'bold'}),
            dcc.Input(id='bmi', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Diabetes Pedigree Function', style={'font-weight': 'bold'}),
            dcc.Input(id='dpf', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '10px'}),
        html.Div([
            html.Label('Age (years)', style={'font-weight': 'bold'}),
            dcc.Input(id='age', type='number', value=0, style={'width': '100%'}),
        ], style={'margin-bottom': '20px'}),
        html.Button('Predict', id='predict-button', className='btn btn-danger btn-lg btn-block', style={'margin-bottom': '10px'}),
        html.Div(id='prediction-output', style={'margin-top': '10px', 'font-weight': 'bold', 'text-align': 'center'})
    ], style={'padding': '20px', 'border': '1px solid #dee2e6', 'border-radius': '5px', 'background-color': '#f8f9fa', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),
    
], style={'background-color': '#f0f5f5', 'padding-top': '50px'})

# Define callback to update the output
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [
        Input('pregnancies', 'value'),
        Input('glucose', 'value'),
        Input('blood_pressure', 'value'),
        Input('skin_thickness', 'value'),
        Input('insulin', 'value'),
        Input('bmi', 'value'),
        Input('dpf', 'value'),
        Input('age', 'value')
    ]
)
def predict_diabetes(n_clicks, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age):
    # Create a DataFrame with the input values
    input_data = pd.DataFrame({
        'Pregnancies': [pregnancies],
        'Glucose': [glucose],
        'BloodPressure': [blood_pressure],
        'SkinThickness': [skin_thickness],
        'Insulin': [insulin],
        'BMI': [bmi],
        'DiabetesPedigreeFunction': [dpf],
        'Age': [age]
    })

    # Use the model to make a prediction
    prediction = model.predict(input_data)[0]

    if prediction == 0:
        result = 'No diabetes risk detected.'
    else:
        result = 'Diabetes risk detected.'

    return html.Div([
        html.H3('Prediction Result', style={'color': '#004d99'}),
        html.P(result, style={'font-weight': 'bold'})
    ], style={'text-align': 'center'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
