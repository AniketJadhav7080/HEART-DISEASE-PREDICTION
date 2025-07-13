import streamlit as st
import os
import sys
from Ecg_fixed import ECG

# Set page config
st.set_page_config(
    page_title="Heart Disease Prediction using ECG Images",
    page_icon="❤️",
    layout="wide"
)

# Add title and description
st.title("❤️ Heart Disease Prediction using ECG Images")
st.markdown("""
This application analyzes ECG images to predict heart conditions including:
- **Normal ECG**
- **Myocardial Infarction** 
- **Abnormal Heartbeat**
- **History of Myocardial Infarction**

Upload an ECG image to get started!
""")

# Initialize ECG object
try:
    ecg = ECG()
    st.success("✅ ECG analysis system loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading ECG system: {e}")
    st.stop()

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

        # Process the image
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

# Add footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔬 This application uses machine learning to analyze ECG images for educational and research purposes.</p>
    <p>⚠️ <strong>Medical Disclaimer:</strong> This tool is not a substitute for professional medical diagnosis.</p>
</div>
""", unsafe_allow_html=True) 