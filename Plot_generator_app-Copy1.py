import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import io

st.title("Plot Selector App")
st.markdown("This is an app that you can use to display and download plots of different types as a .png file. Simply upload your (clean) dataset, choose your plot type and select the data to display in the plot. Then press the download button to download the plot.")
     
def file_uploader(key):
    uploaded_file = st.file_uploader(label="Upload your dataset", type=['csv', 'xlsx'], key=key)
    if uploaded_file:
        return pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    return None


def render_and_export(plot, label="Download Plot as PNG"):
    fig, ax = plt.subplots()
    plot(fig, ax)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button(label, data=buf, file_name="plot.png", mime="image/png")
    return fig


def boxplot(fig, ax):
    x_options = ['None'] + list(df.select_dtypes(include='object').columns)
    x_choice = st.selectbox("Select x variable", x_options)
    x = None if x_choice == 'None' else x_choice
    y = st.selectbox("Select y variable", df.select_dtypes(include=['int', 'float']).columns, key="y_var_box")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.boxplot(data=df, x=x, y=y, hue=hue, ax=ax)
    plt.title(f"Boxplot of {y} per {x}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")
    

def lineplot(fig, ax):
    x = st.selectbox("Select x variable", df.select_dtypes(include=['int', 'float', 'datetime']).columns, key="x_var_line")
    y = st.selectbox("Select y variable", df.select_dtypes(include=['int', 'float', 'datetime']).columns, key="y_var_line")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.lineplot(data=df, x=x, y=y, hue=hue, ax=ax, ci=None)
    plt.title(f"Line plot of {y} vs. {x}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")

def scatterplot(fig, ax):
    x = st.selectbox("Select x variable", df.select_dtypes(include=['int', 'float', 'datetime']).columns, key="x_var_scatter")
    y = st.selectbox("Select y variable", df.select_dtypes(include=['int', 'float', 'datetime']).columns, key="y_var_scatter")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.scatterplot(data=df, x=x, y=y, hue=hue, ax=ax)
    plt.title(f"Scatterplot of {y} vs. {x}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")

def countplot(fig, ax):
    x = st.selectbox("Select x variable", df.select_dtypes(include='object').columns, key="x_var_count")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.countplot(data=df, x=x, hue=hue, ax=ax)
    plt.title(f"Countplot of {x}")
    plt.xlabel(f"{x}")

def histogram(fig, ax):
    x = st.selectbox("Select x variable", df.select_dtypes(include=['int', 'float', 'datetime']).columns, key="x_var_hist")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.histplot(data=df, x=x, hue=hue, ax=ax, kde=True, multiple='dodge', bins=len(x))
    plt.title(f"Histogram of {x}")
    plt.xlabel(f"{x}")

def barplot(fig, ax):
    x = st.selectbox("Select x variable", df.select_dtypes(include='object').columns, key="x_var_bar")
    y = st.selectbox("Select y variable", df.select_dtypes(include=['int', 'float']).columns, key="y_var_bar")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax)
    plt.title(f"Barplot of {y} per {x}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")

def violinplot(fig, ax):
    y = st.selectbox("Select x variable", df.select_dtypes(include='object').columns, key="x_var_violin")
    x = st.selectbox("Select y variable", df.select_dtypes(include=['int', 'float']).columns, key="y_var_violin")
    hue_options = ['None'] + list(df.select_dtypes(include='object').columns)
    hue_choice = st.selectbox("Select hue variable", hue_options)
    hue = None if hue_choice == 'None' else hue_choice
    sns.violinplot(data=df, x=x, y=y, hue=hue, ax=ax, inner='quartile')
    plt.title(f"Violin plot of {y} per {x}")
    plt.xlabel(f"{x}")
    plt.ylabel(f"{y}")

def correlation_heatmap(fig, ax):
    corr = df.corr(numeric_only=True)
    sns.heatmap(data=corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title("Correlation heatmap of df")    


plot_gen_key = 'plotgen.app'
df = file_uploader(plot_gen_key)

if df is not None:
    st.subheader("Original dataframe preview")
    st.dataframe(df.head())
    
    plot_selector = {'None' : None,
                     'Boxplot' : boxplot,
                     'Line Plot' : lineplot,
                     'Scatterplot' : scatterplot,
                     'Countplot' : countplot,
                     'Histogram' : histogram,
                     'Barplot' : barplot,
                     'Violin Plot' : violinplot,
                     'Correlation Heatmap' : correlation_heatmap
                    }
    
    selected_plot = st.selectbox("Select plot type", list(plot_selector.keys()))
    if plot_selector[selected_plot] is not None:
        render_and_export(plot_selector[selected_plot])
    else:
        st.info("Select a plot type to display.")
else:
    st.info("Upload a .csv or .xlsx file.")

    
