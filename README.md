# Quiz Video Generator

A powerful tool to automatically generate engaging quiz videos from content. This project combines video processing, interactive quiz creation, and multimedia integration to produce educational video content.

## Table of Contents

- [Features](#features)
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

✨ **Core Capabilities:**
- 📹 Automatic video generation from quiz content
- 🎯 Interactive quiz creation and management
- 🎨 Customizable templates and styling
- 🔊 Multi-language support and text-to-speech integration
- ⚡ Batch processing for multiple quizzes
- 📊 Analytics and performance tracking
- 🎬 Video editing and enhancement tools
- 💾 Multiple output format support (MP4, WebM, etc.)
- 🔐 Secure content handling and encryption

## Project Overview

Quiz Video Generator is designed to streamline the creation of educational video content with embedded quizzes. It provides a comprehensive solution for:

- **Content Input**: Accept quiz data in various formats (JSON, CSV, XML)
- **Video Processing**: Leverage FFmpeg for video manipulation and rendering
- **Quiz Integration**: Seamlessly embed quiz elements into video timelines
- **Output Generation**: Produce publication-ready video files
- **Metadata Management**: Track and organize generated content

### Use Cases

- Educational institutions creating course material
- Training departments producing employee onboarding videos
- Content creators building interactive educational content
- E-learning platforms needing automated video production

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.8 or higher
- **FFmpeg** 4.2 or higher
- **Node.js** 14.0+ (if using web interface)
- **Git** 2.25+
- **pip** (Python package manager)
- **Virtual Environment** tools (venv or conda)

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended for batch processing)
- **Storage**: At least 10GB free disk space
- **Processor**: Multi-core processor recommended
- **OS**: Windows, macOS, or Linux

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rahulbhatforu/quiz-video-generator.git
cd quiz-video-generator
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (if not already installed)
# On Ubuntu/Debian:
sudo apt-get install ffmpeg

# On macOS (using Homebrew):
brew install ffmpeg

# On Windows (using Chocolatey):
choco install ffmpeg
```

### 4. Verify Installation

```bash
python -m quiz_video_generator --version
ffmpeg -version
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=localhost
API_PORT=5000
API_KEY=your_api_key_here

# Video Processing
VIDEO_QUALITY=high
VIDEO_FORMAT=mp4
VIDEO_FPS=30
VIDEO_RESOLUTION=1920x1080

# Storage
OUTPUT_DIR=./outputs
TEMP_DIR=./temp
CACHE_DIR=./cache

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Features
ENABLE_TEXT_TO_SPEECH=true
ENABLE_BATCH_PROCESSING=true
MAX_BATCH_SIZE=10

# Database (if applicable)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quiz_generator
DB_USER=postgres
DB_PASSWORD=your_password
```

### Configuration File

Create a `config.yaml` for advanced settings:

```yaml
video:
  quality: high
  fps: 30
  resolution: 1920x1080
  codec: libx264
  bitrate: 8000k

quiz:
  timeout: 30
  shuffle_questions: true
  show_feedback: true
  randomize_options: true

output:
  formats:
    - mp4
    - webm
  watermark: true
  auto_optimize: true

logging:
  level: INFO
  format: json
  retention_days: 30
```

## Usage

### Basic Usage

#### 1. Creating a Quiz Video from JSON

```bash
python -m quiz_video_generator create \
  --input quiz_data.json \
  --output quiz_video.mp4 \
  --template default
```

#### 2. Command Line Interface

```bash
# Generate a quiz video
python -m quiz_video_generator generate \
  --quiz-file quiz.json \
  --output-file output.mp4 \
  --quality high

# Batch process multiple quizzes
python -m quiz_video_generator batch \
  --input-dir ./quizzes \
  --output-dir ./videos

# List available templates
python -m quiz_video_generator templates

# Validate quiz data
python -m quiz_video_generator validate --file quiz.json
```

### Python API

```python
from quiz_video_generator import QuizVideoGenerator

# Initialize generator
generator = QuizVideoGenerator(
    template='default',
    quality='high',
    output_format='mp4'
)

# Load quiz data
quiz_data = generator.load_quiz('quiz_data.json')

# Generate video
video_path = generator.generate(
    quiz_data=quiz_data,
    output_path='./output/quiz_video.mp4',
    background_music='assets/music.mp3',
    transitions='fade'
)

print(f"Video generated: {video_path}")
```

### Advanced Usage

#### Custom Template

```python
from quiz_video_generator import CustomTemplate

template = CustomTemplate(
    name='my_template',
    colors={
        'primary': '#007AFF',
        'secondary': '#FF3B30',
        'background': '#FFFFFF'
    },
    fonts={
        'title': 'Arial Bold 48px',
        'body': 'Arial 24px'
    }
)

