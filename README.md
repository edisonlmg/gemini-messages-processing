# 🤖 gemini-messages-processing 🚀

Automated lead extraction from business chats. Uses Python and LLMs to turn messy chat history into clean, deduplicated buyer lists in tables.

## ✨ Overview

The `gemini-messages-processing` project is designed to powered how businesses manage leads from their WhatsApp conversations. It leverages the power of Large Language Models (LLMs) and Python to intelligently process unstructured chat data, identify potential buyers, and organize this information into structured, deduplicated tables. Say goodbye to manual data entry and hello to efficient lead management! 📈

## 🌟 Features

*   **Automated Lead Identification**: Automatically detects and extracts lead information from WhatsApp chat histories. 🕵️‍♀️
*   **LLM-Powered Classification**: Utilizes advanced LLMs for accurate classification and extraction of relevant data points. 🧠
*   **Data Deduplication**: Ensures your buyer lists are clean and free from duplicate entries. 🧹
*   **Structured Output**: Transforms messy chat data into organized tables, ready for CRM integration or further analysis. 📊
*   **Python-Based**: Built with Python, offering flexibility and ease of integration. 🐍

## 🛠️ Technologies Used

*   **Python**: The core programming language.
*   **Large Language Models (LLMs)**: For natural language understanding and data extraction.

## 🚀 Getting Started

Follow these steps to get your `gemini-messages-processing` up and running.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/edisonlmg/gemini-messages-processing.git
    cd gemini-messages-processing
    ```
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **API Keys**: You will need API keys for the LLM service you intend to use (e.g., Google Gemini API, OpenAI API).
    Set your API key as an environment variable:
    ```bash
    export LLM_API_KEY="your_api_key_here"
    ```

## 💡 Usage

1.  **Prepare your chat data**: Ensure your WhatsApp chat history is in a readable format (e.g., exported text files, JSON).
2.  **Run the classifier**:
    ```bash
    python main.py --chat_file "path/to/your/chat.txt" --output_format "csv"
    ```
3.  **Review the output**: The processed buyer list will be generated in the specified format.

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements or new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeature`).
6.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 📞 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---
