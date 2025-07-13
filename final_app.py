import streamlit as st
import os
import sys
from Ecg_fixed import ECG
from login_system import check_authentication, show_user_dashboard
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Heart Disease Prediction using ECG Images",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main_app():
    """Main application after authentication"""
    
    # Get user info
    user = st.session_state.user
    
    # Main title with user info
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #ff6b6b, #4ecdc4); border-radius: 10px; margin-bottom: 2rem;'>
        <h1>❤️ Heart Disease Prediction using ECG Images</h1>
        <h3>Welcome back, {user['full_name']}! 👋</h3>
        <p>Analyze ECG images to predict heart conditions with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize ECG object
    try:
        ecg = ECG()
        st.success("✅ ECG analysis system loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading ECG system: {e}")
        st.stop()

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔬 ECG Analysis", "📊 Analysis History", "ℹ️ About"])
    
    with tab1:
        st.subheader("🔬 ECG Image Analysis")
        st.markdown("Upload an ECG image to analyze and predict heart conditions.")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an ECG image file", 
            type=["jpg", "jpeg", "png"],
            help="Upload an ECG image in JPG, JPEG, or PNG format"
        )

        if uploaded_file is not None:
            try:
                # Display uploaded image
                st.subheader("📸 **UPLOADED IMAGE**")
                ecg_user_image_read = ecg.getImage(uploaded_file)
                st.image(ecg_user_image_read, caption="Uploaded ECG Image", use_column_width=True)

                # Process the image with progress tracking
                with st.spinner("Processing ECG image..."):
                    # Convert to grayscale
                    st.subheader("🔍 **GRAY SCALE IMAGE**")
                    ecg_user_gray_image_read = ecg.GrayImgae(ecg_user_image_read)
                    
                    with st.expander("View Gray Scale Image"):
                        st.image(ecg_user_gray_image_read, caption="Grayscale ECG Image")

                    # Divide leads
                    st.subheader("📊 **DIVIDING LEADS**")
                    dividing_leads = ecg.DividingLeads(ecg_user_image_read)
                    
                    with st.expander("View Divided Leads"):
                        if os.path.exists('Leads_1-12_figure.png'):
                            st.image('Leads_1-12_figure.png', caption="12-Lead ECG")
                        if os.path.exists('Long_Lead_13_figure.png'):
                            st.image('Long_Lead_13_figure.png', caption="Long Lead 13")

                    # Preprocess leads
                    st.subheader("⚙️ **PREPROCESSED LEADS**")
                    ecg_preprocessed_leads = ecg.PreprocessingLeads(dividing_leads)
                    
                    with st.expander("View Preprocessed Leads"):
                        if os.path.exists('Preprossed_Leads_1-12_figure.png'):
                            st.image('Preprossed_Leads_1-12_figure.png', caption="Preprocessed 12-Lead ECG")
                        if os.path.exists('Preprossed_Leads_13_figure.png'):
                            st.image('Preprossed_Leads_13_figure.png', caption="Preprocessed Long Lead 13")

                    # Extract signals
                    st.subheader("📈 **EXTRACTING SIGNALS (1-12)**")
                    ec_signal_extraction = ecg.SignalExtraction_Scaling(dividing_leads)
                    
                    with st.expander("View Contour Leads"):
                        if os.path.exists('Contour_Leads_1-12_figure.png'):
                            st.image('Contour_Leads_1-12_figure.png', caption="Contour Extracted Signals")

                    # Convert to 1D signal
                    st.subheader("🔄 **CONVERTING TO 1D SIGNAL**")
                    ecg_1dsignal = ecg.CombineConvert1Dsignal()
                    
                    with st.expander("View 1D Signals"):
                        st.write("1D Signal Data Shape:", ecg_1dsignal.shape)
                        st.dataframe(ecg_1dsignal.head())

                    # Perform dimensionality reduction
                    st.subheader("📉 **PERFORM DIMENSIONALITY REDUCTION**")
                    ecg_final = ecg.DimensionalReduciton(ecg_1dsignal)
                    
                    with st.expander("View Dimensional Reduction"):
                        st.write("Reduced Data Shape:", ecg_final.shape)
                        st.dataframe(ecg_final.head())

                    # Make prediction
                    st.subheader("🔮 **PREDICTION RESULTS**")
                    ecg_model = ecg.ModelLoad_predict(ecg_final)
                    
                    # Save analysis to history
                    save_analysis_history(user['id'], uploaded_file.name, ecg_model)
                    
                    with st.expander("View Prediction", expanded=True):
                        # Display result with appropriate styling
                        if "Normal" in ecg_model:
                            st.success(f"🎉 **{ecg_model}**")
                        elif "Myocardial Infarction" in ecg_model:
                            st.error(f"⚠️ **{ecg_model}**")
                        elif "Abnormal Heartbeat" in ecg_model:
                            st.warning(f"⚠️ **{ecg_model}**")
                        else:
                            st.info(f"ℹ️ **{ecg_model}**")
                        
                        st.write("**Note:** This is an AI-assisted analysis. Please consult with a healthcare professional for medical diagnosis.")

            except Exception as e:
                st.error(f"❌ Error processing image: {e}")
                st.error("Please make sure you uploaded a valid ECG image file.")
                st.info("💡 **Tip:** Try uploading an image from the sample dataset in the ECG_IMAGES_DATASET folder.")

    with tab2:
        st.subheader("📊 Analysis History")
        show_analysis_history(user['id'])
    
    with tab3:
        st.subheader("ℹ️ About This Application")
        st.markdown("""
        ### 🔬 **Heart Disease Prediction using ECG Images**
        
        This application uses advanced machine learning techniques to analyze ECG (Electrocardiogram) images 
        and predict various heart conditions.
        
        #### **How it works:**
        1. **Image Upload**: Upload an ECG image in JPG, JPEG, or PNG format
        2. **Preprocessing**: Convert to grayscale, apply filters, and remove grid lines
        3. **Lead Division**: Extract 12 standard ECG leads plus 1 long lead
        4. **Signal Extraction**: Convert ECG waves to 1D signals using contour detection
        5. **Feature Engineering**: Apply dimensionality reduction using PCA
        6. **Prediction**: Use trained ML model to classify the ECG
        
        #### **Supported Conditions:**
        - ✅ **Normal ECG** - Healthy heart pattern
        - ⚠️ **Myocardial Infarction** - Heart attack indicators
        - ⚠️ **Abnormal Heartbeat** - Irregular heart rhythm
        - ℹ️ **History of Myocardial Infarction** - Previous heart attack evidence
        
        #### **Technical Stack:**
        - **Frontend**: Streamlit
        - **Image Processing**: scikit-image
        - **Machine Learning**: scikit-learn
        - **Data Processing**: pandas, numpy
        - **Authentication**: SQLite database
        
        #### **⚠️ Medical Disclaimer:**
        This tool is designed for educational and research purposes only. 
        It is not a substitute for professional medical diagnosis or treatment. 
        Always consult with qualified healthcare professionals for medical decisions.
        """)

