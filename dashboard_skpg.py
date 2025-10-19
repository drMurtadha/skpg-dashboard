import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Dashboard SKPG-MyMoheS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    try:
        # Try with different encodings
        df = pd.read_csv('Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv', encoding='latin-1')
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv', encoding='ISO-8859-1')
            return df
        except UnicodeDecodeError:
            try:
                df = pd.read_csv('Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv', encoding='cp1252')
                return df
            except UnicodeDecodeError as e:
                st.error(f"Could not read the file. Encoding error: {e}")
                return None
            
# Load data
@st.cache_data
def load_data():
    try:
        # Try with different encodings
        df = pd.read_csv('Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv', encoding='latin-1')
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv', encoding='ISO-8859-1')
            return df
        except UnicodeDecodeError:
            try:
                df = pd.read_csv('Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv', encoding='cp1252')
                return df
            except UnicodeDecodeError as e:
                st.error(f"Could not read the file. Encoding error: {e}")
                return None

# ✅ ADD THIS PART - Call the function and handle errors
df = load_data()

# Check if data loaded successfully
if df is None:
    st.error("❌ Failed to load data file. Please check:")
    st.info("1. The file 'Data SKPG-MyMoheS_UTM_Prototaip_v2(SKPG).csv' exists in the same folder")
    st.info("2. The file is not corrupted")
    st.info("3. The file is a valid CSV file")
    st.stop()  # Stop the app if data isn't loaded

# ✅ ADD THIS TO SHOW DATA LOADED SUCCESSFULLY
st.success(f"✅ Data loaded successfully! Shape: {df.shape}")

# Sidebar
st.sidebar.title("Navigasi Dashboard")
st.sidebar.markdown("---")

# Main title
st.title("📊 Dashboard Analisis Data SKPG-MyMoheS")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview", 
    "🎓 Profil Lulusan", 
    "💼 Status Pekerjaan", 
    "💰 Analisis Pendapatan", 
    "📋 Data Lengkap"
])

