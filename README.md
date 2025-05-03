<!-- 1. Creating the virtual env

    1.1. Pre-requisits:

    - `sudo apt install python3-venv`

    1.2. `python3 -m venv .venv`

    1.3. `source .venv/bin/activate`

    1.4. `deactivate`

2. Install the requirements from the requirements,txt

    `pip install -r requirements.txt`

3. After installing the packages, you need to register your virtual environment as a 

    Jupyter kernel:

    >    `python -m ipykernel install --user --name=your_env_name`

    Replace "your_env_name" with a descriptive name for your environment

4. Creating the audio recorder component (for python) or we can use the android 
recorder API to do so aswell (simply records audio in .mp3 format)

5. Created the transcripter using the Whisper-small model(~1GB space)

6. Creating the Transcripter_API.

7. Install Ollama https://ollama.com/download

    7.1 Install 2 Ollama Models 

    - `ollama pull hf.co/mradermacher/Qwen2.5-0.5B-Instruct-GGUF:Q8_0`

    - `ollama run qwen2.5:0.5b`

8. Requirements to Generate Audio ReCap using kokoro model.
    - `sudo apt-get install espeak-ng -y`
    - For Windows and Mac installation:
        - https://github.com/hexgrad/kokoro?tab=readme-ov-file#advanced-usage

 -->

<!-- New -->
# Adhyayan Mitra

Adhyayan Mitra is an AI-powered learning companion that combines real-time audio transcription, document analysis, and adaptive question generation to help students self-assess, identify gaps, and reinforce understanding through personalized study materials.

## 🚀 Features
- Real-time audio recording & Whisper-based transcription  
- Document ingestion pipeline (PDF, DOCX, Markdown)  
- AI-driven question generation & answer evaluation  
- Knowledge-gap analysis with interactive feedback  
- Personalized revision tools: summaries, vocab lists, practice exercises  
- Multi-LLM support: Google GenAI, NVIDIA AI, Ollama, Llama.cpp  

## 💻 Prerequisites
- Python 3.8+  
- git  
- System packages (Linux/macOS):  
  ```bash
  sudo apt-get update
  sudo apt-get install -y python3-venv espeak-ng
  ```
- Windows/macOS audio dependencies: see Kokoro docs → https://github.com/hexgrad/kokoro  

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/pro402/Adhyayan_mitra.git
cd ADHYAYAN_MITRA
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows
```

### 3. Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Register Jupyter kernel (optional)
```bash
python -m ipykernel install --user --name=adhyayan_mitra
```

### 5. Download and prepare LLM models

#### a. Hugging Face GGUF (Qwen2.5)
```bash
huggingface-cli download \
  Qwen/Qwen2.5-0.5B-Instruct-GGUF \
  qwen2.5-0.5b-instruct-q8_0.gguf \
  --local-dir . \
  --local-dir-use-symlinks False
```

#### b. Ollama models (optional)
```
ollama run hf.co/mradermacher/Qwen2.5-0.5B-Instruct-GGUF:Q8_0
```

## 📁 Project Structure
```
ADHYAYAN_MITRA/
├── components/               # Core functionality modules
│   ├── audio_gen/            # Text-to-speech generation
│   ├── audio_recorder/       # Audio recording utilities
│   ├── doc_pipeline/         # Document processing pipeline
│   ├── gap_analyzer/         # Knowledge gap identification
│   ├── qna_judge/            # Answer evaluation system
│   ├── question_generator/   # AI question generation
│   ├── revision_tools/       # Study aids generation
│   ├── select_llm/           # LLM provider integrations
│   ├── sTT_model/            # Speech-to-text models
│   ├── transcripter_api/     # Transcription API
│   └── transcript_gen/       # Transcript generation
├── Idea/                     # Project concept documents
├── static/                   # Static assets
│   └── audio/                # Audio file storage
├── testing/                  # Development and testing files
│   ├── audio_chunks/         # Audio segment storage
│   ├── Docs/                 # Test documents
│   └── *.ipynb               # Test notebooks
├── usage/                    # Usage examples
│   ├── Docs/                 # Sample documents
│   └── *.ipynb               # Example notebooks
├── user_interface/           # Streamlit web interface
│   ├── Home.py               # Main dashboard
│   └── pages/                # Feature-specific pages
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

## 🚀 Launching the UI
```bash
cd user_interface
streamlit run Home.py
```
The web interface lets you record/upload audio, transcribe, select AI models, upload study materials, and navigate through gap analysis, Q&A, and learning-material pages.
### 🎬 Demo

[![Watch the video]](.videos/demo.mp4)

## 📖 Usage Examples

Check the notebooks inside the `testing/` directory for detailed examples:

```bash
jupyter notebook testing/beta_notebook.ipynb
```

Other useful notebooks to explore:
- `testing/HFLangchain.ipynb` - Examples of using Hugging Face models with Langchain
- `testing/kokoro.ipynb` - Audio generation examples
- `testing/notebook.ipynb` - General usage patterns

These notebooks demonstrate:
- **Audio recording & transcription**
- **Document processing**
- **Question generation & evaluation**
- **Gap analysis workflows**

Thank you for exploring Adhyayan Mitra-your feedback and contributions are welcome!  