def save_analysis_history(user_id, filename, prediction):
    """Save analysis history to database"""
    try:
        import sqlite3
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Create history table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename TEXT,
                prediction TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert analysis record
        cursor.execute('''
            INSERT INTO analysis_history (user_id, filename, prediction)
            VALUES (?, ?, ?)
        ''', (user_id, filename, prediction))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        st.error(f"Could not save analysis history: {e}")

def show_analysis_history(user_id):
    """Display user's analysis history"""
    try:
        import sqlite3
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Get analysis history
        cursor.execute('''
            SELECT filename, prediction, analysis_date
            FROM analysis_history 
            WHERE user_id = ?
            ORDER BY analysis_date DESC
            LIMIT 20
        ''', (user_id,))
        
        history = cursor.fetchall()
        conn.close()
        
        if history:
            st.markdown("### Recent Analyses")
            
            # Create DataFrame for better display
            df = pd.DataFrame(history, columns=['Filename', 'Prediction', 'Date'])
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Display with styling
            for idx, row in df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 2])
                    
                    with col1:
                        st.write(f"**{row['Filename']}**")
                    
                    with col2:
                        if "Normal" in row['Prediction']:
                            st.success(row['Prediction'])
                        elif "Myocardial Infarction" in row['Prediction']:
                            st.error(row['Prediction'])
                        elif "Abnormal Heartbeat" in row['Prediction']:
                            st.warning(row['Prediction'])
                        else:
                            st.info(row['Prediction'])
                    
                    with col3:
                        st.write(f"📅 {row['Date']}")
                    
                    st.markdown("---")
        else:
            st.info("No analysis history found. Upload an ECG image to get started!")
            
    except Exception as e:
        st.error(f"Could not load analysis history: {e}")

def main():
    """Main function"""
    # Check authentication
    if check_authentication():
        # Show user dashboard in sidebar
        show_user_dashboard()
        
        # Run main app
        main_app()
        
        # Add footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🔬 This application uses machine learning to analyze ECG images for educational and research purposes.</p>
            <p>⚠️ <strong>Medical Disclaimer:</strong> This tool is not a substitute for professional medical diagnosis.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 