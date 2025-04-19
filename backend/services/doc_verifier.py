"""
Document verification service that uses OCR and document understanding models
to extract information from ID documents and verify against provided details.
"""

import logging
import os
import json
import ast
from PIL import Image
from io import BytesIO
from typing import Dict, Any, Optional, Tuple

# Configure logging
logger = logging.getLogger(__name__)

# Global variables to store model instances
trocr_processor = None
trocr_model = None
donut_processor = None
donut_model = None
models_loaded = False

def load_models():
    """
    Load ML models for document verification.
    """
    global trocr_processor, trocr_model, donut_processor, donut_model, models_loaded
    
    if models_loaded:
        return
    
    try:
        logger.info("Loading document verification models...")
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel, DonutProcessor
        
        # Load TrOCR model for general OCR
        trocr_processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-stage1")
        trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-stage1")
        
        # Load Donut model for structured document extraction
        donut_processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
        donut_model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")
        
        models_loaded = True
        logger.info("Document verification models loaded successfully")
    except Exception as e:
        logger.error(f"Error loading document verification models: {str(e)}")
        raise RuntimeError(f"Failed to load document verification models: {str(e)}")

def ocr_text(image: Image.Image) -> str:
    """Extract text from image using TrOCR"""
    if not models_loaded:
        load_models()
    
    try:
        pixel_values = trocr_processor(images=image, return_tensors="pt").pixel_values
        generated_ids = trocr_model.generate(pixel_values)
        return trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    except Exception as e:
        logger.error(f"OCR text extraction error: {str(e)}")
        return ""

def extract_fields(image: Image.Image) -> Dict[str, Any]:
    """Extract structured fields from document image using Donut"""
    if not models_loaded:
        load_models()
    
    try:
        # Donut expects image + prompt to output JSON-like key/values
        prompt = "<s_doc>extract</s_doc>"
        pixel_values = donut_processor(image, return_tensors="pt").pixel_values
        generated_ids = donut_model.generate(
            pixel_values, 
            decoder_input_ids=donut_processor.tokenizer(prompt, return_tensors="pt").input_ids
        )
        
        raw = donut_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Try to parse the result as JSON or dict
        try:
            # First try to evaluate as Python literal (safer than eval)
            result = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            # Fallback to JSON parsing
            try:
                result = json.loads(raw)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse extraction result: {raw}")
                result = {}
                
        return result
    except Exception as e:
        logger.error(f"Field extraction error: {str(e)}")
        return {}

def match_data(extracted: Dict[str, str], manual: Dict[str, str]) -> Dict[str, Any]:
    """Match extracted data with manually entered data using fuzzy matching"""
    try:
        # Import fuzzywuzzy for string matching
        from fuzzywuzzy import fuzz
        
        scores = {}
        for key in manual:
            if not manual[key]:  # Skip empty fields
                continue
                
            extracted_value = extracted.get(key, "")
            manual_value = manual[key]
            
            # If either value is empty and the other isn't, score is 0
            if not extracted_value or not manual_value:
                scores[key] = 0
            else:
                scores[key] = fuzz.token_set_ratio(extracted_value, manual_value)
        
        # Calculate overall confidence and status
        if not scores:
            confidence = 0
        else:
            confidence = sum(scores.values()) / (len(scores) * 100) * 100
            
        status = "Passed" if scores and min(scores.values()) >= 90 else "Failed"
        
        return {
            "scores": scores,
            "confidence": confidence,
            "status": status
        }
    except Exception as e:
        logger.error(f"Data matching error: {str(e)}")
        return {
            "scores": {},
            "confidence": 0,
            "status": "Failed"
        }

def verify_document(image_data: bytes, manual_data: Dict[str, str]) -> Dict[str, Any]:
    """
    Verify a document by comparing extracted data with manually entered data
    
    Args:
        image_data: Binary image data
        manual_data: Dictionary with manually entered data (name, dob, id_number, etc.)
        
    Returns:
        Dictionary with verification results
    """
    try:
        # Convert binary data to PIL Image
        img = Image.open(BytesIO(image_data)).convert("RGB")
        
        # Extract fields from document
        extracted = extract_fields(img)
        
        # Fallback to OCR if extraction failed or returned empty
        if not extracted:
            text = ocr_text(img)
            logger.info(f"Fallback to OCR text: {text[:100]}...")
            
            # Simple heuristic extraction based on OCR text
            # This would be better with regex patterns specific to document types
            extracted = {"raw_text": text}
        
        # Match extracted data with manual data
        result = match_data(extracted, manual_data)
        
        return {
            "extracted": extracted,
            "match": result["scores"],
            "confidence": result["confidence"],
            "status": result["status"]
        }
    except Exception as e:
        logger.error(f"Document verification error: {str(e)}")
        return {
            "extracted": {},
            "match": {},
            "confidence": 0,
            "status": "Failed",
            "error": str(e)
        }

# Try to load models at module import time
try:
    load_models()
except Exception as e:
    logger.warning(f"Models will be loaded on first use. Error at startup: {e}")

# Create a singleton instance for easy import
doc_verification_service = {
    "verify_document": verify_document,
    "ocr_text": ocr_text,
    "extract_fields": extract_fields,
    "match_data": match_data
} 