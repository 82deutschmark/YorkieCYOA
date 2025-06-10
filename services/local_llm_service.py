import os
import json
import requests
import logging
import base64
from typing import Dict, Any, Optional
import ollama

# Configure logging
logger = logging.getLogger(__name__)

class LocalLLMService:
    """Service for interacting with local LLM models via Ollama"""
    
    def __init__(self, model_name: str = "phi3:mini"):
        self.model_name = model_name
        self.client = ollama.Client()
        self._ensure_model_available()
    
    def _ensure_model_available(self):
        """Ensure the model is downloaded and available"""
        try:
            # Check if model is already available
            models = self.client.list()
            model_names = [model['name'] for model in models['models']]
            
            if self.model_name not in model_names:
                logger.info(f"Downloading {self.model_name} model...")
                self.client.pull(self.model_name)
                logger.info(f"Model {self.model_name} downloaded successfully")
            else:
                logger.info(f"Model {self.model_name} is available")
                
        except Exception as e:
            logger.error(f"Error checking/downloading model: {str(e)}")
            raise Exception(f"Failed to setup model {self.model_name}: {str(e)}")
    
    def analyze_artwork(self, image_url: str) -> Dict[str, Any]:
        """Analyze artwork using local vision model"""
        try:
            # Download the image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Get image metadata
            image_metadata = {
                "width": None,
                "height": None, 
                "format": None,
                "size_bytes": len(response.content)
            }
            
            # Try to get image dimensions and format
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(response.content))
                image_metadata.update({
                    "width": img.width,
                    "height": img.height,
                    "format": img.format.lower() if img.format else "unknown"
                })
            except Exception as img_err:
                logger.warning(f"Could not extract image metadata: {str(img_err)}")
            
            # Convert image to base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            
            # Create the analysis prompt
            system_prompt = """You are an expert analyzer of images for a "Choose Your Own Adventure" story universe.

The universe is centered around Uncle Mark's forest farm where two Yorkshire Terriers are the main characters:
- Pawel (male) - fearless, clever, impulsive
- Pawleen (female) - fearless, clever, thoughtful

Key characters in this universe:
1. HEROES:
   - The Yorkies (Pawel and Pawleen) - masters of the forest homestead and pasture
   - Chickens - clever birds with personality (30+ of them)
     - Big Red (the rooster, not very smart)
     - Main hens (clever): Birdadette, Henrietta, Birderella, Birdatha, Birdgit

2. NEUTRAL:
   - Turkeys - big, white, not very smart, always getting stuck

Analyze this image and determine if it shows a CHARACTER or a SCENE. Then provide detailed analysis.

For CHARACTERS, provide:
- character_name: string
- character_traits: array of strings
- character_role: "hero", "villain", or "neutral"
- plot_lines: array of story suggestions

For SCENES, provide:
- scene_type: string (e.g., "narrative", "choice", "action")  
- setting: string
- setting_description: string
- story_fit: string
- dramatic_moments: array of strings

Respond in JSON format with the appropriate keys based on the image type. Use snake_case for all field names."""

            user_prompt = "Please analyze this image for our Choose Your Own Adventure story:"
            
            # For Phi-3, we'll use text-only analysis since vision capabilities may be limited
            # We'll describe what we can infer from the image URL/context
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user', 
                        'content': f"{user_prompt}\n\nImage URL: {image_url}\nImage size: {image_metadata['size_bytes']} bytes"
                    }
                ],
                format='json'
            )
            
            # Parse the response
            content = response['message']['content']
            result = json.loads(content)
            
            # Add image metadata to the result
            result["image_metadata"] = image_metadata
            
            logger.debug("Successfully analyzed artwork with local LLM")
            return result
            
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Error downloading image: {str(req_err)}")
            raise Exception(f"Failed to download image from {image_url}: {str(req_err)}")
        except json.JSONDecodeError as json_err:
            logger.error(f"Error parsing LLM response: {str(json_err)}")
            raise Exception(f"Failed to parse LLM response: {str(json_err)}")
        except Exception as e:
            logger.error(f"Error analyzing artwork: {str(e)}")
            raise Exception(f"Failed to analyze artwork: {str(e)}")
    
    def generate_story(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate story content using local LLM"""
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a creative storyteller specializing in Choose Your Own Adventure stories. Generate engaging, interactive narratives with meaningful choices.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                format='json'
            )
            
            content = response['message']['content']
            result = json.loads(content)
            
            logger.debug("Successfully generated story with local LLM")
            return result
            
        except json.JSONDecodeError as json_err:
            logger.error(f"Error parsing story generation response: {str(json_err)}")
            raise Exception(f"Failed to parse story generation response: {str(json_err)}")
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            raise Exception(f"Failed to generate story: {str(e)}")
    
    def generate_image_description(self, analysis: Dict[str, Any]) -> str:
        """Generate a concise description of the analyzed image"""
        try:
            prompt = f"Based on this image analysis, write a concise, engaging description:\n{json.dumps(analysis, indent=2)}"
            
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a skilled writer. Create concise, vivid descriptions based on image analysis data.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"Error generating image description: {str(e)}")
            return "A scene from the adventure story."

# Global service instance
local_llm_service = None

def get_local_llm_service() -> LocalLLMService:
    """Get or initialize local LLM service"""
    global local_llm_service
    
    if local_llm_service is None:
        local_llm_service = LocalLLMService()
    
    return local_llm_service

# Convenience functions to match the OpenAI service interface
def analyze_artwork(image_url: str) -> Dict[str, Any]:
    """Analyze artwork using local LLM"""
    return get_local_llm_service().analyze_artwork(image_url)

def generate_image_description(analysis: Dict[str, Any]) -> str:
    """Generate a concise description of the analyzed image"""
    return get_local_llm_service().generate_image_description(analysis)