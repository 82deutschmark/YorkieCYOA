# Uncle Mark's Infinite Storybook

An AI-powered interactive storytelling platform that generates dynamic Choose Your Own Adventure narratives featuring Yorkshire Terriers Pawel and Pawleen on their forest farm adventures.

## 🌟 Features

### Core Storytelling
- **Dynamic Story Generation**: AI-powered narrative creation using OpenAI's GPT models
- **Character-Driven Adventures**: Stories featuring beloved farm characters with unique personalities
- **Interactive Choices**: Meaningful decision points that shape story direction
- **Branching Narratives**: Multiple story paths with diverse outcomes

### Character System
- **Rich Character Database**: Pre-analyzed character images with traits and roles
- **Character Selection**: Choose protagonists from available farm residents
- **Personality-Driven Stories**: Character traits influence narrative direction and available choices
- **Visual Character Cards**: Beautiful character displays with trait indicators

### Advanced Features
- **Image Analysis**: AI-powered character and scene analysis using computer vision
- **Story Persistence**: Save and continue adventures across sessions
- **Unity Game Integration**: API endpoints for external game client support
- **Debug Tools**: Comprehensive management interface for content creators

## 🏗️ Technology Stack

- **Backend**: Flask web framework with PostgreSQL database
- **AI Integration**: OpenAI GPT models for story generation and image analysis
- **Frontend**: Bootstrap 5 with custom CSS and vanilla JavaScript
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Deployment**: Replit with automatic scaling

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/uncle-marks-storybook.git
cd uncle-marks-storybook
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="your_postgresql_url"
export OPENAI_API_KEY="your_openai_api_key"
export SESSION_SECRET="your_session_secret"
```

4. Initialize the database:
```bash
python -c "from app import app, db; app.app_context().db.create_all()"
```

5. Run the application:
```bash
python main.py
```

The app will be available at `http://localhost:5000`

## 📖 Story Universe

### Main Characters
- **Pawel** (Male Yorkshire Terrier): Fearless, clever, and impulsive leader
- **Pawleen** (Female Yorkshire Terrier): Fearless, clever, and thoughtful strategist

### Supporting Cast
- **Big Red**: The well-meaning but not-so-bright rooster
- **The Clever Hens**: Birdadette, Henrietta, Birderella, Birdatha, and Birdgit
- **White Turkeys**: Large, friendly, but prone to getting into predicaments
- **Various Farm Animals**: Each with unique personalities and story roles

### Antagonists
- **Evil Squirrel Gangs**: Arrogant bullies who steal food and harass other animals
- **The Rat Wizard**: Forest-dwelling villain who steals eggs and enchants rodents
- **Enchanted Minions**: Mice and moles forced to help with villainous schemes

## 🎮 Usage

### Creating Stories
1. **Select a Character**: Choose one protagonist from the character gallery
2. **Set Story Parameters**: Pick conflict type, setting, narrative style, and mood
3. **Generate Adventure**: Let AI create your personalized story
4. **Make Choices**: Navigate through decision points to shape the narrative

### Story Options
- **Conflicts**: Mystery, rescue, adventure, friendship, rivalry, survival, discovery, protection
- **Settings**: Forest, farm, pasture, chicken coop, creek, barn, garden, meadow
- **Styles**: Playful, mysterious, heroic, cozy, adventurous, educational, humorous, dramatic
- **Moods**: Cheerful, suspenseful, peaceful, energetic, mysterious, heartwarming, comedic, inspiring

## 🔧 API Reference

### Unity Game Integration
The platform provides REST API endpoints for Unity game integration:

#### Story Management
- `GET /api/unity/story_node/{node_id}` - Retrieve story node with choices
- `POST /api/unity/choice/{choice_id}` - Process choice selection
- `GET /api/unity/user_progress/{user_id}` - Get user's current progress

#### Character System
- `GET /api/unity/characters` - List all available characters
- `GET /api/unity/story_branch/{node_id}` - Get complete story branch

#### Game State
- `POST /api/unity/save_game_state` - Save comprehensive game state
- `GET /api/unity/load_game_state/{user_id}` - Load saved game state
- `GET /api/unity/achievements/{user_id}` - Get user achievements

## 🛠️ Development

### Project Structure
```
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── models.py             # Database models
├── database.py           # Database configuration
├── services/
│   ├── openai_service.py # AI integration service
│   └── story_maker.py    # Story generation logic
├── api/
│   └── unity_routes.py   # Unity API endpoints
├── templates/            # HTML templates
├── static/              # CSS, JavaScript, assets
└── migrations/          # Database migrations
```

### Database Models
- **ImageAnalysis**: Character and scene data with AI analysis
- **StoryGeneration**: Generated story content and metadata
- **StoryNode**: Individual story segments in branching narratives
- **StoryChoice**: Decision points connecting story nodes
- **UserProgress**: Player progress tracking
- **Achievement**: Story achievement system

### Adding New Characters
1. Use the debug interface at `/debug`
2. Analyze character images with AI
3. Review and edit character traits
4. Save to database for story integration

## 🐛 Debug Tools

Access the debug interface at `/debug` for:
- **Image Analysis**: Process new character and scene images
- **Database Management**: View, edit, and manage stored content
- **Story Browser**: Review generated stories and choices
- **Health Monitoring**: Database connectivity and system status

## 📝 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `SESSION_SECRET`: Flask session encryption key
- `REPLIT_DEPLOYMENT`: Deployment mode indicator

### OpenAI Models
- **Story Generation**: GPT-4 Turbo for creative writing
- **Image Analysis**: GPT-4 Vision for character/scene analysis
- **Response Format**: JSON structured responses for consistent parsing

## 🚀 Deployment

The application is optimized for Replit deployment with:
- Automatic dependency management
- Environment variable configuration
- Database initialization
- Horizontal scaling support

### Replit Deployment
1. Import project to Replit
2. Configure secrets in Replit environment
3. Run the application
4. Access via generated Replit domain

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add tests for new features
- Update documentation for API changes
- Ensure database migrations are included

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for powerful AI models enabling dynamic storytelling
- Bootstrap team for responsive UI framework
- Flask community for excellent web framework
- PostgreSQL for reliable data storage

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check existing documentation
- Review debug tools for troubleshooting

---

*Created with ❤️ for interactive storytelling adventures*