generator = QuizVideoGenerator(template=template)
```

#### Batch Processing

```python
from quiz_video_generator import BatchProcessor

processor = BatchProcessor(
    max_workers=4,
    retry_failed=True,
    log_progress=True
)

results = processor.process(
    input_directory='./quizzes',
    output_directory='./videos',
    config='config.yaml'
)
```

## Project Structure

```
quiz-video-generator/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── config.yaml.example
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── cli.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   ├── processor.py
│   │   └── validator.py
│   │
│   ├── video/
│   │   ├── __init__.py
│   │   ├── editor.py
│   │   ├── effects.py
│   │   └── renderer.py
│   │
│   ├── quiz/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── builder.py
│   │   └── serializer.py
│   │
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── default/
│   │   └── custom/
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── config.py
│   │   └── helpers.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── routes.py
│       └── handlers.py
│
├── tests/
│   ├── __init__.py
│   ├── test_generator.py
│   ├── test_video.py
│   ├── test_quiz.py
│   └── fixtures/
│
├── examples/
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   ├── batch_processing.py
│   └── sample_quizzes/
│
├── assets/
│   ├── templates/
│   ├── fonts/
│   ├── music/
│   └── images/
│
└── docs/
    ├── api.md
    ├── templates.md
    ├── troubleshooting.md
    └── faq.md
```

## API Reference

### QuizVideoGenerator Class

```python
class QuizVideoGenerator:
    def __init__(self, template='default', quality='high', output_format='mp4'):
        """Initialize the generator with configuration."""
        pass
    
    def load_quiz(self, path: str) -> dict:
        """Load quiz data from file."""
        pass
    
    def validate_quiz(self, quiz_data: dict) -> bool:
        """Validate quiz data structure."""
        pass
    
    def generate(self, quiz_data: dict, output_path: str, **kwargs) -> str:
        """Generate video from quiz data."""
        pass
    
    def set_template(self, template: str) -> None:
        """Change the video template."""
        pass
    
    def get_progress(self) -> dict:
        """Get generation progress information."""
        pass
```

### Quiz Data Format

```json
{
  "metadata": {
    "title": "Python Basics Quiz",
    "description": "Test your Python knowledge",
    "duration": 300,
    "created_at": "2025-12-28T13:58:59Z"
  },
  "questions": [
    {
      "id": "q1",
      "type": "multiple_choice",
      "question": "What is Python?",
      "options": [
        "A programming language",
        "A snake",
        "A tool",
        "A framework"
      ],
      "correct_answer": 0,
      "explanation": "Python is a high-level programming language.",
      "duration": 15,
      "points": 10
    }
  ],
  "settings": {
    "shuffle_questions": false,
    "show_feedback": true,
    "randomize_options": false
  }
}
```

## Examples

### Example 1: Simple Quiz Video

```python
from quiz_video_generator import QuizVideoGenerator

generator = QuizVideoGenerator()
quiz_data = generator.load_quiz('sample_quiz.json')
video_path = generator.generate(quiz_data, 'output.mp4')
print(f"Video created: {video_path}")
```

### Example 2: Custom Styling

```python
from quiz_video_generator import QuizVideoGenerator, CustomTemplate

template = CustomTemplate(
    colors={'primary': '#007AFF', 'background': '#F5F5F5'},
    fonts={'title': 'Roboto Bold 48px'}
)

generator = QuizVideoGenerator(template=template, quality='ultra')
video_path = generator.generate(quiz_data, 'styled_video.mp4')
```

### Example 3: Batch Processing

```python
from quiz_video_generator import BatchProcessor

processor = BatchProcessor(max_workers=4)
results = processor.process('./quizzes', './videos')
print(f"Processed {len(results)} videos")
```

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 src/

# Format code
black src/
```

### Code Standards

- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation accordingly
- Ensure all tests pass before submitting PR

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

### Getting Help

- 📖 **Documentation**: Check the [docs](./docs) folder
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Email**: Contact the maintainers directly

### Troubleshooting

Common issues and solutions:

**FFmpeg not found**
```bash
# Ensure FFmpeg is installed and in PATH
ffmpeg -version
```

**Memory issues with large videos**
```bash
# Use quality reduction
--quality low
# Or process in smaller chunks
--chunk-size 100
```

**Video codec errors**
```bash
# Verify codec support
ffmpeg -codecs | grep h264
```

For more detailed troubleshooting, see [troubleshooting.md](./docs/troubleshooting.md)

### Performance Tips

- Use appropriate video quality based on output platform
- Enable batch processing for multiple videos
- Consider using GPU acceleration if available
- Monitor memory usage for large projects

---

**Last Updated**: 2025-12-28

**Maintainer**: [@rahulbhatforu](https://github.com/rahulbhatforu) 

For more information and updates, visit the [project repository](https://github.com/rahulbhatforu/quiz-video-generator)
