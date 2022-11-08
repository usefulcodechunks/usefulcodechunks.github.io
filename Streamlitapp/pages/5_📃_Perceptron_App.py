import streamlit as st
import pandas as pd
import numpy as np
from helperfunctions.perceptron import *
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.datasets import make_circles
import plotly.express as px

# TO DO
# Set the cutoff rate

# def side_bar_models():
#     with st.sidebar:
#         cols = st.columns(4)
#         for model in st.session_state.models:
#             cols[0].write(model)

def session_state_vars_for_app():
    if 'models' not in st.session_state:
        st.session_state.models = {}

def get_scores_for_data(score_df, model, accuracy_cutoff = .4):

    xdata = score_df[model.xcols]
    xvector = list(xdata.values)
    yvector = [list(score_df[model.ycol].values)]

    scoring_inputs = np.array(xvector)
    scoring_outputs = np.array(yvector).T

    df = pd.DataFrame(data=model.think(scoring_inputs),columns=["Predicted_Y"])
    df["Actual_Y"] = scoring_outputs
    df["Error"] = df["Actual_Y"] - df["Predicted_Y"]
    df["Accurate"] = abs(df["Error"]) < accuracy_cutoff
    for i in range(len(score_df.columns)):
        df[score_df.columns[i]] = score_df[score_df.columns[i]]

    return df, sum(df["Accurate"])/len(df["Accurate"]), sum(df["Error"])

def train_model_with_data(train_df, model, iterations):
    xdata = train_df[model.xcols]
    xvector = list(xdata.values)
    yvector = [list(train_df[model.ycol].values)]

    training_inputs = np.array(xvector)
    training_outputs = np.array(yvector).T

    model.train(training_inputs,training_outputs,iterations)

    return model

def generate_perceptron_model(df,xcols,ycol,iterations=0):
    model = Perceptron(df,xcols,ycol)

    xdata = df[xcols]
    xvector = list(xdata.values)
    yvector = [list(df[ycol].values)]

    training_inputs = np.array(xvector)
    training_outputs = np.array(yvector).T

    model.train(training_inputs,training_outputs,iterations)

    return model

def data_prep_widget():

    with st.expander("Format your data"):

        steps_done = [False,False,False]

        def clear_steps():
            steps_done = [False,False,False]

        def update_step(step,value):
            steps_done[step] = value

        cols = st.columns(4)
        block0 = cols[0].empty()
        block1 = cols[1].empty()
        block2 = cols[2].empty()
        block3 = cols[3].empty()

        with block0.container():
            #st.write(steps_done)

            uploaded_file = st.file_uploader("Choose a file",on_change=clear_steps)
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                data = data.fillna(0)
                update_step(0,True)
            else:
                data = pd.read_csv("Data/sampledata/dummy.csv")
                st.warning("No File Uploaded using default data")
                update_step(0,True)

            #st.write(steps_done)

        def format_col_option_in_dropdown(col,df=data):
            format_string = "Title: {0} | Values: {1}"
            sample_of_values = list(df[col].unique())[:10]
            sample_of_values = str(sample_of_values).replace("[","")
            sample_of_values = sample_of_values.replace("]","")

            return format_string.format(col,sample_of_values)

        with block1.container():
            #st.write(steps_done)

            xcols = st.multiselect("Select the X Columns",data.columns, format_func=format_col_option_in_dropdown)
            st.info("Select your columns for your x vector, number columns are only supported")


            if(len(xcols) > 0):
                update_step(1,True)
            else:
                update_step(1,False)

            #st.write(steps_done)

        with block2.container():
            #st.write(steps_done)

            if(steps_done[1]):
                cols_left = [x for x in data.columns if x not in xcols]

                ycol = st.selectbox("Select your Y Column",cols_left,format_func=format_col_option_in_dropdown)
                st.info("Select your y column, number columns are only supported")
                update_step(2,True)

            else:
                ycol = st.selectbox("Select your Y Column",data.columns,disabled=True)
                st.error("Select at least one x column to proceed")
                update_step(2,False)

            #st.write(steps_done)

        with block3.container():
            if(steps_done[0] and steps_done[1] and steps_done[2]):
                model_name = st.text_input("Model Name")
                if(model_name != ""):
                    if st.button("Save Data & Create Model"):
                        st.session_state.models[model_name] = {"model": generate_perceptron_model(data,xcols,ycol)}
                        st.session_state.models[model_name]["data"] = data
                        st.session_state.models[model_name]["split"] = 1
                        st.session_state.models[model_name]["training_df"] = data
                        st.session_state.models[model_name]["testing_df"] = data
            else:
                model_name = st.text_input("Model Name",disabled=True)
                st.info("Finish all steps to finish model")

