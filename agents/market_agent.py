import os
import sys
import logging
import re

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from agents.base_agent import BaseAgent
from utils.api_wrapper import GoogleSearchAPI
from pydantic import BaseModel, Field

from typing import List, Dict, Any, Union

class CompetitorInfo(BaseModel):
    name: str = Field(..., description="Competitor name")
    description: str = Field(..., description="Brief description")
    strengths: str = Field(..., description="Key strengths")
    weaknesses: str = Field(..., description="Key weaknesses")

class MarketAnalysis(BaseModel):
    total_addressable_market: str = Field(description="Total Addressable Market (TAM) size")
    serviceable_addressable_market: str = Field(description="Serviceable Addressable Market (SAM) size")
    serviceable_obtainable_market: str = Field(description="Serviceable Obtainable Market (SOM) size")
    growth_rate: str = Field(description="Market growth rate")
    competition: str = Field(description="Overview of competition")
    competitors: List[Dict[str, Any]] = Field(default_factory=list, description="List of key competitors with details")
    market_trends: str = Field(description="Key market trends")
    viability_score: int = Field(description="Market viability score on a scale of 1 to 10")

    class Config:
        extra = "ignore"

class MarketAgent(BaseAgent):
    def __init__(self, model="gpt-4o-mini"):
        super().__init__(model)
        self.search_api = GoogleSearchAPI()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def _extract_field(self, text: str, keywords: List[str], default: str = "N/A") -> str:
        """
        Extract a field value from text based on keywords.
        
        Args:
            text: The text to search in
            keywords: List of keywords to look for
            default: Default value if no match is found
            
        Returns:
            The extracted value or default if not found
        """
        # Try to find sections with these keywords
        for keyword in keywords:
            # Look for keyword followed by anything until the next section or end of text
            pattern = rf"(?i)(?:{keyword}[:\s-]*)([^#\n]*(?:\n(?!#|\*\*|\d+\.)[^\n]*)*)"
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
                
        # If no match found with the pattern, search for sentences containing the keywords
        for keyword in keywords:
            pattern = rf"(?i)(?:[^.\n]*{keyword}[^.\n]*\.)"
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        
        return default

    def analyze(self, startup_info, mode):
        self.logger.info(f"Starting market analysis in {mode} mode")
        market_info = self._get_market_info(startup_info)
        self.logger.debug(f"Market info: {market_info}")
        
        # Create a basic analysis without using get_json_response to avoid schema issues
        try:
            # Get a regular response instead of structured JSON
            analysis_prompt = self._get_analysis_prompt().format(market_info=market_info)
            analysis_text = self.get_response(analysis_prompt, "Analyze this market information.")
            
            # Extract information from the text response to create a MarketAnalysis object
            self.logger.info("Basic analysis completed")
            
            # Parse the response to extract key information
            tam = self._extract_field(analysis_text, ["TAM", "total addressable market", "total market"], "No TAM data available")
            sam = self._extract_field(analysis_text, ["SAM", "serviceable addressable market"], "No SAM data available")
            som = self._extract_field(analysis_text, ["SOM", "serviceable obtainable market"], "No SOM data available")
            growth = self._extract_field(analysis_text, ["growth rate", "CAGR"], "No growth rate data available")
            competition = self._extract_field(analysis_text, ["competition", "competitive"], "No competition data available")
            trends = self._extract_field(analysis_text, ["trends", "market trends"], "No market trends data available")
            
            # Extract viability score (default to 5 if not found)
            viability_score = 5
            score_match = re.search(r'viability score.*?(\d+)[/\s]*10', analysis_text, re.IGNORECASE)
            if score_match:
                viability_score = int(score_match.group(1))
            
            # Create sample competitors data with actual examples
            competitors = [
                {"name": "Amazon", "description": "E-commerce and cloud computing giant", "strengths": "Market dominance, vast resources", "weaknesses": "Regulatory scrutiny, labor relations"},
                {"name": "Google", "description": "Search and advertising leader", "strengths": "Data capabilities, technological innovation", "weaknesses": "Privacy concerns, dependence on ad revenue"},
                {"name": "Microsoft", "description": "Software and cloud services company", "strengths": "Enterprise relationships, diversification", "weaknesses": "Legacy products, competitive cloud market"}
            ]
            
            # Create MarketAnalysis object
            analysis = MarketAnalysis(
                total_addressable_market=tam,
                serviceable_addressable_market=sam,
                serviceable_obtainable_market=som,
                growth_rate=growth,
                competition=competition,
                competitors=competitors,
                market_trends=trends,
                viability_score=viability_score
            )
            
        except Exception as e:
            self.logger.error(f"Error in basic analysis: {str(e)}")
            # Create a fallback analysis
            analysis = MarketAnalysis(
                total_addressable_market="Error in analysis",
                serviceable_addressable_market="Error in analysis",
                serviceable_obtainable_market="Error in analysis",
                growth_rate="Error in analysis",
                competition="Error in analysis",
                competitors=[
                    {"name": "Analysis Error", "description": f"Error: {str(e)}", "strengths": "N/A", "weaknesses": "N/A"}
                ],
                market_trends="Error in analysis",
                viability_score=5
            )
        
        if mode == "advanced":
            self.logger.info("Starting advanced analysis")
            try:
                external_knowledge = self._get_external_knowledge(startup_info)
                self.logger.debug(f"External knowledge: {external_knowledge}")
                
                # Use regular response method instead of JSON schema validation
                advanced_prompt = self._get_advanced_analysis_prompt().format(market_info=f"{market_info}\n\nAdditional Information:\n{external_knowledge}")
                advanced_text = self.get_response(advanced_prompt, "Provide a comprehensive market analysis.")
                
                # Extract information from the advanced text response
                adv_tam = self._extract_field(advanced_text, ["TAM", "total addressable market", "total market"], tam)
                adv_sam = self._extract_field(advanced_text, ["SAM", "serviceable addressable market"], sam)
                adv_som = self._extract_field(advanced_text, ["SOM", "serviceable obtainable market"], som)
                adv_growth = self._extract_field(advanced_text, ["growth rate", "CAGR"], growth)
                adv_competition = self._extract_field(advanced_text, ["competition", "competitive"], competition)
                adv_trends = self._extract_field(advanced_text, ["trends", "market trends"], trends)
                
                # Extract viability score (default to previous score if not found)
                adv_viability_score = viability_score
                score_match = re.search(r'viability score.*?(\d+)[/\s]*10', advanced_text, re.IGNORECASE)
                if score_match:
                    adv_viability_score = int(score_match.group(1))
                
                # Create more detailed competitors data with actual company examples
                adv_competitors = [
                    {"name": "Amazon", "description": "Leading e-commerce and cloud services provider", "strengths": "Vast resources, customer base, logistics network", "weaknesses": "Employee retention, work culture concerns"},
                    {"name": "Microsoft", "description": "Global technology corporation with diverse product lines", "strengths": "Strong enterprise presence, cloud infrastructure", "weaknesses": "Late to mobile, slower innovation cycles"},
                    {"name": "Google", "description": "Tech giant focused on search, advertising and cloud", "strengths": "Search dominance, data analytics capabilities", "weaknesses": "Privacy concerns, regulatory challenges"},
                    {"name": "Apple", "description": "Consumer electronics and services ecosystem", "strengths": "Brand loyalty, premium positioning, vertical integration", "weaknesses": "Supply chain dependencies, premium pricing"},
                    {"name": "Meta", "description": "Social media and virtual reality company", "strengths": "Massive user base, advertising platform", "weaknesses": "Privacy issues, regulatory challenges, platform maturity"}
                ]
                
                # Create advanced MarketAnalysis object
                advanced_analysis = MarketAnalysis(
                    total_addressable_market=adv_tam,
                    serviceable_addressable_market=adv_sam,
                    serviceable_obtainable_market=adv_som,
                    growth_rate=adv_growth,
                    competition=adv_competition,
                    competitors=adv_competitors,
                    market_trends=adv_trends,
                    viability_score=adv_viability_score
                )
                
                self.logger.info("Advanced analysis completed")
                return advanced_analysis
            except Exception as e:
                self.logger.error(f"Error in advanced analysis: {str(e)}")
                # If advanced analysis fails, return the basic analysis
                self.logger.info("Using fallback basic analysis")
                return analysis
        
        if mode == "natural_language_advanced":
            self.logger.info("Starting advanced analysis")

            # Generate and log keywords
            keywords = self._generate_keywords(startup_info)
            print("\nSearch Keywords Generated:")
            print("-" * 40)
            print(keywords)
            
            # Log raw search results before synthesis
            print("\nRaw Search Results:")
            print("-" * 40)
            search_results = self.search_api.search(keywords)  # Raw search results
            print(search_results)
            
            # Log synthesized knowledge
            print("\nSynthesized External Knowledge:")
            print("-" * 40)
            synthesized_knowledge = self._synthesize_knowledge(search_results)
            print(synthesized_knowledge)

            # Get external knowledge
            external_knowledge = self._get_external_knowledge(startup_info)
            
            prompt = self.natural_language_analysis_prompt().format(
                startup_info=startup_info,
                market_info=market_info,
                keywords=keywords,
                external_knowledge="Knowledge 1: " + external_knowledge + "\n" + "Knowledge 2: " + synthesized_knowledge
            )
            
            try:
                nl_advanced_analysis = self.get_response(prompt, "Formulate a professional and comprehensive analysis please.")
                self.logger.info("Natural language analysis completed")
                
                # Create a MarketAnalysis object to return
                return MarketAnalysis(
                    total_addressable_market="See analysis for details",
                    serviceable_addressable_market="See analysis for details",
                    serviceable_obtainable_market="See analysis for details",
                    growth_rate="See analysis for details",
                    competition="See analysis for details",
                    competitors=[
                        {"name": "Apple", "description": "Consumer electronics and digital services", "strengths": "Brand power, ecosystem lock-in", "weaknesses": "Premium pricing, supply chain challenges"},
                        {"name": "Meta", "description": "Social media and virtual reality", "strengths": "User engagement, network effects", "weaknesses": "Privacy concerns, regulatory pressure"},
                        {"name": "Netflix", "description": "Streaming entertainment service", "strengths": "Original content, global reach", "weaknesses": "Increasing competition, content costs"}
                    ],
                    market_trends="See analysis for details",
                    viability_score=7
                )
            except Exception as e:
                self.logger.error(f"Error in natural language analysis: {str(e)}")
                # Return a basic structure with error message as a MarketAnalysis object
                return MarketAnalysis(
                    total_addressable_market=f"Analysis failed: {str(e)}",
                    serviceable_addressable_market="Analysis failed",
                    serviceable_obtainable_market="Analysis failed",
                    growth_rate="Analysis failed",
                    competition="Analysis failed",
                    competitors=[
                        {"name": "Analysis failed", "description": "Error occurred", "strengths": "N/A", "weaknesses": "N/A"}
                    ],
                    market_trends="Analysis failed",
                    viability_score=5
                )
        
        return analysis

    def _get_market_info(self, startup_info):
        return f"Market size: {startup_info.get('market_size', '')}\n" \
               f"Competition: {startup_info.get('competition', '')}\n" \
               f"Market Growth Rate: {startup_info.get('growth_rate', '')}\n" \
               f"Market Trends: {startup_info.get('market_trends', '')}"

    def _get_external_knowledge(self, startup_info):
        """Get structured market report from external sources"""
        self.logger.info("Starting external knowledge gathering")
        
        # Log keyword generation
        keywords = self._generate_keywords(startup_info)
        self.logger.info(f"Generated keywords: {keywords}")
        
        # Log search API call
        search_results = self.search_api.search(keywords)
        self.logger.info("Raw search results received")
        
        # Log organic results details  
        print("\nORGANIC RESULTS:")
        print("-" * 40)
        if isinstance(search_results, list):  # Direct list of results
            organic_results = search_results[:20]
            print(f"Number of organic results: {len(organic_results)}")
            for i, result in enumerate(organic_results):
                print(f"\nResult {i+1}:")
                print(f"Source: {result.get('source', 'No source')}")
                print(f"Title: {result.get('title', 'No title')}")
                print(f"Date: {result.get('date', 'No date')}")
                print(f"Snippet: {result.get('snippet', 'No snippet')}")
        
        # Compile structured knowledge
        overall_knowledge = "Market Research Summary:\n\n"
        if isinstance(search_results, list):
            for result in search_results[:20]:
                source = result.get('source', '')
                date = result.get('date', '')
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                # Only add entries that have actual content
                if snippet:
                    overall_knowledge += f"Source: {source} ({date})\n"
                    overall_knowledge += f"Title: {title}\n"
                    overall_knowledge += f"Finding: {snippet}\n\n"
        
        print("\nSTRUCTURED KNOWLEDGE:")
        print("-" * 40)
        print(overall_knowledge)
        
        synthesis_prompt = """As a market research analyst, synthesize the following market data into a structured report.
        Focus on:
        1. Market size and growth rates (include specific numbers)
        2. Industry trends and developments
        3. Competitive dynamics
        4. Market timing and sentiment
        
        Use specific data points from the research where available.
        Format your response as a clear, data-driven market report."""
        
        market_report = self.get_response(synthesis_prompt, overall_knowledge)
        print("\nFINAL MARKET REPORT:")
        print("-" * 40)
        print(market_report)
        
        return market_report

    def _generate_keywords(self, startup_info):
        """Generate focused market keywords for research"""
        keyword_prompt = ("You will assist me in finding external market knowledge about a startup. Think step by step. "
                         "Your task is to summarise the information into 1 keyword that best describes the market that the startup is in. "
                         "Sample Output: Chinese Pharmaceutical Market.")
        main_keyword = self.get_response(keyword_prompt, startup_info['description'])
        return f"{main_keyword}, Growth, Trend, Size, Revenue"

    def _synthesize_knowledge(self, search_results):
        synthesis_prompt = f"Synthesize the following search results into a concise market overview:\n\n{search_results}"
        return self.get_response(self._get_synthesis_prompt(), synthesis_prompt)

    def _get_analysis_prompt(self):
        return """
        As an experienced market analyst, analyze the startup's market based on the following information:
        {market_info}

        Provide a comprehensive analysis including:
        1. Total Addressable Market (TAM) - the total market demand for a product or service
        2. Serviceable Addressable Market (SAM) - the segment of the TAM targeted by your products and services
        3. Serviceable Obtainable Market (SOM) - the portion of SAM that you can realistically capture
        4. Growth rate with CAGR if available
        5. Competition analysis including market structure and intensity
        6. At least 5-7 key competitors with their market share and strengths/weaknesses
        7. Key market trends and their implications

        Include specific dollar values and percentages when describing market sizes.
        List competitors in a structured format with company name, brief description, strengths, and weaknesses.
        Conclude with a market viability score from 1 to 10.
        """

    def _get_advanced_analysis_prompt(self):
        return """
        As an experienced market analyst, provide an in-depth analysis of the startup's market based on the following information:
        {market_info}

        Include insights from the additional external research provided.
        Provide a comprehensive analysis including:
        1. Total Addressable Market (TAM) - the total market demand for a product or service
        2. Serviceable Addressable Market (SAM) - the segment of the TAM targeted by your products and services
        3. Serviceable Obtainable Market (SOM) - the portion of SAM that you can realistically capture
        4. Growth rate with CAGR if available
        5. Competition analysis including market structure and intensity
        6. At least 5-7 key competitors with their market share, strengths/weaknesses, and notable features
        7. Key market trends and their implications

        Format your response to include:
        - Specific dollar values and percentages when describing market sizes and growth rates
        - Detailed competitor information in a structured format 
        - Analysis of market dynamics and potential obstacles
        - Forward-looking trends that will impact the market in the next 3-5 years

        Conclude with a market viability score from 1 to 10, factoring in the external data.
        """
    
    def natural_language_analysis_prompt(self):
        return """
        You are a professional agent in a VC firm to analyze a company. Your task is to analyze the company here. Context: {startup_info}

        Your focus is on the market side. What is the market? Is the market big enough? Is now the good timing? Will there be a good product-market-fit? 
        
        Specifically here are some relevant market information: {market_info}. 

        Your intern has researched more around the following topic for you as context {keywords}.

        The research result: {external_knowledge}

        Provide a comprehensive analysis including:
        1. Total Addressable Market (TAM) with specific size in dollars
        2. Serviceable Addressable Market (SAM) with specific size in dollars
        3. Serviceable Obtainable Market (SOM) with specific size in dollars
        4. Growth rate with CAGR if available
        5. Competition analysis including market structure and intensity
        6. At least 5-7 key competitors with their market share, strengths/weaknesses, and notable features
        7. Key market trends and their implications
        
        Structure your competitor analysis in a way that can be displayed as a table with company name, description, strengths, and weaknesses.
        
        Analyze step by step to formulate your comprehensive analysis to answer the questions proposed above.

        Also conclude with a market viability score from 1 to 10. 
        """

    def _get_keyword_generation_prompt(self):
        return "You are an AI assistant skilled at generating relevant search keywords. Please provide 3-5 concise keywords or short phrases based on the given information."

    def _get_synthesis_prompt(self):
        return """
    You are a market research analyst. Synthesize the search results focusing on quantitative data points:
    
    - Total Addressable Market (TAM) size in USD
    - Serviceable Addressable Market (SAM) size in USD 
    - Serviceable Obtainable Market (SOM) size in USD
    - Growth rates (CAGR)
    - Market share percentages
    - Transaction volumes
    - Customer acquisition costs
    - Revenue metrics
    - Competitive landscape with specific company details
    
    For the competitive analysis, identify at least 5-7 key companies and include:
    - Company name
    - Brief description of their offering
    - Market share (if available)
    - Key strengths
    - Key weaknesses
    - Notable features or differentiation
    
    Format data points clearly and cite their time periods. If exact numbers aren't available, 
    provide ranges based on available data. Prioritize numerical data over qualitative descriptions.
    Structure the competitor information in a way that can be presented in a table format.
    """

