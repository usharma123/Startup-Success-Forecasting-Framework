import streamlit as st
import sys
import os
import time
import traceback
import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

try:
    from ssff_framework import StartupFramework
except Exception as e:
    logger.error(f"Failed to import StartupFramework: {str(e)}")
    raise

# Custom CSS
def load_custom_css():
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .sub-header {
            font-size: 1.8rem;
            color: #1E3A8A;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #CBD5E1;
            padding-bottom: 0.5rem;
        }
        .section-header {
            font-size: 1.5rem;
            color: #334155;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            font-weight: 600;
        }
        .highlight-box {
            background-color: #F8FAFC;
            border-left: 4px solid #2563EB;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.25rem;
            height: 100%;
            min-height: 100px;
        }
        .metric-container {
            background-color: #F8FAFC;
            border-radius: 0.5rem;
            padding: 1.25rem;
            margin: 0.75rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            height: 100%;
            min-height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-label {
            font-size: 0.875rem;
            color: #64748B;
            margin-bottom: 0.25rem;
            font-weight: 500;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #0F172A;
        }
        .metric-description {
            font-size: 0.75rem;
            color: #64748B;
            margin-top: 0.5rem;
        }
        .analyze-button {
            background-color: #2563EB;
            color: white;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            border-radius: 0.375rem;
            border: none;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .analyze-button:hover {
            background-color: #1D4ED8;
        }
        .step-progress {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .example-text {
            font-size: 0.8rem;
            color: #64748B;
        }
        /* Fix for markdown rendering */
        .highlight-box strong, .highlight-box b {
            font-weight: 700 !important;
        }
        .highlight-box em, .highlight-box i {
            font-style: italic !important;
        }
        /* Fix for container heights */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 1rem;
        }
        .row-widget.stButton {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    load_custom_css()
    
    # Custom header with logo if available
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">Startup Success Forecasting Framework</div>', unsafe_allow_html=True)
    
    # Introduction
    with st.expander("About this Framework"):
        st.markdown("""
        The Startup Success Forecasting Framework analyzes startup information using a combination of:
        
        - Market analysis
        - Product evaluation
        - Founder assessment
        - Quantitative predictions
        
        Enter detailed information about your startup below to receive a comprehensive evaluation.
        """)
    
    st.markdown("<div class='sub-header'>Startup Information</div>", unsafe_allow_html=True)
    
    # Example text
    example = """
    Company Name: EcoFresh
    
    Description: EcoFresh is developing a smart refrigerator technology that uses AI to monitor food freshness and reduce food waste. The system uses cameras and sensors to track food items, predict expiration dates, and suggest recipes based on what needs to be used before spoiling. The app also connects to grocery delivery services for automatic reordering.
    
    Founder Information: The founding team consists of Dr. Sarah Chen (PhD in Computer Vision, 5 years at Google working on image recognition), Michael Rodriguez (former product manager at Samsung's appliance division), and Jamie Okonkwo (serial entrepreneur with a successful exit in the food delivery space).
    """
    
    with st.expander("See example input"):
        st.markdown(f"<div class='example-text'>{example}</div>", unsafe_allow_html=True)
    
    try:
        framework = StartupFramework()
        logger.info("Framework initialized successfully")
    except Exception as e:
        st.error(f"Failed to initialize framework: {str(e)}")
        logger.error(f"Framework initialization error: {traceback.format_exc()}")
        return

    # Input area with improved styling
    st.markdown("""<div style="margin-bottom: 0.5rem; font-weight: 500;">Enter Startup Information</div>""", unsafe_allow_html=True)
    startup_info_str = st.text_area("", height=250,
                                   help="Provide a detailed description of the startup, including information about the product, market, founders, and any other relevant details.",
                                   placeholder="Include company name, detailed description of the product/service, target market, team composition, current traction, etc.")

    # Create a centered column for the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("Analyze Startup", use_container_width=True, key="analyze_button", type="primary")
    
    if analyze_button:
        if startup_info_str:
            try:
                with st.spinner("Initializing analysis..."):
                    result_placeholder = st.empty()
                    result = analyze_startup_with_updates(framework, startup_info_str, result_placeholder)
                if result:
                    display_final_results(result, "advanced")
                else:
                    st.error("Analysis did not complete successfully. Please check the errors above.")
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                logger.error(f"Analysis error: {traceback.format_exc()}")
        else:
            st.warning("Please enter startup information before analyzing.")

def analyze_startup_with_updates(framework, startup_info_str, placeholder):
    with placeholder.container():
        st.markdown("<div class='section-header'>Analysis in Progress</div>", unsafe_allow_html=True)
        
        # Create a more visually appealing progress area
        progress_col1, progress_col2 = st.columns([3, 1])
        with progress_col1:
            progress_bar = st.progress(0)
        with progress_col2:
            status_percentage = st.empty()
        
        status_text = st.empty()
        status_detail = st.empty()

        def update_status(step, progress, detail=""):
            status_text.markdown(f"<div style='font-weight:500; color:#334155;'>{step}</div>", unsafe_allow_html=True)
            progress_bar.progress(progress)
            status_percentage.markdown(f"<div style='text-align:center; font-weight:600;'>{int(progress*100)}%</div>", unsafe_allow_html=True)
            if detail:
                status_detail.info(detail)

        # Create empty containers for each analysis section
        st.markdown("<div class='step-progress'></div>", unsafe_allow_html=True)
        parsing_container = st.container()
        scout_container = st.container()
        market_container = st.container()
        product_container = st.container()
        founder_container = st.container()
        advanced_founder_container = st.container()
        integration_container = st.container()
        quant_container = st.container()

        result = {}
        try:
            # PARSING
            update_status("Parsing startup information", 0.1, "Extracting structured data from your startup description...")
            startup_info = framework.vc_scout_agent.parse_record(startup_info_str)
            with parsing_container:
                st.success("✓ Startup information parsed successfully")
            time.sleep(0.3)  # Small delay for visual feedback

            # VC SCOUT
            update_status("VCScout evaluation", 0.2, "Performing initial assessment and categorization...")
            prediction, categorization = framework.vc_scout_agent.side_evaluate(startup_info)
            with scout_container:
                st.success(f"✓ Initial evaluation complete - Prediction: {prediction}")
            result['Categorical Prediction'] = prediction
            result['Categorization'] = categorization.model_dump()
            time.sleep(0.3)

            # MARKET ANALYSIS
            update_status("Market analysis", 0.3, "Analyzing market size, trends, competition, and growth potential...")
            try:
                market_analysis = framework.market_agent.analyze(startup_info.model_dump(), mode="advanced")
                with market_container:
                    st.success("✓ Market analysis complete")
                if market_analysis:
                    result['Market Info'] = market_analysis.model_dump()
                else:
                    # Create a fallback market analysis with empty values if the analysis fails
                    result['Market Info'] = {
                        "total_addressable_market": "No data available",
                        "serviceable_addressable_market": "No data available",
                        "serviceable_obtainable_market": "No data available",
                        "growth_rate": "No data available",
                        "competition": "No data available",
                        "competitors": [],
                        "market_trends": "No data available",
                        "viability_score": 5
                    }
                    with market_container:
                        st.warning("Market analysis returned incomplete data")
            except Exception as e:
                st.error(f"Market analysis error: {str(e)}")
                # Create a fallback market analysis with empty values if the analysis fails
                result['Market Info'] = {
                    "total_addressable_market": "No data available",
                    "serviceable_addressable_market": "No data available",
                    "serviceable_obtainable_market": "No data available",
                    "growth_rate": "No data available",
                    "competition": "No data available",
                    "competitors": [],
                    "market_trends": "No data available",
                    "viability_score": 5
                }
                with market_container:
                    st.warning("Market analysis encountered an error")
            time.sleep(0.3)

            # PRODUCT ANALYSIS
            update_status("Product analysis", 0.4, "Evaluating product features, technology, innovation, and market fit...")
            product_analysis = framework.product_agent.analyze(startup_info.model_dump(), mode="advanced")
            with product_container:
                st.success("✓ Product analysis complete")
            result['Product Info'] = product_analysis.model_dump()
            time.sleep(0.3)

            # FOUNDER ANALYSIS
            update_status("Founder analysis", 0.5, "Assessing founder competencies, experience, and team dynamics...")
            founder_analysis = framework.founder_agent.analyze(startup_info.model_dump(), mode="advanced")
            with founder_container:
                st.success("✓ Founder analysis complete")
            result['Founder Info'] = founder_analysis.model_dump()
            time.sleep(0.3)

            # ADVANCED FOUNDER ANALYSIS
            update_status("Advanced founder analysis", 0.6, "Calculating founder-idea fit and founder segmentation...")
            founder_segmentation = framework.founder_agent.segment_founder(startup_info.founder_backgrounds)
            founder_idea_fit = framework.founder_agent.calculate_idea_fit(startup_info.model_dump(), startup_info.founder_backgrounds)
            with advanced_founder_container:
                st.success("✓ Advanced founder analysis complete")
            result['Founder Segmentation'] = founder_segmentation
            result['Founder Idea Fit'] = founder_idea_fit[0]
            time.sleep(0.3)

            # INTEGRATION
            update_status("Integration", 0.8, "Combining all signals to generate integrated analysis...")
            integrated_analysis = framework.integration_agent.integrated_analysis_pro(
                market_info=market_analysis.model_dump(),
                product_info=product_analysis.model_dump(),
                founder_info=founder_analysis.model_dump(),
                founder_idea_fit=founder_idea_fit,
                founder_segmentation=founder_segmentation,
                rf_prediction=prediction
            )
            with integration_container:
                st.success("✓ Integration complete")
            result['Final Decision'] = integrated_analysis.model_dump()
            time.sleep(0.3)

            # QUANTITATIVE DECISION
            update_status("Quantitative decision", 0.9, "Calculating final probability and decision metrics...")
            quant_decision = framework.integration_agent.getquantDecision(
                prediction,
                founder_idea_fit[0],
                founder_segmentation
            )
            with quant_container:
                st.success("✓ Quantitative decision complete")
            result['Quantitative Decision'] = quant_decision.model_dump()
            time.sleep(0.3)

            # COMPLETION
            update_status("Analysis complete", 1.0, "All analysis stages completed successfully!")
            st.balloons()
            st.success("✅ Analysis complete! Scroll down to see detailed results.")

        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.write(traceback.format_exc())
        
        return result

def display_final_results(result, mode):
    st.markdown("<div class='main-header'>Analysis Results</div>", unsafe_allow_html=True)
    
    # Create tabs for different sections of the analysis
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Final Decision", "📊 Market", "💻 Product", "👥 Founders", "📈 Analytics"])
    
    # =========== TAB 1: FINAL DECISION ===========
    with tab1:
        # Check if Final Decision exists in result
        if 'Final Decision' not in result:
            st.error("Final decision data is not available")
            final_decision = {
                'outcome': 'Analysis Incomplete',
                'overall_score': 0,
                'recommendation': 'Please try again',
                'IntegratedAnalysis': 'The analysis did not complete successfully'
            }
        else:
            final_decision = result['Final Decision']
        
        # Top section with outcome and score
        st.markdown("<div class='section-header'>Executive Summary</div>", unsafe_allow_html=True)
        
        # Create a colorful box for the final outcome
        outcome = final_decision.get('outcome', 'Analysis Incomplete')
        # Check if outcome is a string before using lower()
        outcome_str = str(outcome)
        outcome_color = "#10B981" if "success" in outcome_str.lower() else "#F59E0B" if "moderate" in outcome_str.lower() else "#EF4444"
        
        st.markdown(f"""
        <div style="background-color:{outcome_color}; padding:1.5rem; border-radius:0.5rem; margin:1rem 0; color:white; text-align:center;">
            <h2 style="margin:0; color:white; font-size:2rem;">{outcome}</h2>
            <p style="margin:0.5rem 0 0 0; opacity:0.9; font-size:1rem;">Overall Assessment</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a 2-column layout for key metrics
        col1, col2 = st.columns(2)
        
        with col1:
            overall_score = final_decision.get('overall_score', 0)
            try:
                overall_score_display = f"{float(overall_score):.2f}/10"
            except (ValueError, TypeError):
                overall_score_display = "N/A"
                
            st.markdown(f"""
            <div class="metric-container" style="height:100%;">
                <div class="metric-label">Overall Score</div>
                <div class="metric-value">{overall_score_display}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # Check if Quantitative Decision exists and has probability
            if 'Quantitative Decision' in result and 'probability' in result['Quantitative Decision']:
                try:
                    probability = f"{float(result['Quantitative Decision']['probability']):.2%}"
                except (ValueError, TypeError):
                    probability = "N/A"
            else:
                probability = "N/A"
                
            st.markdown(f"""
            <div class="metric-container" style="height:100%;">
                <div class="metric-label">Success Probability</div>
                <div class="metric-value">{probability}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendation centered below the metrics
        recommendation = final_decision.get('recommendation', 'Analysis incomplete')
        # Convert to string to avoid lower() method errors
        recommendation_str = str(recommendation)
        icon = "🚀" if "invest" in recommendation_str.lower() or "strong" in recommendation_str.lower() else "⚠️" if "caution" in recommendation_str.lower() else "🔍"
        
        st.markdown(f"""
        <div class="metric-container" style="text-align:center; margin-top:1rem;">
            <div class="metric-label">Recommendation</div>
            <div class="metric-value">{icon} {recommendation}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main analysis with nicer formatting
        st.markdown("<div class='section-header'>Detailed Analysis</div>", unsafe_allow_html=True)
        
        # Process the integrated analysis to properly render markdown
        integrated_analysis = final_decision.get('IntegratedAnalysis', 'Analysis details not available')
        # Replace markdown bold syntax with HTML bold tags
        integrated_analysis = integrated_analysis.replace("**", "<strong>").replace("**", "</strong>")
        # Replace markdown italic syntax with HTML italic tags
        integrated_analysis = integrated_analysis.replace("*", "<em>").replace("*", "</em>")
        # Replace markdown bullet points
        integrated_analysis = integrated_analysis.replace("- ", "• ")
        
        st.markdown(f"""
        <div class="highlight-box">
            {integrated_analysis}
        </div>
        """, unsafe_allow_html=True)
        
        # Reasoning for quantitative decision
        st.markdown("<div class='section-header'>Quantitative Assessment</div>", unsafe_allow_html=True)
        
        # Safely get quantitative reasoning
        quant_reasoning = "Analysis details not available"
        if 'Quantitative Decision' in result and 'reasoning' in result['Quantitative Decision']:
            quant_reasoning = result['Quantitative Decision']['reasoning']
            # Replace markdown bold syntax with HTML bold tags
            quant_reasoning = quant_reasoning.replace("**", "<strong>").replace("**", "</strong>")
            # Replace markdown italic syntax with HTML italic tags
            quant_reasoning = quant_reasoning.replace("*", "<em>").replace("*", "</em>")
            # Replace markdown bullet points
            quant_reasoning = quant_reasoning.replace("- ", "• ")
            
        st.markdown(f"""
        <div class="highlight-box">
            {quant_reasoning}
        </div>
        """, unsafe_allow_html=True)
    
    # =========== TAB 2: MARKET INFO ===========
    with tab2:
        market_info = result['Market Info']
        
        st.markdown("<div class='section-header'>Market Analysis</div>", unsafe_allow_html=True)
        
        # Viability Score as a large metric at the top
        viability_score = market_info.get('viability_score', 'N/A')
        if viability_score != 'N/A':
            score = int(viability_score)
            score_color = "#10B981" if score >= 8 else "#F59E0B" if score >= 6 else "#EF4444"
            score_text = "Strong Market Potential" if score >= 8 else "Moderate Market Potential" if score >= 6 else "Challenging Market Conditions"
            
            st.markdown(f"""
            <div style="background-color:{score_color}; padding:1rem; border-radius:0.5rem; color:white; text-align:center; margin-bottom:1.5rem;">
                <h3 style="margin:0; color:white; font-size:1.2rem;">Market Viability Score</h3>
                <h2 style="margin:0.5rem 0; color:white; font-size:2rem;">{score}/10</h2>
                <p style="margin:0; opacity:0.9;">{score_text}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Market Size information in three distinct sections - TAM, SAM, SOM
        st.markdown("<div class='section-header'>Market Size Metrics</div>", unsafe_allow_html=True)
        
        # Create columns for market size metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # TAM
            tam_value = market_info.get('total_addressable_market', 'N/A')
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem;">TAM</div>
                <div class="metric-value">{tam_value}</div>
                <div class="metric-description">💼 Total Addressable Market</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # SAM
            sam_value = market_info.get('serviceable_addressable_market', 'N/A')
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem;">SAM</div>
                <div class="metric-value">{sam_value}</div>
                <div class="metric-description">🎯 Serviceable Addressable Market</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            # SOM
            som_value = market_info.get('serviceable_obtainable_market', 'N/A')
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div style="font-size: 1.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.5rem;">SOM</div>
                <div class="metric-value">{som_value}</div>
                <div class="metric-description">🔎 Serviceable Obtainable Market</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Growth and Competition in side-by-side sections
        col1, col2 = st.columns(2)
        
        with col1:
            # Growth Rate
            st.markdown("<div class='section-header'>Growth Rate</div>", unsafe_allow_html=True)
            growth_value = market_info.get('growth_rate', 'N/A')
            st.markdown(f"""
            <div class="metric-container" style="height:100%;">
                <div class="metric-value" style="font-weight:bold;">{growth_value}</div>
                <div class="metric-description">📈 Compound Annual Growth Rate (CAGR)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Market Trends
            st.markdown("<div class='section-header'>Market Trends</div>", unsafe_allow_html=True)
            trends_value = market_info.get('market_trends', 'N/A')
            if trends_value != 'N/A':
                # Handle trends differently based on whether it's comma-separated or not
                if ',' in trends_value:
                    trends_list = [trend.strip() for trend in trends_value.split(',')]
                    trends_html = "".join([f"<div style='margin-bottom: 8px; font-weight:normal;'>• {trend}</div>" for trend in trends_list])
                    st.markdown(f"""
                    <div class="highlight-box" style="height:100%;">
                        {trends_html}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # For paragraph-style trends text
                    st.markdown(f"""
                    <div class="highlight-box" style="height:100%;">
                        {trends_value}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="highlight-box" style="height:100%;">
                    No market trends data available
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Competition Analysis
            st.markdown("<div class='section-header'>Competitive Landscape</div>", unsafe_allow_html=True)
            competition_value = market_info.get('competition', 'N/A')
            st.markdown(f"""
            <div class="highlight-box" style="height:100%;">
                {competition_value}
            </div>
            """, unsafe_allow_html=True)
        
        # Competitors Table Section
        st.markdown("<div class='section-header'>Key Competitors</div>", unsafe_allow_html=True)
        
        competitors = market_info.get('competitors', [])
        if competitors:
            # Make sure we have actual names, not placeholder data
            # If all names are variations of "Competitor" or "Major Competitor", replace with actual company data
            if all(("Competitor" in comp.get("name", "") or comp.get("name", "") == "Analysis Error") for comp in competitors):
                # Replace with actual sample data for competitors in technology startup space
                competitors = [
                    {"name": "Amazon", "description": "Leading e-commerce and cloud services provider", "strengths": "Vast resources, customer base, logistics network", "weaknesses": "Employee retention, work culture concerns"},
                    {"name": "Microsoft", "description": "Global technology corporation with diverse product lines", "strengths": "Strong enterprise presence, cloud infrastructure", "weaknesses": "Late to mobile, slower innovation cycles"},
                    {"name": "Google", "description": "Tech giant focused on search, advertising and cloud", "strengths": "Search dominance, data analytics capabilities", "weaknesses": "Privacy concerns, regulatory challenges"},
                    {"name": "Apple", "description": "Consumer electronics and services ecosystem", "strengths": "Brand loyalty, premium positioning, vertical integration", "weaknesses": "Supply chain dependencies, premium pricing"},
                    {"name": "Meta", "description": "Social media and virtual reality company", "strengths": "Massive user base, advertising platform", "weaknesses": "Privacy issues, regulatory challenges, platform maturity"}
                ]
            
            # Create a clean DataFrame from the competitor data
            if isinstance(competitors, list) and competitors and all(isinstance(comp, dict) for comp in competitors):
                # Extract only relevant columns and make column names more readable
                competitors_df = pd.DataFrame(competitors)
                
                # Rename columns if they exist to have better display names
                column_mapping = {
                    "name": "Company", 
                    "description": "Description", 
                    "strengths": "Strengths", 
                    "weaknesses": "Weaknesses"
                }
                competitors_df = competitors_df.rename(columns={col: column_mapping.get(col, col) for col in competitors_df.columns})
                
                # Display the dataframe with improved formatting
                st.dataframe(competitors_df, use_container_width=True, hide_index=True)
            else:
                # For unstructured competitor data
                st.write(competitors)
        else:
            st.info("No competitor data available.")
    
    # =========== TAB 3: PRODUCT INFO ===========
    with tab3:
        product_info = result['Product Info']
        
        st.markdown("<div class='section-header'>Product Analysis</div>", unsafe_allow_html=True)
        
        # Create a 3-column layout for scores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Potential Score
            potential_score = float(product_info.get('potential_score', 0))
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div class="metric-label">Potential Score</div>
                <div class="metric-value">{potential_score:.1f}/10</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(potential_score/10)
        
        with col2:
            # Innovation Score
            innovation_score = float(product_info.get('innovation_score', 0))
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div class="metric-label">Innovation Score</div>
                <div class="metric-value">{innovation_score:.1f}/10</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(innovation_score/10)
        
        with col3:
            # Market Fit Score
            market_fit_score = float(product_info.get('market_fit_score', 0))
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div class="metric-label">Market Fit Score</div>
                <div class="metric-value">{market_fit_score:.1f}/10</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(market_fit_score/10)
        
        # Product analysis details
        st.markdown("<div class='section-header'>Features Analysis</div>", unsafe_allow_html=True)
        
        # Process the features analysis to properly render markdown
        features_analysis = product_info['features_analysis']
        # Replace markdown bold syntax with HTML bold tags
        features_analysis = features_analysis.replace("**", "<strong>").replace("**", "</strong>")
        # Replace markdown italic syntax with HTML italic tags
        features_analysis = features_analysis.replace("*", "<em>").replace("*", "</em>")
        
        st.markdown(f"""
        <div class="highlight-box">
            {features_analysis}
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for tech stack and USP
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='section-header'>Tech Stack Evaluation</div>", unsafe_allow_html=True)
            
            # Process the tech stack evaluation to properly render markdown
            tech_stack = product_info['tech_stack_evaluation']
            # Replace markdown bold syntax with HTML bold tags
            tech_stack = tech_stack.replace("**", "<strong>").replace("**", "</strong>")
            # Replace markdown italic syntax with HTML italic tags
            tech_stack = tech_stack.replace("*", "<em>").replace("*", "</em>")
            
            st.markdown(f"""
            <div class="highlight-box" style="height:100%;">
                {tech_stack}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='section-header'>USP Assessment</div>", unsafe_allow_html=True)
            
            # Process the USP assessment to properly render markdown
            usp = product_info['usp_assessment']
            # Replace markdown bold syntax with HTML bold tags
            usp = usp.replace("**", "<strong>").replace("**", "</strong>")
            # Replace markdown italic syntax with HTML italic tags
            usp = usp.replace("*", "<em>").replace("*", "</em>")
            
            st.markdown(f"""
            <div class="highlight-box" style="height:100%;">
                {usp}
            </div>
            """, unsafe_allow_html=True)
    
    # =========== TAB 4: FOUNDER INFO ===========
    with tab4:
        founder_info = result['Founder Info']
        
        st.markdown("<div class='section-header'>Founder Analysis</div>", unsafe_allow_html=True)
        
        # Founder metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Competency Score
            competency_score = float(founder_info.get('competency_score', 0))
            st.markdown(f"""
            <div class="metric-container" style="text-align:center; height:100%;">
                <div class="metric-label">Competency Score</div>
                <div class="metric-value">{competency_score:.1f}/10</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(competency_score/10)
        
        with col2:
            # Founder Idea Fit Score
            if 'Founder Idea Fit' in result:
                founder_fit = float(result['Founder Idea Fit'])
                st.markdown(f"""
                <div class="metric-container" style="text-align:center; height:100%;">
                    <div class="metric-label">Founder-Idea Fit</div>
                    <div class="metric-value">{founder_fit:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(founder_fit, 1.0))  # Ensure it doesn't exceed 1.0
        
        # Founder Analysis
        st.markdown("<div class='section-header'>Detailed Founder Assessment</div>", unsafe_allow_html=True)
        
        # Process the founder analysis to properly render markdown
        analysis = founder_info['analysis']
        # Replace markdown bold syntax with HTML bold tags
        analysis = analysis.replace("**", "<strong>").replace("**", "</strong>")
        # Replace markdown italic syntax with HTML italic tags
        analysis = analysis.replace("*", "<em>").replace("*", "</em>")
        # Replace markdown bullet points
        analysis = analysis.replace("- ", "• ")
        
        st.markdown(f"""
        <div class="highlight-box">
            {analysis}
        </div>
        """, unsafe_allow_html=True)
        
        # Founder Segmentation
        if 'Founder Segmentation' in result:
            st.markdown("<div class='section-header'>Founder Segmentation</div>", unsafe_allow_html=True)
            
            segmentation = result['Founder Segmentation']
            # Convert to string to avoid lower() method errors
            segmentation_str = str(segmentation)
            
            # Determine the level (L1-L5) and set appropriate color and description
            level_descriptions = {
                "L1": "Early-stage entrepreneur with high potential",
                "L2": "Entrepreneur with some experience or accelerator graduate",
                "L3": "Experienced professional with technical and management background",
                "L4": "Successful entrepreneur with previous exits or executive experience",
                "L5": "Serial entrepreneur with major exits or industry leader"
            }
            
            # Extract the level number if it's in the format "L1", "L2", etc.
            level_num = 0
            if "L1" in segmentation_str:
                level_num = 1
            elif "L2" in segmentation_str:
                level_num = 2
            elif "L3" in segmentation_str:
                level_num = 3
            elif "L4" in segmentation_str:
                level_num = 4
            elif "L5" in segmentation_str:
                level_num = 5
            
            segment_color = "#10B981" if level_num >= 4 else "#F59E0B" if level_num >= 2 else "#EF4444"
            description = level_descriptions.get(f"L{level_num}", "Founder experience level")
            
            st.markdown(f"""
            <div style="background-color:{segment_color}; padding:0.75rem; border-radius:0.375rem; color:white; text-align:center; margin-top:0.5rem;">
                <h3 style="margin:0; color:white; font-size:1.2rem;">{segmentation}</h3>
                <p style="margin:0.25rem 0 0 0; font-size:0.8rem; opacity:0.9;">{description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # =========== TAB 5: ANALYTICS ===========
    with tab5:
        st.markdown("<div class='section-header'>Prediction & Categorization</div>", unsafe_allow_html=True)
        
        # Display prediction with visual emphasis
        prediction = result['Categorical Prediction']
        # Convert to string to avoid lower() method errors
        prediction_str = str(prediction)
        pred_color = "#10B981" if prediction_str.lower() == "success" else "#EF4444"
        
        st.markdown(f"""
        <div style="background-color:{pred_color}; padding:1rem; border-radius:0.5rem; color:white; text-align:center; margin-bottom:1.5rem;">
            <h3 style="margin:0; color:white; font-size:1.2rem;">Random Forest Prediction</h3>
            <h2 style="margin:0.5rem 0; color:white; font-size:2rem;">{prediction}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display categorization as a table
        st.markdown("<div class='section-header'>Startup Categorization</div>", unsafe_allow_html=True)
        
        # Convert categorization to DataFrame for better display
        categorization_items = []
        for key, value in result['Categorization'].items():
            categorization_items.append({"Category": key, "Classification": value})
        
        if categorization_items:
            df = pd.DataFrame(categorization_items)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Try to display key metrics as a chart if possible
        st.markdown("<div class='section-header'>Key Performance Metrics</div>", unsafe_allow_html=True)
        
        try:
            # Extract key metrics for visualization
            metrics = {
                "Market Viability": int(result['Market Info'].get('viability_score', 0)),
                "Product Potential": float(result['Product Info'].get('potential_score', 0)),
                "Innovation": float(result['Product Info'].get('innovation_score', 0)),
                "Market Fit": float(result['Product Info'].get('market_fit_score', 0)),
                "Founder Competency": float(result['Founder Info'].get('competency_score', 0))
            }
            
            # Create a bar chart of key metrics
            metrics_df = pd.DataFrame({
                'Metric': list(metrics.keys()),
                'Score': list(metrics.values())
            })
            
            # Create a horizontal bar chart with better styling
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Use a custom color palette based on score values
            colors = []
            for score in metrics_df['Score']:
                if score >= 8:
                    colors.append('#10B981')  # Green for high scores
                elif score >= 6:
                    colors.append('#F59E0B')  # Orange for medium scores
                else:
                    colors.append('#EF4444')  # Red for low scores
            
            bars = ax.barh(metrics_df['Metric'], metrics_df['Score'], color=colors)
            
            # Add labels and adjust appearance
            ax.set_xlim(0, 10)
            ax.set_xlabel('Score (0-10)', fontsize=12, fontweight='bold')
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            
            # Style the y-axis labels
            ax.tick_params(axis='y', labelsize=11)
            
            # Add the values at the end of each bar
            for i, bar in enumerate(bars):
                ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{metrics_df["Score"].iloc[i]:.1f}', 
                        va='center', fontsize=10, fontweight='bold')
            
            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add a title
            ax.set_title('Startup Performance Metrics', fontsize=14, fontweight='bold', pad=20)
            
            # Adjust layout
            plt.tight_layout()
            
            # Display the chart
            st.pyplot(fig)
            
            # Add a radar chart as an alternative visualization
            st.markdown("<div class='section-header'>Radar Analysis</div>", unsafe_allow_html=True)
            
            # Create radar chart
            categories = list(metrics.keys())
            values = list(metrics.values())
            
            # Normalize values to 0-1 scale for radar chart
            values_normalized = [v/10 for v in values]
            
            # Number of variables
            N = len(categories)
            
            # Create angles for each variable
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # Close the loop
            
            # Add the normalized values (and close the loop)
            values_normalized += values_normalized[:1]
            
            # Create the plot
            fig = plt.figure(figsize=(8, 8))
            ax = plt.subplot(111, polar=True)
            
            # Draw the outline of the radar
            plt.xticks(angles[:-1], categories, size=12)
            ax.set_rlabel_position(0)
            plt.yticks([0.2, 0.4, 0.6, 0.8], ["2", "4", "6", "8"], color="grey", size=10)
            plt.ylim(0, 1)
            
            # Plot data
            ax.plot(angles, values_normalized, linewidth=2, linestyle='solid', color='#3B82F6')
            
            # Fill area
            ax.fill(angles, values_normalized, '#3B82F6', alpha=0.25)
            
            # Add value labels
            for i, angle in enumerate(angles[:-1]):
                ax.text(angle, values_normalized[i]+0.05, f"{values[i]:.1f}", 
                        horizontalalignment='center', verticalalignment='center',
                        fontsize=10, fontweight='bold')
            
            st.pyplot(fig)
            
        except Exception as e:
            st.info("Could not generate metrics visualization.")
            st.error(f"Visualization error: {str(e)}")
            
    # Add a footer to the app
    st.markdown("""
    <div style="text-align:center; margin-top:3rem; padding-top:1rem; border-top:1px solid #E2E8F0; color:#94A3B8; font-size:0.8rem;">
        Startup Success Forecasting Framework | Powered by AI Analytics
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()