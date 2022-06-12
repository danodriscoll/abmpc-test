# Studio: ABMPC-TEST
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Must be called first.
st.set_page_config(
    layout="wide", # 'centered' or 'wide'
    page_title='ABMPC-TEST',
    menu_items={
        'About': "This is a shareable data application. Visit https://www.transmissionvamp.com."
    }
)

header = st.container()
dataset = st.container()
model = st.container()
footer = st.container()

with header:
    st.title('Agent-Based Model Portfolio Choice: Test Ouput')
    st.subheader("The Puzzling Impact of Interest Rates")
    st.write(' "... It follows, in contrast to what most students of principles of economics are taught, that higher interest rates generate more economic activity, not less. Unless high interest rates have a detrimental impact on some components of aggregate demand."')
    st.caption("Godley, W & Lavoie, M, Monetary Economics: An Integrated Approach to Credit, Money, Income, Production and Wealth, p. 114")
    st.markdown("---")

    option = st.selectbox(
        'Select Test Output:',
        ('0% Interest on Government Bills Issued', '2.5% Interest on Government Bills Issued', '2.5% to 3.5% Bills (@Step 90)', '2.5% to 1.5% Bills (@Step 90)'))

with dataset:
    data_url = ('https://danodriscoll.github.io/abmpc-test/abmpc-test-01.csv')

    if option == "0% Interest on Government Bills Issued":
        data_url = "https://danodriscoll.github.io/abmpc-test/abmpc-test-01.csv"
    elif option == "2.5% Interest on Government Bills Issued":
        data_url = "https://danodriscoll.github.io/abmpc-test/abmpc-test-02.csv"
    elif option == "2.5% to 3.5% Bills (@Step 90)":
        data_url = "https://danodriscoll.github.io/abmpc-test/abmpc-test-03.csv"
    elif option == "2.5% to 1.5% Bills (@Step 90)":
        data_url = "https://danodriscoll.github.io/abmpc-test/abmpc-test-04.csv"    
    
    @st.cache
    def load_data(steps):
        data = pd.read_csv(data_url, nrows=steps)
        return data

with model:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chart Options")
        st.text("Hover over the chart for options. 'View fullscreen' and unselect / select legend categories.")

    with col2:
        stepsDefault = 170 # Default number of steps to show.
        steps = st.slider("Model Steps", min_value=1, max_value=170, value=stepsDefault, step=2)

    # Load data.
    df = load_data(steps)

    goFig = go.Figure()
    goFig.add_trace(go.Scatter(x=df.Step, y=df.national_income,
        mode='lines+markers',
        name='National Income'
    ))
    goFig.add_trace(go.Scatter(x=df.Step, y=df.disposable_income,
        mode='lines+markers',
        name='Disposable Income'
    ))
    goFig.add_trace(go.Scatter(x=df.Step, y=df.consumption,
        mode='lines+markers',
        name='Consumption'
    ))
    goFig.add_trace(go.Scatter(x=df.Step, y=df.bills_issued,
        mode='lines+markers',
        name='Bills Issued'
    ))    
    goFig.add_trace(go.Scatter(x=df.Step, y=df.fiscal_balance,
        mode='lines+markers',
        name='Fiscal Balance'
    ))

    goFig.update_layout(
        margin=dict(l=50,r=50,b=50,t=50),
        template="gridon",
        xaxis_title="Model Steps",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Monetary Units',
            titlefont_size=16,
            tickfont_size=14,
        ),        
        showlegend=True,
        legend_title="Macro Indicators",
        title=go.layout.Title(
            text="Steady State Economy: " + option,
            xref="paper",
            xanchor="center",
            yanchor="top"
        ),
        height=700
    )

    st.plotly_chart(goFig, use_container_width=True, sharing='streamlit')


with footer:
    st.caption("View a list of [data apps](https://share.streamlit.io/danodriscoll/transvamp-apps/main/app.py). Visit the [TransmissionVamp](https://www.transmissionvamp.com) website.")