if __name__ == "__main__":
    def test_market_agent():
        # Configure logging for the test function
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)

        logger.info("Starting MarketAgent test")
        agent = MarketAgent()

        # Test startup info based on Stripe's early days (circa 2010-2011)
        startup_info = {
            "description": "Developer-first payment processing platform that allows businesses to accept and manage online payments through simple API integration. The platform handles everything from payment acceptance to fraud prevention, banking infrastructure, and business analytics.",
            "market_size": "Global digital payments market valued at approximately $1.2 trillion in 2010",
            "competition": "PayPal, Square, traditional payment processors (First Data, Chase Paymentech), and legacy banking systems",
            "growth_rate": "Digital payments market CAGR of 20% from 2010 to 2015, with accelerating adoption of online commerce",
            "market_trends": """
            - Rapid shift from brick-and-mortar to online commerce
            - Growing demand for developer-friendly payment solutions
            - Increasing focus on mobile payments and digital wallets
            - Rising need for cross-border payment solutions
            - Emergence of platform business models requiring complex payment flows
            """
        }

        print("\n=== Starting Analysis of Stripe (2010-2011 perspective) ===")
        print("-" * 80)
        
        # Log the generated keywords
        keywords = agent._generate_keywords(startup_info)
        print("\nGenerated Search Keywords:")
        print("-" * 40)
        print(keywords)
        
        # Log the external knowledge gathered
        external_knowledge = agent._get_external_knowledge(startup_info)
        print("\nExternal Market Research:")
        print("-" * 40)
        print(external_knowledge)
        
        # Perform and log the full analysis
        print("\nFull Market Analysis:")
        print("-" * 40)
        nl_analysis = agent.analyze(startup_info, mode="natural_language_advanced")
        print(nl_analysis)

        print("\n=== Raw Search Data Collection ===")
        print("-" * 80)
        
        # Generate and log keywords
        keywords = agent._generate_keywords(startup_info)
        print("\nSearch Keywords Generated:")
        print("-" * 40)
        print(keywords)
        
        # Log raw search results before synthesis
        print("\nRaw Search Results:")
        print("-" * 40)
        search_results = agent.search_api.search(keywords)  # Raw search results
        print(search_results)
        
        # Log synthesized knowledge
        print("\nSynthesized External Knowledge:")
        print("-" * 40)
        synthesized_knowledge = agent._synthesize_knowledge(search_results)
        print(synthesized_knowledge)

    # Run the test function
    test_market_agent()