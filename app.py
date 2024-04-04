import pandas as pd
import numpy as np
import streamlit as st
import streamlit_authenticator as stauth
import plotly.express as px
from auth import register, login
from database import create_comment, fetch_all_comments, fetch_all_users

st.set_page_config(page_title="Climate Change in Africa",
                   page_icon="🌍", layout="wide")
st.title("🌍 Temperature and CO2 Emission Trends in Africa")
st.markdown(
    '<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Put sign up and login in expander
register_expander = st.expander("Register (optional)")
login_expander = st.expander("Login (optional)")

with register_expander:
    register()
with login_expander:
    login()

col1, col2 = st.columns([1, 1])


@st.cache_data
def load_data():
    temp_df = pd.read_csv("data/Africa_Avg_Temperature_1960-2013.csv")
    co2_df = pd.read_csv("data/Africa_CO2_Emissions_1960-2018.csv")
    return co2_df, temp_df


co2_df, temp_df = load_data()

filtered_temp_df, filtered_co2_df = temp_df.copy(), co2_df.copy()


# Melt Temp data to reshape it
melted_temp_df = pd.melt(temp_df, id_vars=['Country', 'Region'],
                         var_name='Year', value_name='Temperature')
melted_temp_df['Year'] = pd.to_numeric(melted_temp_df['Year'])

# Melt CO2 data to reshape it
melted_co2_df = pd.melt(co2_df, id_vars=['Country', 'Region'],
                        var_name='Year', value_name='Emission')
melted_co2_df['Year'] = pd.to_numeric(melted_co2_df['Year'])


def commenter(chart_tag):
    with st.expander("Comment"):
        # Text area to input comments
        new_comment = st.text_area(
            "Add your comment:", key=chart_tag + 'comment')

        # Button to submit comment
        if st.button("Submit", key=chart_tag + 'button'):
            try:
                comment = create_comment(
                    new_comment, st.session_state["username"], chart_tag)
            except Exception as e:
                st.error("Please Login Again to Comment")
                return
        # Display previous comments
        previous_comments = fetch_all_comments(chart_tag)
        if previous_comments:
            st.write("**:green[Comments]**")
            for comment in previous_comments:
                username = comment["username"]
                comment = comment["comment"]
                st.write(username + ':', comment)


def plot_filterable_highest_temp():
    global filtered_temp_df, filtered_co2_df
    with col1:
        chart_tag = 'filterable_highest_temp'

        st.subheader('Countries with High Temperature')

        region = st.selectbox(
            "Select a Region", temp_df["Region"].unique(), index=None, key="temp_region")
        if region:
            filtered_temp_df = temp_df[temp_df["Region"] == region]
            filtered_co2_df = co2_df[co2_df["Region"] == region]

        fig1 = px.bar(filtered_temp_df.nlargest(10, "1960"), x="Country",
                      y="1960", title="Average temperature 1960 to 2013")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("""
            <style>
            .info {
                color: black;
                # background-color: #1F51FF;
                margin-top: 0px;
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            </style>
            <div class="info">
                Filterable by region, this chart shows the countries with the highest average temperature in Africa from 1960 to 2013.
            </div>
            """, unsafe_allow_html=True)
        # display comment
        commenter(chart_tag)

    with col2:
        st.subheader('Countries with High CO2 Emission')
        chart_tag = 'filterable_highest_co2'

        region = st.selectbox(
            "Select a Region", temp_df["Region"].unique(), index=None, key="co2_region")
        if region:
            filtered_temp_df = temp_df[temp_df["Region"] == region]
            filtered_co2_df = co2_df[co2_df["Region"] == region]

        fig2 = px.bar(filtered_co2_df.nlargest(10, "1960"), x="Country",
                      y="1960", title="Highest CO2 emissions 1960 to 2018")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("""
            <style>
            .info {
                color: black;
                # background-color: #1F51FF;
                margin-top: 0px;
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
            </style>
            <div class="info">
                Filterable by region, this chart shows the countries with the highest CO2 emissions in Africa from 1960 to 2018.
            </div>
            """, unsafe_allow_html=True)

        # display comment
        commenter(chart_tag)


def plot_regional_c02_contribution():
    st.subheader('Regional Temperature Contribution')
    chart_tag = 'regional_temp_contribution'

    fig = px.pie(temp_df, names="Region",
                 title="Region Wise Temperature (°C)", hole=0.5)
    fig.update_traces(text=temp_df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <style>
    .info {
        color: black;
        # background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        Western Africa has the highest temperature contribution in Africa, 
        followed by Eastern Africa, and Central Africa.
    </div>
    """, unsafe_allow_html=True)

    # display comment
    commenter(chart_tag)


def plot_avg_regional_temp():
    st.subheader('Average Regional Temperature')
    chart_tag = 'avg_regional_temp'
    avg_temp_by_region = melted_temp_df.groupby(
        'Region')['Temperature'].mean().reset_index()
    fig = px.bar(avg_temp_by_region, x='Region', y='Temperature',
                 title='Average Regional Temperature(1960-2013)',
                 labels={'Temperature': 'Average Temperature (°C)'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <style>
    .info {
        color: black;
        # background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        This chart shows the average temperature of each region in Africa from 1960 to 2013.
    </div>
    """, unsafe_allow_html=True)
    # display comment
    commenter(chart_tag)


def plot_avg_regional_temp_time_series():
    st.subheader('Regional Temperature Time Series')
    chart_tag = 'regional_temp_time_series'
    avg_temp_by_region_year = melted_temp_df.groupby(['Year', 'Region'])[
        'Temperature'].mean().reset_index()
    fig = px.line(avg_temp_by_region_year, x='Year', y='Temperature', color='Region',
                  title='Time Series - Average Regional Temperature(1960-2013)',
                  labels={'Temperature': 'Average Temperature (°C)', 'Year': 'Year'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <style>
    .info {
        color: black;
        # background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        This chart shows the time series of the average temperature of each region in Africa from 1960 to 2013.
    </div>
    """, unsafe_allow_html=True)
    # display comment
    commenter(chart_tag)


def plot_avg_regional_co2_emission_time_series():
    st.subheader('Regional CO2 Emission Time Series')
    chart_tag = 'regional_co2_emission_time_series'
    avg_emission_by_region_year = melted_co2_df.groupby(['Year', 'Region'])[
        'Emission'].mean().reset_index()
    fig = px.line(avg_emission_by_region_year, x='Year', y='Emission', color='Region',
                  title='Time Series - Average Regional CO2 Emission(1960-2018)',
                  labels={'Emission': 'Average CO2 Emission (Mt CO2)', 'Year': 'Year'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <style>
    .info {
        color: black;
        # background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        This chart shows the time series of the average CO2 Emission of each region in Africa from 1960 to 2013.
        Southern Africa showed a sharp increase in CO2 in 1961 which was followed by a sharp decrease in 1963.
    </div>
    """, unsafe_allow_html=True)
    # display comment
    commenter(chart_tag)


def plot_average_regional_co2_and_temp():
    st.subheader(' Regional Temperature & CO2 Emission')
    chart_tag = 'avg_regional_temp_co2'
    avg_temp_by_region = melted_temp_df.groupby(
        'Region')['Temperature'].mean().reset_index()
    avg_co2_by_region = melted_co2_df.groupby(
        'Region')['Emission'].mean().reset_index()

    avg_co2_by_region['Emission'] *= 10

    merged_data = pd.merge(avg_temp_by_region, avg_co2_by_region, on='Region')

    merged_data_melted = pd.melt(
        merged_data, id_vars='Region', var_name='Type', value_name='Value')

    fig = px.bar(merged_data_melted, x='Region', y='Value', color='Type',
                 barmode='group',
                 labels={'Value': 'Average Value', 'Region': 'Region'},
                 title='Average Regional Temperature (°C) and CO2 (Mt CO2 x10) Emission by Region',
                 facet_col_wrap=2, color_discrete_map={'Temperature': 'red', 'Emission': 'black'})
    st.plotly_chart(fig)
    st.markdown("""
    <style>
    .info {
        color: black;
        # background-color: #1F51FF;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info"> This chart show the average regional temperature and CO2 emission. 
    The CO2 emission value is multiplied by 10 for better visualization.
    </div>
    """, unsafe_allow_html=True)
    # display comment
    commenter(chart_tag)


def plot_temp_map():
    st.subheader('Countries Temperature Map')
    chart_tag = 'countries_temp_map'
    df_temp_melted = melted_temp_df.copy()

    years_list = range(1960, 2014, 5)
    selected_year = st.selectbox(
        'Select a specific year (5-year intervals)', years_list)

    avg_temp_selected_year = df_temp_melted[df_temp_melted['Year']
                                            == selected_year]

    avg_temp_by_country = avg_temp_selected_year.groupby(
        'Country')['Temperature'].mean().reset_index()

    fig = px.choropleth(avg_temp_by_country, locations='Country', locationmode='country names',
                        color='Temperature', scope='africa',
                        color_continuous_scale='hot_r', range_color=(avg_temp_by_country['Temperature'].min(), avg_temp_by_country['Temperature'].max()),
                        labels={'Temperature': 'Average Temperature (°C)'},
                        title=f'Average Temperature of Each Country in Africa for the Year {selected_year}', height=700)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <style>
    .info {
        color: black;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        This map shows the average temperature contribution of countries in Africa for the selected year.
    </div>
    """, unsafe_allow_html=True)

    # display comment
    commenter(chart_tag)


def plot_emission_map():
    st.subheader('Regional CO2 Emission Map')
    chart_tag = 'emission_map'
    df_emission_melted = melted_co2_df.copy()

    years_list = range(1960, 2018, 5)
    selected_year = st.selectbox(
        'Select a specific year (5-year intervals)', years_list, key='emission_map')

    avg_emission_selected_year = df_emission_melted[df_emission_melted['Year']
                                                    == selected_year]

    avg_temp_by_country = avg_emission_selected_year.groupby(
        'Country')['Emission'].mean().reset_index()

    fig = px.choropleth(avg_temp_by_country, locations='Country', locationmode='country names',
                        color='Emission', scope='africa',
                        color_continuous_scale='blackbody_r', range_color=(avg_temp_by_country['Emission'].min(), avg_temp_by_country['Emission'].max()),
                        labels={'Emission': 'Average Emission (°C)'},
                        title=f'Average Emission of Each Country in Africa for the Year {selected_year}', height=700)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <style>
    .info {
        color: black;
        margin-top: 0px;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    <div class="info">
        This map shows the average CO2 emission contribution of countries in Africa for the selected year.
    </div>
    """, unsafe_allow_html=True)
    # display comment
    commenter(chart_tag)


with col1:
    plot_regional_c02_contribution()
    plot_temp_map()


with col2:
    plot_average_regional_co2_and_temp()
    plot_emission_map()


plot_filterable_highest_temp()

plot_avg_regional_co2_emission_time_series()
plot_avg_regional_temp_time_series()

plot_avg_regional_temp()
