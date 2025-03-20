import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
import validators
import time
import pandas as pd
import io
import json

# Streamlit UI
st.title("AI Web Scraper")
st.write("Enter a website URL to scrape and analyze its content.")

url = st.text_input("Enter Website URL", help="Enter the complete URL including http:// or https://")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if not url:
        st.error("Please enter a URL")
    elif not validators.url(url):
        st.error("Please enter a valid URL")
    else:
        try:
            with st.spinner("Scraping the website... This may take a few moments."):
                # Scrape the website
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content
                st.success("Website scraped successfully!")

                # Display the DOM content in an expandable text box
                with st.expander("View Scraped Content"):
                    st.text_area("Content", cleaned_content, height=300)
                    
        except Exception as e:
            st.error(f"An error occurred while scraping: {str(e)}")
            st.info("Tips:\n- Check if the website is accessible\n- Try again in a few moments\n- Make sure the URL is correct")


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    st.write("---")
    st.subheader("Analyze Scraped Content")
    parse_description = st.text_area(
        "What would you like to know about the content?",
        help="Example: 'Extract all product prices' or 'Summarize the main points'"
    )

    if st.button("Analyze Content"):
        if not parse_description:
            st.warning("Please enter what you'd like to know about the content")
        else:
            try:
                with st.spinner("Analyzing the content..."):
                    # Parse the content with Ollama
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    
                    # Store the parsed result in session state
                    try:
                        # Try to parse the result as JSON
                        if isinstance(parsed_result, str):
                            st.session_state.parsed_data = json.loads(parsed_result)
                        else:
                            st.session_state.parsed_data = parsed_result
                    except json.JSONDecodeError:
                        # If not JSON, store as plain text
                        st.session_state.parsed_data = {"result": parsed_result}
                    
                    st.success("Analysis complete!")
                    st.write("Results:")
                    st.write(parsed_result)
                    
                    # Add export button if we have data
                    if "parsed_data" in st.session_state:
                        # Convert the parsed data to a DataFrame
                        if isinstance(st.session_state.parsed_data, dict):
                            df = pd.DataFrame([st.session_state.parsed_data])
                        elif isinstance(st.session_state.parsed_data, list):
                            df = pd.DataFrame(st.session_state.parsed_data)
                        else:
                            df = pd.DataFrame([{"result": str(st.session_state.parsed_data)}])
                        
                        # Create a download button for CSV
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="scraped_data.csv",
                            mime="text/csv",
                        )
                    
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.info("Please try again with a different query or check if the content was scraped properly")
