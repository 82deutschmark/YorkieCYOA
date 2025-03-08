import os
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)

# Get OpenAI API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    logger.warning("OpenAI API key not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Default story options
STORY_OPTIONS = {
    "conflicts": [
        ("🐿️", "Squirrel gang's mischief"),
        ("🧙‍♂️", "Rat wizard's devious plots"),
        ("🦃", "Turkey's clumsy adventures"),
        ("🐔", "Chicken's clever conspiracies")
    ],
    "settings": [
        ("🌳", "Deep Forest"),
        ("🌾", "Sunny Pasture"),
        ("🏡", "Homestead"),
        ("🌲", "Mysterious Woods")
    ],
    "narrative_styles": [
        ("😎", "Gen Z teen style"),
        ("✌️", "Old hippie 1960s vibe"),
        ("🤘", "Mix of both")
    ],
    "moods": [
        ("😄", "Joyful and playful"),
        ("😲", "Thrilling and mysterious"),
        ("😎", "Cool and laid-back"),
        ("😂", "Funny and quirky")
    ]
}

def get_story_options() -> Dict[str, List[Tuple[str, str]]]:
    """Return available story options for UI display"""
    return STORY_OPTIONS

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
    story_context: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a story based on selected or custom parameters and character info"""
    if not api_key:
        raise ValueError("OpenAI API key not found. Please add it to your environment variables.")

    # Use custom values if provided, otherwise use selected options
    final_conflict = custom_conflict or conflict
    final_setting = custom_setting or setting
    final_narrative = custom_narrative or narrative_style
    final_mood = custom_mood or mood

    # Build character information for the prompt
    selected_character_prompt = ""
    if character_info and character_info.get('name'):
        # Extract character traits with fallback options for different data structures
        traits = character_info.get('character_traits', [])
        if not traits and 'traits' in character_info:
            traits = character_info['traits']
        
        # Extract plot lines with fallback options
        plot_lines = character_info.get('plot_lines', [])
        if not plot_lines and 'plot_lines' in character_info:
            plot_lines = character_info['plot_lines']
        
        # Get character style/visual description
        style = character_info.get('style', '')
        if not style and character_info.get('visual_description'):
            style = character_info.get('visual_description')
            
        # Build the character prompt section with all available data
        selected_character_prompt = (
            f"\nSelected Character to Feature:\n"
            f"Name: {character_info['name']}\n"
            f"Role: {character_info.get('role', 'neutral')}\n"
            f"Traits: {', '.join(traits)}\n"
            f"Visual Description: {style}\n"
        )
        
        # Add plot lines with emphasis to ensure they're incorporated into the story
        if plot_lines:
            selected_character_prompt += f"Suggested Plot Lines (MUST USE AT LEAST ONE):\n"
            for plot in plot_lines:
                selected_character_prompt += f"- {plot}\n"

    # Add context from previous choices if available
    context_prompt = ""
    if story_context and previous_choice:
        context_prompt = (
            f"\nPrevious story context: {story_context}\n"
            f"Player chose: {previous_choice}\n"
            "Continue the story based on this choice, maintaining consistency with previous events."
        )

    # Core story universe description
    universe_prompt = (
        "This story takes place in Uncle Mark's forest farm, where animals have distinct personalities "
        "and adventures happen daily. The main cast includes:\n\n"
        "Core Characters:\n"
        "- Pawel and Pawleen: Two Yorkshire terriers who protect the farm. Pawel is impulsive and fearless, "
        "while Pawleen is thoughtful and clever.\n"
        "- Big Red: The not-so-bright rooster who leads the chicken coop\n"
        "- The Clever Hens: Birdadette, Henrietta, and others who actually run things\n"
        "- The White Turkeys: Well-meaning but big and clumsy prone to getting into silly situations\n\n"
        "Antagonists:\n"
        "- Evil Squirrel Gangs: Think they're superior to other animals, bully others, and steal food\n"
        "- The Rat Wizard: Lives in the woods, steals eggs and vegetables for his potions, enchants other rodents to do his bidding\n"
        "- Various mice and moles: Forced by squirrels to help with their schemes\n"
    )

    # Construct the main prompt
    prompt = (
        f"Primary Conflict: {final_conflict}\n"
        f"Setting: {final_setting}\n"
        f"Narrative Style: {final_narrative}\n"
        f"Mood: {final_mood}\n\n"
        f"{universe_prompt}\n"
        f"{selected_character_prompt}\n"
        f"{context_prompt}\n\n"
        "Create an engaging story segment that:\n"
        "1. Features Pawel and/or Pawleen as the main story drivers\n"
        "2. Introduces the selected character (if provided) into the farm's ongoing adventures\n"
        "3. IMPORTANT: If plot lines are provided for the character, you MUST incorporate at least one into the story\n"
        "4. Maintains the established personalities and relationships\n"
        "5. Uses the character's traits to guide their behavior and dialogue\n"
        "6. Provides exactly two meaningful choice options that:\n"
        "   - Lead to different potential outcomes\n"
        "   - Stay true to the characters' established traits\n"
        "   - Relate to at least one of the plot lines if provided\n"
        "   - Avoid dead ends or quick conclusions\n"
        "7. Include clear consequences for each choice that follow from the plot lines\n\n"
        "Format the response as a JSON object with:\n"
        "{\n"
        "  'title': 'Episode title',\n"
        "  'story': 'The story text',\n"
        "  'choices': [\n"
        "    {'text': 'First choice', 'consequence': 'Brief outcome hint'},\n"
        "    {'text': 'Second choice', 'consequence': 'Brief outcome hint'}\n"
        "  ],\n"
        "  'characters': ['List of character names featured']\n"
        "}"
    )

    try:
        # Note: gpt-4o is the newest model, released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a master storyteller creating stories set in Uncle Mark's forest farm. "
                        "Your stories feature the adventures of the farm's animal residents, "
                        "especially Pawel and Pawleen the Yorkshire terriers. Keep the tone playful and engaging, "
                        "with clear moral lessons about friendship, courage, and standing up to bullies."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            response_format={"type": "json_object"}
        )

        # Parse and return the generated story
        result = json.loads(response.choices[0].message.content)
        return {
            "story": json.dumps(result),  # Convert dict to JSON string for database storage
            "conflict": final_conflict,
            "setting": final_setting,
            "narrative_style": final_narrative,
            "mood": final_mood
        }

    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise Exception(f"Failed to generate story: {str(e)}")