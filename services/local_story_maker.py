import os
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from services.local_llm_service import get_local_llm_service

# Configure logging
logger = logging.getLogger(__name__)

def get_story_options() -> Dict[str, List[Tuple[str, str]]]:
    """Return available story options for UI display"""
    return {
        "conflicts": [
            ("mystery", "A mysterious disappearance or strange occurrence"),
            ("rescue", "Someone or something needs to be rescued"),
            ("adventure", "An exciting journey or quest"),
            ("friendship", "Building bonds and working together"),
            ("rivalry", "Competition between characters"),
            ("survival", "Overcoming dangerous situations"),
            ("discovery", "Finding something new or important"),
            ("protection", "Defending home or loved ones")
        ],
        "settings": [
            ("forest", "Deep in the enchanted forest"),
            ("farm", "Around Uncle Mark's homestead"),
            ("pasture", "In the open grazing fields"),
            ("chicken_coop", "Near the bustling chicken community"),
            ("creek", "By the babbling forest creek"),
            ("barn", "Inside the old wooden barn"),
            ("garden", "Among the vegetable patches"),
            ("meadow", "In the sunny wildflower meadow")
        ],
        "narrative_styles": [
            ("playful", "Light-hearted and fun"),
            ("mysterious", "Suspenseful and intriguing"),
            ("heroic", "Bold and courageous"),
            ("cozy", "Warm and comfortable"),
            ("adventurous", "Thrilling and exciting"),
            ("educational", "Learning through experience"),
            ("humorous", "Funny and entertaining"),
            ("dramatic", "Intense and emotional")
        ],
        "moods": [
            ("cheerful", "Happy and optimistic"),
            ("suspenseful", "Tense and exciting"),
            ("peaceful", "Calm and serene"),
            ("energetic", "Active and lively"),
            ("mysterious", "Dark and intriguing"),
            ("heartwarming", "Touching and emotional"),
            ("comedic", "Funny and amusing"),
            ("inspiring", "Uplifting and motivating")
        ]
    }

def generate_story(
    conflict: str,
    setting: str,
    narrative_style: str,
    mood: str,
    character_info: Optional[Dict[str, Any]] = None,
    custom_conflict: Optional[str] = None,
    custom_setting: Optional[str] = None,
    custom_narrative: Optional[str] = None,
    custom_mood: Optional[str] = None,
    previous_choice: Optional[str] = None,
    story_context: Optional[str] = None,
    additional_characters: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generate a story based on selected or custom parameters and character info"""
    
    try:
        # Use custom parameters if provided, otherwise use selected ones
        final_conflict = custom_conflict if custom_conflict else conflict
        final_setting = custom_setting if custom_setting else setting
        final_narrative = custom_narrative if custom_narrative else narrative_style
        final_mood = custom_mood if custom_mood else mood
        
        # Build the character context
        character_context = ""
        if character_info:
            if character_info.get('character_name'):
                character_context += f"Main character: {character_info['character_name']}\n"
            if character_info.get('character_traits'):
                character_context += f"Traits: {', '.join(character_info['character_traits'])}\n"
            if character_info.get('character_role'):
                character_context += f"Role: {character_info['character_role']}\n"
        
        # Add additional characters
        if additional_characters:
            character_context += "\nAdditional characters:\n"
            for char in additional_characters:
                if char.get('character_name'):
                    character_context += f"- {char['character_name']}"
                    if char.get('character_traits'):
                        character_context += f" ({', '.join(char['character_traits'])})"
                    character_context += "\n"
        
        # Build context for continuing stories
        continuation_context = ""
        if previous_choice and story_context:
            continuation_context = f"\nPrevious story context:\n{story_context}\n\nPlayer's last choice: {previous_choice}\n"
        
        # Create the story generation prompt
        prompt = f"""Create an engaging Choose Your Own Adventure story segment with the following parameters:

STORY UNIVERSE: Uncle Mark's forest farm with Yorkshire Terriers Pawel and Pawleen as main characters.

PARAMETERS:
- Conflict: {final_conflict}
- Setting: {final_setting}  
- Narrative Style: {final_narrative}
- Mood: {final_mood}

{character_context}

{continuation_context}

KEY CHARACTERS TO POTENTIALLY INCLUDE:
- Pawel (male Yorkshire Terrier) - fearless, clever, impulsive
- Pawleen (female Yorkshire Terrier) - fearless, clever, thoughtful  
- Big Red (rooster) - not very smart but well-meaning
- Chickens: Birdadette, Henrietta, Birderella, Birdatha, Birdgit (all clever)
- Turkeys - big, white, not very smart, always getting stuck

REQUIREMENTS:
1. Write 3-4 paragraphs of engaging narrative (200-300 words)
2. End with a decision point
3. Provide exactly 3 meaningful choices that affect the story direction
4. Each choice should lead to different consequences
5. Keep the tone appropriate for all ages
6. Stay true to the character personalities

Respond in JSON format with:
{{
    "narrative": "The story text",
    "choices": [
        {{"text": "Choice 1 description", "consequence_hint": "Brief hint about outcome"}},
        {{"text": "Choice 2 description", "consequence_hint": "Brief hint about outcome"}},
        {{"text": "Choice 3 description", "consequence_hint": "Brief hint about outcome"}}
    ],
    "setting_details": "Description of the current scene setting",
    "character_focus": "Which characters are prominently featured",
    "tension_level": "low/medium/high"
}}"""

        # Generate the story using local LLM
        llm_service = get_local_llm_service()
        result = llm_service.generate_story(prompt)
        
        # Validate the response structure
        required_fields = ['narrative', 'choices', 'setting_details', 'character_focus', 'tension_level']
        for field in required_fields:
            if field not in result:
                logger.warning(f"Missing field '{field}' in story generation response")
                if field == 'narrative':
                    result[field] = "The adventure continues..."
                elif field == 'choices':
                    result[field] = [
                        {"text": "Continue the adventure", "consequence_hint": "See what happens next"},
                        {"text": "Take a different path", "consequence_hint": "Explore new possibilities"},
                        {"text": "Return to safety", "consequence_hint": "Play it safe"}
                    ]
                else:
                    result[field] = "Unknown"
        
        # Ensure choices is a list with at least 3 options
        if not isinstance(result.get('choices'), list) or len(result['choices']) < 3:
            result['choices'] = [
                {"text": "Continue forward", "consequence_hint": "Push ahead with determination"},
                {"text": "Look for another way", "consequence_hint": "Seek alternative solutions"},
                {"text": "Call for help", "consequence_hint": "Get assistance from friends"}
            ]
        
        logger.info(f"Successfully generated story with conflict: {final_conflict}, setting: {final_setting}")
        return result
        
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        
        # Return a fallback story structure
        fallback_setting = custom_setting if custom_setting else setting if 'setting' in locals() else "forest"
        return {
            "narrative": "Pawel and Pawleen stood at the forest edge, their keen eyes scanning the horizon. Something interesting was about to happen, and they could feel the excitement building. The adventure was just beginning, and they needed to decide their next move carefully.",
            "choices": [
                {"text": "Investigate the mysterious sound", "consequence_hint": "Discover something unexpected"},
                {"text": "Gather more information first", "consequence_hint": "Learn before acting"},
                {"text": "Rally the other animals", "consequence_hint": "Seek help from friends"}
            ],
            "setting_details": fallback_setting,
            "character_focus": "Pawel and Pawleen",
            "tension_level": "medium"
        }