with tab1:
    st.header("Overview Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_graduates = len(df)
        st.metric("Total Lulusan", f"{total_graduates:,}")
    
    with col2:
        employed = df[df['status_pekerjaan_skpg'] == 'Bekerja'].shape[0]
        employment_rate = (employed / total_graduates) * 100
        st.metric("Tingkat Pekerjaan", f"{employment_rate:.1f}%")
    
    with col3:
        avg_cgpa = df[df['e_cgpa'] > 0]['e_cgpa'].mean()
        st.metric("Rata-rata CGPA", f"{avg_cgpa:.2f}")
    
    with col4:
        institutions_count = df['institusi_skpg'].nunique()
        st.metric("Jumlah Institusi", institutions_count)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution by institution type
        institusi_counts = df['jenis_ipt_skpg'].value_counts()
        fig = px.pie(
            values=institusi_counts.values,
            names=institusi_counts.index,
            title="Distribusi Jenis Institusi"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Graduation year distribution
        tahun_counts = df['tahun_konvo'].value_counts().sort_index()
        fig = px.bar(
            x=tahun_counts.index,
            y=tahun_counts.values,
            title="Distribusi Tahun Konvokesyen",
            labels={'x': 'Tahun', 'y': 'Jumlah Lulusan'}
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Profil Lulusan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        gender_counts = df['jantina_skpg'].value_counts()
        fig = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Distribusi Jantina"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Education level distribution
        peringkat_counts = df['peringkat_pengajian_skpg'].value_counts()
        fig = px.bar(
            x=peringkat_counts.values,
            y=peringkat_counts.index,
            orientation='h',
            title="Distribusi Peringkat Pengajian",
            labels={'x': 'Jumlah', 'y': 'Peringkat'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # CGPA distribution
    st.subheader("Distribusi CGPA")
    cgpa_data = df[df['e_cgpa'] > 0]['e_cgpa']
    fig = px.histogram(
        cgpa_data,
        nbins=20,
        title="Distribusi CGPA Lulusan",
        labels={'value': 'CGPA', 'count': 'Jumlah Lulusan'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Status Pekerjaan")
    
    # Employment status
    status_counts = df['status_pekerjaan_skpg'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Status Pekerjaan Lulusan"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Employment sector for those working
        employed_df = df[df['status_pekerjaan_skpg'] == 'Bekerja']
        if not employed_df.empty:
            sektor_counts = employed_df['Bekerja_sektor_pekerjaan_skpg'].value_counts().head(10)
            fig = px.bar(
                x=sektor_counts.values,
                y=sektor_counts.index,
                orientation='h',
                title="Top 10 Sektor Pekerjaan",
                labels={'x': 'Jumlah', 'y': 'Sektor'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Employment by institution
    st.subheader("Status Pekerjaan berdasarkan Institusi")
    employment_by_institution = df.groupby(['institusi_skpg', 'status_pekerjaan_skpg']).size().unstack(fill_value=0)
    fig = px.bar(
        employment_by_institution,
        title="Status Pekerjaan per Institusi",
        labels={'value': 'Jumlah', 'institusi_skpg': 'Institusi'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Analisis Pendapatan")
    
    # Filter hanya yang bekerja dan memiliki data pendapatan
    income_df = df[(df['status_pekerjaan_skpg'] == 'Bekerja') & 
                  (df['Bekerja_pendapatan_bulanan_skpg'] != 'Tidak Berkenaan')]
    
    if not income_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Income distribution
            income_counts = income_df['Bekerja_pendapatan_bulanan_skpg'].value_counts()
            fig = px.bar(
                x=income_counts.values,
                y=income_counts.index,
                orientation='h',
                title="Distribusi Pendapatan Bulanan",
                labels={'x': 'Jumlah', 'y': 'Pendapatan'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Income by education level
            income_by_edu = income_df.groupby('peringkat_pengajian_skpg')['Bekerja_pendapatan_bulanan_skpg'].value_counts().unstack(fill_value=0)
            fig = px.bar(
                income_by_edu,
                title="Pendapatan berdasarkan Peringkat Pengajian",
                labels={'value': 'Jumlah', 'peringkat_pengajian_skpg': 'Peringkat Pengajian'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Income vs CGPA analysis
        st.subheader("Hubungan Pendapatan dengan CGPA")
        
        # Create a simplified income mapping for analysis
        income_mapping = {
            'Kurang daripada RM1,000': 500,
            'RM1,000 dan ke bawah': 500,
            'RM1,000 - RM1,499': 1250,
            'RM1,501 – RM2,000': 1750,
            'RM2,000 - RM2,499': 2250,
            'RM2,500 - RM2,999': 2750,
            'RM3,000 - RM3,499': 3250,
            'RM3,500 - RM3,999': 3750,
            'RM4,000 - RM4,499': 4250,
            'RM4,500 - RM4,999': 4750,
            'RM5,000 - RM5,499': 5250,
            'RM5,500 - RM5,999': 5750,
            'RM6,000 - RM6,499': 6250,
            'RM6,500 - RM6,999': 6750,
            'RM7,000 - RM7,499': 7250,
            'RM7,500 - RM7,999': 7750,
            'RM8,000 - RM8,499': 8250,
            'RM8,500 - RM8,999': 8750,
            'RM9,000 - RM9,499': 9250,
            'RM9,500 - RM9,999': 9750
        }
        
        analysis_df = income_df.copy()
        analysis_df['income_numeric'] = analysis_df['Bekerja_pendapatan_bulanan_skpg'].map(income_mapping)
        analysis_df = analysis_df.dropna(subset=['income_numeric', 'e_cgpa'])
        analysis_df = analysis_df[analysis_df['e_cgpa'] > 0]
        
        if not analysis_df.empty:
            fig = px.scatter(
                analysis_df,
                x='e_cgpa',
                y='income_numeric',
                trendline="ols",
                title="Hubungan CGPA dengan Pendapatan",
                labels={'e_cgpa': 'CGPA', 'income_numeric': 'Pendapatan (RM)'}
            )
            st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Data Lengkap")
    
    # Filters
    st.subheader("Filter Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_institutions = st.multiselect(
            "Pilih Institusi:",
            options=df['institusi_skpg'].unique(),
            default=df['institusi_skpg'].unique()[:3] if len(df['institusi_skpg'].unique()) > 3 else df['institusi_skpg'].unique()
        )
    
    with col2:
        selected_status = st.multiselect(
            "Pilih Status Pekerjaan:",
            options=df['status_pekerjaan_skpg'].unique(),
            default=df['status_pekerjaan_skpg'].unique()
        )
    
    with col3:
        selected_years = st.multiselect(
            "Pilih Tahun Konvokesyen:",
            options=sorted(df['tahun_konvo'].unique()),
            default=sorted(df['tahun_konvo'].unique())
        )
    
    # Apply filters
    filtered_df = df[
        (df['institusi_skpg'].isin(selected_institutions)) &
        (df['status_pekerjaan_skpg'].isin(selected_status)) &
        (df['tahun_konvo'].isin(selected_years))
    ]
    
    st.subheader("Data Terfilter")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data sebagai CSV",
        data=csv,
        file_name="filtered_skpg_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    "**Dashboard SKPG-MyMoheS** | Data menunjukkan tren pekerjaan dan pencapaian lulusan institusi pendidikan tinggi Malaysia"
)