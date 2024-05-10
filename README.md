# LangChain RAG Sample App

**日本語の解説は[こちら](#日本語の解説)にあります。**

This project provides a sample application implementing Retrieval-Augmented Generation (RAG) using LangChain and OpenAI's GPT models. While it can work with various types of documents, this sample is designed for testing purposes with information from the Kysely TypeScript query builder.

There are many articles about RAG, but most provide only superficial information, making it challenging to get a functional solution up and running. To address this, this repository provides a ready-to-use code sample.

## Features

- **Document Loading:** Supports Markdown, HTML, JSON, and CSV files.
- **Vector Store Indexing:** Utilizes FAISS for efficient document retrieval.
- **Language Models:** Integrates OpenAI's GPT-3.5 and GPT-4 models.
- **Prompt Management:** Custom prompt template for comprehensive answers.
- **Streamlit UI:** Interactive web application for QA.

## Requirements

- Python 3.8 or higher
- `pip` (Python package installer)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/langchain-rag-sample-app.git
cd langchain-rag-sample-app
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install nltk
pip install python-dotenv
pip install langchain
pip install langchain_openai
pip install jq
pip install markdown
pip install unstructured
pip install -U langchain-openai
pip install faiss-cpu
pip install langchainhub
pip install streamlit
```

### 4. Environment Variables Setup

Create a `.env` file in the project root and add your OpenAI and LangChain API keys:

```bash
touch .env
```

Inside `.env`, add:

```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
```

### 5. Prepare Document Directory

Since this repository doesn't include the Kysely documentation or any other documents, you must obtain the desired documents yourself. Create a directory named `kysely` (or any other name), populate it with your documents, and update the `documents` variable path in the `process_documents.py` file.

## Usage

### 1. Run Document Processing Script

```bash
python process_documents.py
```

This script will:

1. Load documents from the directory you specified.
2. Split documents into manageable chunks.
3. Create or load a FAISS vector store for document retrieval.

### 2. Start the Streamlit QA App

```bash
streamlit run webapp.py
```

### 3. Use the Application

- **Ask Questions:** Use the text input to ask questions about your chosen documents.
- **Select LLM Model:** Choose between `gpt-3.5-turbo` and `gpt-4-turbo`.
- **Custom OpenAI Key:** Override the default API key for testing purposes.

## Detailed Code Explanation

### `process_documents.py`

This script handles the document processing and vector store indexing.

- **Environment Setup:** Loads OpenAI and LangChain API keys from the `.env` file.
- **Document Loaders:** Supports different file types via LangChain's loaders:
  - `UnstructuredMarkdownLoader`
  - `UnstructuredHTMLLoader`
  - `JSONLoader`
  - `CSVLoader`
- **Text Splitter:** Splits documents into chunks using `RecursiveCharacterTextSplitter`.
- **FAISS Vector Store:** Creates or loads a FAISS index for efficient retrieval.
- **Prompt Loading:** Retrieves a prompt template from the LangChain Hub.
- **RAG Chain:** Creates a Retrieval-Augmented Generation (RAG) chain combining retriever, prompt, and language model.

### `webapp.py`

This is the Streamlit-based web application for asking questions and generating answers.

- **FAISS Vector Store Loader:** Loads the vector store for document retrieval.
- **LLM Model Setup:** Configures the OpenAI GPT model using `ChatOpenAI`.
- **Custom Prompt Template:** Provides comprehensive answers with source citations.
- **Streamlit UI:**
  - **Question Input:** Text input to ask questions.
  - **Model Selection:** Dropdown for choosing the GPT model.
  - **Answer Generation:** Button to generate answers.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License.

---

## 日本語の解説

このプロジェクトでは、LangChainとOpenAIのGPTモデルを使ったRetrieval-Augmented Generation（RAG）を実装するサンプルアプリケーションを提供しています。さまざまな種類のドキュメントに対応できますが、このサンプルはKysely TypeScriptのクエリビルダーに関する情報を用いて実験のために設計されています。

RAGに関する記事は多くありますが、そのほとんどは表面的な情報だけで、機能するソリューションを実際に作成するには苦労します。それを解決するため、このリポジトリではすぐに使えるサンプルコードを提供します。

## 特徴

- **ドキュメント読み込み:** Markdown、HTML、JSON、およびCSVファイルをサポートしています。
- **ベクトルストアインデックス:** FAISSを利用し、効率的なドキュメント検索が可能です。
- **言語モデル:** OpenAIのGPT-3.5とGPT-4モデルを統合します。
- **プロンプト管理:** 包括的な回答を提供するカスタムプロンプトテンプレート。
- **Streamlit UI:** インタラクティブなQAのウェブアプリケーション。

## 必要条件

- Python 3.8以上
- `pip`（Pythonパッケージインストーラー）

## インストール

### 1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/langchain-rag-sample-app.git
cd langchain-rag-sample-app
```

### 2. 仮想環境を作成し、アクティブ化

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合：venv\Scripts\activate
```

### 3. 依存関係をインストール

```bash
pip install nltk
pip install python-dotenv
pip install langchain
pip install langchain_openai
pip install jq
pip install markdown
pip install unstructured
pip install -U langchain-openai
pip install faiss-cpu
pip install langchainhub
pip install streamlit
```

### 4. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、OpenAIとLangChainのAPIキーを追加します。

```bash
touch .env
```

`.env`の中には次のように書いてください：

```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
```

### 5. ドキュメントディレクトリの準備

このリポジトリにはKyselyのドキュメントや他のドキュメントは含まれていないため、自分で取得してください。 `kysely` という名前のディレクトリ（または他の名前でも可）を作成し、ドキュメントを配置し、 `process_documents.py` ファイル内の `documents` 変数のパスを更新してください。

## 使用方法

### 1. ドキュメント処理スクリプトの実行

```bash
python process_documents.py
```

このスクリプトは次のことを行います：

1. 指定したディレクトリからドキュメントを読み込む。
2. ドキュメントを扱いやすいサイズに分割する。
3. ドキュメント検索のためのFAISSベクトルストアを作成または読み込む。

### 2. Streamlit QAアプリを開始

```bash
streamlit run webapp.py
```

### 3. アプリを使う

- **質問:** テキスト入力でドキュメントに関する質問を行います。
- **LLMモデルの選択:** `gpt-3.5-turbo` と `gpt-4-turbo` から選べます。
- **カスタムOpenAIキー:** テスト用にデフォルトAPIキーを上書きできます。

## 詳細なコードの説明

### `process_documents.py`

このスクリプトはドキュメント処理とベクトルストアのインデックス作成を担当しています。

- **環境設定:** `.env`ファイルからOpenAIとLangChainのAPIキーを読み込みます。
- **ドキュメントローダー:** LangChainのローダーでさまざまなファイル形式に対応：
  - `UnstructuredMarkdownLoader`
  - `UnstructuredHTMLLoader`
  - `JSONLoader`
  - `CSV

Loader`
- **テキスト分割:** `RecursiveCharacterTextSplitter`を使ってドキュメントを分割します。
- **FAISSベクトルストア:** 効率的な検索のためにFAISSインデックスを作成または読み込みます。
- **プロンプトの読み込み:** LangChain Hubからプロンプトテンプレートを取得します。
- **RAGチェーン:** リトリーバー、プロンプト、言語モデルを組み合わせたRAGチェーンを作成します。

### `webapp.py`

これは質問を行い、回答を生成するためのStreamlitベースのウェブアプリケーションです。

- **FAISSベクトルストアローダー:** ドキュメント検索用のベクトルストアを読み込みます。
- **LLMモデルの設定:** `ChatOpenAI`を使ってOpenAI GPTモデルを構成します。
- **カスタムプロンプトテンプレート:** ソースの引用を含む包括的な回答を提供します。
- **Streamlit UI:**
  - **質問入力:** 質問を行うためのテキスト入力。
  - **モデルの選択:** GPTモデルを選択するためのドロップダウン。
  - **回答生成:** 回答を生成するためのボタン。

## 貢献

貢献は歓迎されます！プルリクエストを提出するか、アイデアを議論するために問題を提起してください。

## ライセンス

このプロジェクトはMITライセンスで提供されています。
