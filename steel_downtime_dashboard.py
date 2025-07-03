import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Custom CSS for gradient background and font color fixes
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 50%, #f44369 100%);
        backdrop-filter: blur(4px);
        color: black !important;
    }
    .block-container {
        background: rgba(255,255,255,0.7);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(6px);
        color: black !important;
    }
    h1, h2, h3, h4, h5, h6, label, .css-1cpxqw2, .css-1d391kg, .css-1v0mbdj, 
    .css-1offfwp, .css-1q8dd3e, .css-1l02zno, .css-1n76uvr, .css-1b0udgb, 
    .css-1v3fvcr, .css-1p05t8e, .css-1vzeuhh {
        color: black !important;
    }

    /* Fix white text in metric values */
    [data-testid="stMetricValue"] {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Steel Plant Downtime Analysis Dashboard')

# Load data
def load_data():
    df = pd.read_csv('steel_downtime_data.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Month'] = df['Timestamp'].dt.strftime('%Y-%m')
    df['Production_Loss_Tons'] = df['Production_Loss'].apply(lambda x: float(x.replace(' tons','')) if 'tons' in x else None)
    df['Production_Loss_INR'] = df['Production_Loss'].apply(lambda x: int(x.replace('₹','')) if '₹' in x else None)
    return df

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header('Filters')
    dept = st.multiselect('Department', options=sorted(df['Department'].unique()), default=list(df['Department'].unique()))
    month = st.multiselect('Month', options=sorted(df['Month'].unique()), default=list(df['Month'].unique()))
    machine = st.multiselect('Machine', options=sorted(df['Machine_ID'].unique()), default=list(df['Machine_ID'].unique()))
    shift = st.multiselect('Shift', options=sorted(df['Shift'].unique()), default=list(df['Shift'].unique()))

# Filter data
filtered = df[
    df['Department'].isin(dept) &
    df['Month'].isin(month) &
    df['Machine_ID'].isin(machine) &
    df['Shift'].isin(shift)
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric('Total Downtime Events', len(filtered))
col2.metric('Total Downtime (hrs)', round(filtered['Downtime_Minutes'].sum() / 60, 1))
col3.metric('Estimated Production Loss (tons)', round(filtered['Production_Loss_Tons'].sum(), 1))

# Downtime by Machine
st.subheader('Downtime by Machine')
fig1 = px.bar(
    filtered.groupby('Machine_ID')['Downtime_Minutes'].sum().reset_index(),
    x='Machine_ID', y='Downtime_Minutes',
    color='Downtime_Minutes',
    color_continuous_scale=["#f7971e", "#ffd200", "#f44369"],
    title='Total Downtime Minutes by Machine'
)
fig1.update_layout(plot_bgcolor='rgba(255,255,255,0.6)', paper_bgcolor='rgba(255,255,255,0.0)', font_color='black')
fig1.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
fig1.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
st.plotly_chart(fig1, use_container_width=True)

# Downtime by Reason
st.subheader('Downtime by Reason')
fig2 = px.pie(
    filtered, names='Downtime_Reason', values='Downtime_Minutes',
    color_discrete_sequence=["#f7971e", "#ffd200", "#f44369", "#a770ef", "#f5576c", "#ff5858", "#ff9a44", "#ff6a00", "#ffb347", "#ff5e62"],
    title='Downtime Distribution by Reason'
)
fig2.update_traces(
    textinfo='percent+label',
    pull=[0.05]*len(pd.Series(filtered['Downtime_Reason']).unique()),
    textfont=dict(color='black'),
    insidetextfont=dict(color='black'),
    outsidetextfont=dict(color='black')
)
fig2.update_layout(plot_bgcolor='rgba(255,255,255,0.6)', paper_bgcolor='rgba(255,255,255,0.0)', font_color='black')
fig2.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
fig2.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
st.plotly_chart(fig2, use_container_width=True)

# Monthly Downtime Trend
st.subheader('Monthly Downtime Trend')
trend = filtered.groupby('Month')['Downtime_Minutes'].sum().reset_index()
fig3 = px.line(
    trend, x='Month', y='Downtime_Minutes',
    markers=True,
    line_shape='spline',
    color_discrete_sequence=["#f44369"],
    title='Monthly Downtime Trend'
)
fig3.update_layout(plot_bgcolor='rgba(255,255,255,0.6)', paper_bgcolor='rgba(255,255,255,0.0)', font_color='black')
fig3.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
fig3.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
st.plotly_chart(fig3, use_container_width=True)

# Downtime Duration Histogram
st.subheader('Downtime Duration Distribution')
fig4 = px.histogram(
    filtered, x='Downtime_Minutes', nbins=30,
    color_discrete_sequence=["#f7971e"],
    title='Distribution of Downtime Durations (Minutes)'
)
fig4.update_layout(
    plot_bgcolor='rgba(255,255,255,0.6)',
    paper_bgcolor='rgba(255,255,255,0.0)',
    font_color='black',
    xaxis_title_font=dict(color='black'),
    yaxis_title_font=dict(color='black'),
    legend_font_color='black',
    title_font_color='black'
)
fig4.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
fig4.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
st.plotly_chart(fig4, use_container_width=True)

# Downtime by Department and Shift
st.subheader('High-risk Shifts and Departments')
highrisk = filtered.groupby(['Department', 'Shift'])['Downtime_Minutes'].sum().reset_index()
fig5 = px.bar(
    highrisk, x='Department', y='Downtime_Minutes', color='Shift',
    barmode='group',
    color_discrete_sequence=["#f7971e", "#ffd200", "#f44369"],
    title='Downtime by Department and Shift'
)
fig5.update_layout(plot_bgcolor='rgba(255,255,255,0.6)', paper_bgcolor='rgba(255,255,255,0.0)', font_color='black')
fig5.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
fig5.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
st.plotly_chart(fig5, use_container_width=True)
