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
        ("😎", "GenZ fresh style"),
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
    character_prompt = ""
    if character_info:
        # Process selected character
        character_prompt = (
            f"\nMain Character: {character_info['name']}\n"
            f"Role: {character_info.get('role', 'protagonist')}\n"
            f"Traits: {', '.join(character_info.get('character_traits', []))}\n"
            f"Visual Description: {character_info.get('style', '')}\n"
            f"Potential Plot Lines:\n"
        )
        for plot in character_info.get('plot_lines', []):
            character_prompt += f"- {plot}\n"

    # Add context from previous choices if available
    context_prompt = ""
    if story_context and previous_choice:
        context_prompt = (
            f"\nPrevious story context: {story_context}\n"
            f"Player chose: {previous_choice}\n"
            "Continue the story based on this choice, maintaining consistency with previous events."
        )

    # Construct the main prompt
    prompt = (
        f"Primary Conflict: {final_conflict}\n"
        f"Setting: {final_setting}\n"
        f"Narrative Style: {final_narrative}\n"
        f"Mood: {final_mood}\n"
        f"{character_prompt}\n"
        f"{context_prompt}\n\n"
        "Create an engaging interactive story segment for our Choose Your Own Adventure story. "
        "This story takes place in Uncle Mark's forest farm, a magical place where animals have distinct personalities.\n\n"
        "Remember these important story elements:\n"
        "- The farm's main protectors are two Yorkshire terriers: Pawel (impulsive male) and Pawleen (thoughtful female)\n"
        "- The farm has chickens led by Big Red (the dumb rooster) and his clever hens (Birdadette, Henrietta, etc.)\n"
        "- White turkeys who aren't very smart and often get stuck in silly situations\n"
        "- Evil squirrel gangs who think they're superior to other animals\n"
        "- A devious rat wizard who steals eggs and vegetables for his potions\n"
        "- Mice and moles who are bullied by squirrels into helping them\n\n"
        "Your story segment should:\n"
        "1. Continue the ongoing narrative, incorporating the selected character naturally\n"
        "2. Use the character's established traits and suggested plot lines\n"
        "3. Maintain consistency with any previous story context\n"
        "4. End with exactly two distinct and meaningful choices that:\n"
        "   - Lead to significantly different potential outcomes\n"
        "   - Reflect the character's established traits\n"
        "   - Avoid dead ends or quick story conclusions\n"
        "5. Provide clear consequences for each choice\n\n"
        "Format the response as a JSON object with the following structure:\n"
        "{\n"
        "  'title': 'Episode title',\n"
        "  'story': 'The story text',\n"
        "  'choices': [\n"
        "    {'text': 'First choice description', 'consequence': 'Brief hint about outcome'},\n"
        "    {'text': 'Second choice description', 'consequence': 'Brief hint about outcome'}\n"
        "  ],\n"
        "  'characters': ['List of character names featured in this segment']\n"
        "}"
    )

    try:
        # Call OpenAI API to generate the story
        # Note: gpt-4o is the newest model, released May 13, 2024
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a master storyteller creating stories set in Uncle Mark's forest farm. "
                        "These stories are for kids and feature the adventures of the farm's animal residents. "
                        "Each response should continue the narrative while respecting the established universe "
                        "and character traits. Focus on creating meaningful choices that branch the story "
                        "in interesting ways while maintaining the playful and engaging tone of the world."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
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