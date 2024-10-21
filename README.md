# GitHub Repository Manager

This script allows you to manage your GitHub repositories by fetching all your repositories and selectively deleting them.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Setup

1. Clone this repository or download the files.

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the same directory as the script with the following content:

   ```
   GITHUB_TOKEN=your_github_token_here
   GITHUB_USERNAME=your_github_username_here
   ```

   Replace `your_github_token_here` with your GitHub personal access token and `your_github_username_here` with your GitHub username.

## Usage

Run the script with the following command:

```
python main.py
```

Follow the prompts to select and delete repositories.

## Warning

Deleting repositories is irreversible. Use this script with caution.

## License

This project is open source and available under the [MIT License](LICENSE).
