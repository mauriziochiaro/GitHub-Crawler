### README.md

```markdown
# GitHub Crawler Chatbot

## Description
GitHub Crawler Chatbot is an interactive application designed to analyze GitHub repositories. It offers insights into various aspects of projects including code quality, structure, documentation, and design. The chatbot interface allows users to interact with the GitHub API and OpenAI's GPT model to fetch information and suggestions for repository improvement.

## Features
- Chat interface for real-time interaction with GitHub repositories.
- Analysis and suggestions for code improvement.
- Dark mode support for code blocks in the chat display.
- Ability to download chat history as a Markdown file.

## Prerequisites
- Python 3.8 or higher

## Installation
To set up the GitHub Crawler Chatbot on your local machine, follow these steps:

1. **Clone the Repository**
   ```
   git clone https://github.com/mauriziochiaro/GitHub-Crawler.git
   ```

2. **Install Dependencies**
   Navigate to the project directory and install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Configuration and Usage

### GitHub API Access

The GitHub Crawler Chatbot can access both public and private GitHub repositories. To enable access to private repositories, you need to provide a GitHub access token with the necessary permissions.

1. **Generate a GitHub Access Token**:
   - Go to your GitHub account settings.
   - Navigate to Developer settings -> Personal access tokens.
   - Generate a new token with the appropriate scopes (permissions). For repository access, select `repo`. This will allow the chatbot to access private repositories you have access to.

2. **Configure the Application with Your Access Token**:
   - Open the `config.py` file in the project root.
   - Replace `ghp_xxx` with your generated GitHub access token:
     ```python
     # GITHUB API
     access_token = 'ghp_yourGeneratedAccessToken'
     headers = {'Authorization': f'token {access_token}'}
     ```

3. **Set Up OpenAI API Key**:
   - Similarly, set your OpenAI API key in the `config.py` file:
     ```python
     # OPENAI API
     OPENAI_API_KEY = "yourOpenAIApiKey"
     MODEL = "gpt-3.5-turbo-1106"
     MAX_TOKENS = 5000
     ```

### Running the Chatbot

To use the chatbot:
1. Start the application by running `python main.py`.
2. Enter the URL of the GitHub repository you wish to analyze in the chat interface.
   - For public repositories, simply enter the URL.
   - For private repositories, ensure your GitHub access token is configured as described above.

## Contributing
Contributions to the GitHub Crawler Chatbot are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
- OpenAI for the GPT models.
- GitHub API for repository data access.
```