def data_inspector_widget():
    with st.expander("View your data structure"):
        model_selected = st.selectbox("Select a model ",st.session_state.models.keys())

        if(model_selected is not None):
            cols = st.columns([1,1,4])
            cols[0].write("Current Split")
            value_to_update = cols[0].empty()
            value_to_update.write(st.session_state.models[model_selected]["split"])
            split_data = cols[1].button("Split Data")
            split = cols[2].slider('Size of training dataset', 0.0, 1.0, .05)

            if(split_data):
                st.session_state.models[model_selected]["split"] = split
                value_to_update.write(st.session_state.models[model_selected]["split"])

                train, test = train_test_split(st.session_state.models[model_selected]["data"], test_size=1-st.session_state.models[model_selected]["split"])
                st.session_state.models[model_selected]["training_df"] = train
                st.session_state.models[model_selected]["testing_df"] = test

        if(model_selected is not None):
            model_i = st.session_state.models[model_selected]["model"]
            df = st.session_state.models[model_selected]["data"]
            train_df = st.session_state.models[model_selected]["training_df"]
            test_df = st.session_state.models[model_selected]["testing_df"]

            st.header("Original Data")
            og_data_col = st.columns([1,1,1])
            og_data_col[0].write("Raw Data")
            og_data_col[1].write("X Vector")
            og_data_col[2].write("Y Vector")
            og_data_col[0].write(df)
            og_data_col[1].write(df[model_i.xcols])
            og_data_col[2].write(df[model_i.ycol])

            st.header("Training Data")
            og_data_col = st.columns([1,1,1])
            og_data_col[0].write("Raw Data")
            og_data_col[1].write("X Vector")
            og_data_col[2].write("Y Vector")
            og_data_col[0].write(train_df)
            og_data_col[1].write(train_df[model_i.xcols])
            og_data_col[2].write(train_df[model_i.ycol])

            st.header("Testing Data")
            og_data_col = st.columns([1,1,1])
            og_data_col[0].write("Raw Data")
            og_data_col[1].write("X Vector")
            og_data_col[2].write("Y Vector")
            og_data_col[0].write(test_df)
            og_data_col[1].write(test_df[model_i.xcols])
            og_data_col[2].write(test_df[model_i.ycol])

def train_model_widget():
    with st.expander("Train your model"):
        model_selected = st.selectbox("Select a model",st.session_state.models.keys())

        if(model_selected is not None):
            model_i = st.session_state.models[model_selected]["model"]
            df = st.session_state.models[model_selected]["training_df"]
            with st.form("Training"):

                st.header("Train your model")
                st.info("Hit train to reset the model and retrain it the number you specify")

                training_cols = st.columns(2)
                training_iterations = training_cols[1].number_input("Rounds of training",value=10,step=1)

                running_weight_change = []

                if training_cols[0].form_submit_button("Train"):
                    for i in range(training_iterations):
                        model = train_model_with_data(df, model_i, 1)


                col_names = []
                for col_i in range(len(model_i.xcols)):
                    temp_title = "W-"+model_i.xcols[col_i]
                    col_names.append(temp_title)
                col_names.append("Total Error")
                col_names.append("Accuracy")


                weight_df = pd.DataFrame(model_i.training_history,columns=col_names)
                training_cols[1].line_chart(weight_df["Accuracy"])

                training_cols[0].write(weight_df)

def view_results_widget():
    with st.expander("View Model Results"):
        model_selected = st.selectbox("Select a model  ",st.session_state.models.keys())

        if(model_selected is not None):
            model_i = st.session_state.models[model_selected]["model"]
            df = st.session_state.models[model_selected]["testing_df"]
            st.header("Training Results")
            results_df, accuracy, sum_error = get_scores_for_data(df, model_i)

            st.write("Accuracy: ",accuracy)
            st.write("Total Error: ",sum_error)
            st.write("Avg Error: ",sum_error/len(results_df))


            if(sum_error > 0):
                st.write("Under-estimating for postive values")
            else:
                st.write("Over-estimating for negative values")

            st.write("Iterations: ", model_i.iterations)

            weight_importance = sum(abs(model_i.synaptic_weights).flatten().tolist())/len(model_i.xcols)

            for col in range(len(model_i.xcols)):

                col_title = model_i.xcols[col]
                col_weight = model_i.synaptic_weights.flatten().tolist()[col]
                col_importance = abs(col_weight) >= weight_importance

                if(col_importance):
                    st.write(col_title,col_weight,col_importance)




            result_cols = st.columns(2)
            result_cols[0].write(results_df)

            result_cols[1].line_chart(data=results_df[["Actual_Y","Predicted_Y"]],x="Predicted_Y",y="Actual_Y")

def side_bar_function():
    page = st.sidebar.radio("Page",["Model Builder","Demo"])
    if(page == "Model Builder"):
        model_builder()
    elif(page == "Demo"):
        demo()
st.set_page_config(
page_title="Perceptron Demo App",
page_icon="🧊",
layout="wide",
initial_sidebar_state="collapsed",
)


session_state_vars_for_app()

