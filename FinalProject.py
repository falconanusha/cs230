"""
Name:   Anusha Patel
CS230:  Section SN5
Data:   Earthquake
URL:

Description: This program helps present the data on earthquakes derived from a csv file. For example, it presents a
line plot.
"""
import streamlit as st
import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd

# set text document with earthquake data
filename = "earthquakes_us_20201123.csv"


def lineplot(dates, yval):
    plt.plot(dates, yval, color='c')
    plt.title("Magnitudes Over Time")
    plt.xlabel("Time from September to November (2020)")
    plt.ylabel("Magnitudes")
    plt.yticks([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    return plt


def piechart(data, chart_labels):
    fig, ax = plt.subplots()
    ax.axis('equal')
    ax.pie(data, labels=chart_labels, autopct='%1.1f%%')
    plt.title("How were the earthquakes processed?")
    return plt


def main():
    st.title("Anusha Patel's Final Project")
    st.sidebar.header('Inputs')

    # Using DataFrame to gather data
    df = pd.read_csv(filename, usecols=["time", "latitude", "longitude", "depth", "mag", "magType", "nst", "gap",
                                        "dmin", "rms", "net", "id", "updated", "place", "type", "horizontalError",
                                        "depthError", "magError", "magNst", "status", "locationSource", "magSource"])
    # gathering data for sidebar radio
    maxMags = df["mag"].max()
    meanMag = df["mag"].mean()
    medianMag = df["mag"].sort_values().median()  # sort values in order to find a median
    stdevMag = statistics.stdev(df["mag"])
    # dictionary with values showing which sentences can be displayed on streamlit
    data = {"Maximum": f"The maximum magnitude is {maxMags}.", "Mean": f"The average magnitude is {meanMag:.2f}.",
            "Median": f"The median magnitude is {medianMag}.", "Standard Deviation": f"The standard deviation of \
            magnitudes is {stdevMag:.2f}."}
    data_names = list(data.keys())
    selection = st.sidebar.radio('Choose what magnitude to display:', data_names)
    # use radio in order for user to select the data that they want to see
    st.write(data[selection]) # displays whichever selection is chosen

    # use pandas to create a bar plot and display it through streamlit
    st.header("Average Magnitudes for Automatic vs. Reviewed")
    barplot = pd.pivot_table(df, index=['status'], values=['mag'], aggfunc=np.mean)
    barplot.plot(kind='bar')
    st.bar_chart(barplot)

    # helps gather data for line plot
    with open(filename, "r", encoding='utf-8') as csv_file:
        # convert magnitudes to list
        data = csv.DictReader(csv_file)
        # lists created for line plot
        magnitudes = []
        datelist = []
        # keeps count for pie chart (automatic, reviewed, and deleted)
        automatic = 0
        reviewed = 0
        deleted = 0
        for row in data:
            mag_read = float(row["mag"])
            magnitudes.append(mag_read)
            datelist.append(row["time"])  # convert date to real dates?
            # print(row["status"])
            if str(row["status"]) == "automatic":
                automatic += 1
            elif str(row["status"]) == "reviewed":
                reviewed += 1
            else:
                deleted += 1
        st.pyplot(lineplot(datelist, magnitudes))
        # st.pyplot shows line plot in browser instead of using plt.show()

        # gathering data for pie chart
        piechart_labels = ["Automatic", "Reviewed"]
        piechart_vals = [automatic, reviewed]
        st.pyplot(piechart(piechart_vals, piechart_labels))  # displays pie chart in browser


main()