def demo():
    st.title("Perceptron Demo")

    controls = st.columns(8)

    linear_samples = controls[0].slider("N Samples",10,2000,step =100,value=200)
    linear_classes = controls[1].slider("Linear Classes",1,5,step=1,value=2)
    linear_noise = controls[2].slider("Linear Noise",0.0,1.0,step=.05,value=.05)

    circular_samples = controls[4].slider("N Circular Samples",10,2000,step =100,value=200)
    circular_noise = controls[6].slider("Circular Noise",0.0,1.0,step=.05,value=.05)
    circular_scale = controls[5].slider("Circular Scale",.05,1.0,step=.05,value=.7)

    linear_side, circular_side = st.columns(2)

    X, y = make_classification(
    n_features=2,
    n_classes=linear_classes,
    n_samples=linear_samples,
    n_redundant=0,flip_y=linear_noise,
    n_clusters_per_class=1)

    X2, y2 = make_circles(n_samples=circular_samples, noise=circular_noise, factor=circular_scale)

    linear_data = pd.DataFrame(X,columns=["X","Y"])
    linear_data["X2"] = linear_data["X"] * linear_data["X"]
    linear_data["Y2"] = linear_data["Y"] * linear_data["Y"]
    linear_data["XY"] = linear_data["X"] * linear_data["Y"]
    linear_data["X/Y"] = linear_data["X"] / linear_data["Y"]
    linear_data["Y/X"] = linear_data["X"] / linear_data["Y"]


    linear_data["Z"] = y

    circular_data = pd.DataFrame(X2,columns=["X","Y"])
    circular_data["X2"] = circular_data["X"] * circular_data["X"]
    circular_data["Y2"] = circular_data["Y"] * circular_data["Y"]
    circular_data["XY"] = circular_data["X"] * circular_data["Y"]
    circular_data["X/Y"] = circular_data["X"] / circular_data["Y"]
    circular_data["X2+Y2"] = circular_data["X2"]+circular_data["Y2"]
    circular_data["sqrt(X2+Y2"] =    np.sqrt(circular_data["X2+Y2"] )

    circular_data["Z"] = y2

    fig_lin = px.scatter(
        linear_data,
        x="X",
        y="Y",
        color="Z",color_continuous_scale=px.colors.sequential.Bluered
    )
    fig_lin.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
    )

    fig_cir = px.scatter(
        circular_data,
        x="X",
        y="Y",
        color="Z",color_continuous_scale=px.colors.sequential.Bluered
    )
    fig_cir.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
    )

    linear_side.write(fig_lin)
    circular_side.write(fig_cir)

    sel_x_lin = linear_side.multiselect("X cols for lin",["X","Y","X2","Y2","XY","X/Y","Y/X"])
    sel_x_cir = circular_side.multiselect("X cols for cir",["X","Y","X2","Y2","XY", "X/Y","X2+Y2","sqrt(X2+Y2"])

    lin_training = linear_side.slider("Lin iterations",100,5000,100)
    cir_training = circular_side.slider("cir iterations",100,5000,100)

    linear_model = generate_perceptron_model(linear_data,sel_x_lin,"Z",lin_training)
    circular_model = generate_perceptron_model(circular_data,sel_x_cir,"Z",cir_training)

    linear_results = get_scores_for_data(linear_data,linear_model)
    circular_results = get_scores_for_data(circular_data,circular_model,.4)

    linear_side.write(linear_results[1])
    circular_side.write(circular_results[1])
    circular_side.write(circular_results[0])


    lin_col_names = []
    for col_i in range(len(linear_model.xcols)):
        temp_title = "W-"+linear_model.xcols[col_i]
        lin_col_names.append(temp_title)
    cir_col_names = []
    for col_i in range(len(circular_model.xcols)):
        temp_title = "W-"+circular_model.xcols[col_i]
        cir_col_names.append(temp_title)

    linear_weights = pd.DataFrame(linear_model.synaptic_weights.flatten().tolist())
    linear_weights["Name"] = lin_col_names
    linear_side.write(linear_weights)

    fig_lin = px.scatter(
        linear_results[0],
        x="X",
        y="Y",
        color="Predicted_Y",color_continuous_scale=px.colors.sequential.Bluered
    )
    fig_lin.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
    )

    fig_cir = px.scatter(
        circular_results[0],
        x="X",
        y="Y",
        color="Predicted_Y",color_continuous_scale=px.colors.sequential.Bluered
    )
    fig_cir.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
    )

    circular_weights = pd.DataFrame(circular_model.synaptic_weights.flatten().tolist())
    circular_weights["Name"] = cir_col_names
    circular_side.write(circular_weights)

    linear_side.write(fig_lin)
    circular_side.write(fig_cir)

def model_builder():
    data_prep_widget()
    data_inspector_widget()
    train_model_widget()
    view_results_widget()

# side_bar_models()
side_bar_function()
