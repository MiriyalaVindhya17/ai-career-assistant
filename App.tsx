import {
  useState
} from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import QuickActions from "./components/QuickActions";
import UploadPanel from "./components/UploadPanel";

import {
  sendChatMessage,
  uploadDocument
} from "./services/api";

import type {
  Message
} from "./types";

import "./App.css";


function App() {

  const [
    messages,
    setMessages
  ] = useState<Message[]>([

    {
      id: 1,

      role: "assistant",

      content:
        `## 👋 Welcome to CareerAI

I'm your **AI Career & Interview Assistant**.

I can help you with:

- 📄 Resume analysis
- 💼 Career recommendations
- 🎯 Skill-gap analysis
- 🗺️ Personalized career roadmaps
- 🎤 Mock interviews
- 📚 Document analysis
- 💬 Career questions

**What would you like to work on today?**`,

      timestamp: new Date()
    }

  ]);


  const [
    input,
    setInput
  ] = useState("");


  const [
    loading,
    setLoading
  ] = useState(false);


  const [
    uploading,
    setUploading
  ] = useState(false);


  const [
    uploadOpen,
    setUploadOpen
  ] = useState(false);


  const [
    uploadedFile,
    setUploadedFile
  ] = useState("");


  async function sendMessage(
    customMessage?: string
  ) {

    const text =
      customMessage ||
      input.trim();


    if (
      !text ||
      loading
    ) {
      return;
    }


    const userMessage: Message = {

      id:
        Date.now(),

      role:
        "user",

      content:
        text,

      timestamp:
        new Date()

    };


    setMessages(
      previous => [
        ...previous,
        userMessage
      ]
    );


    setInput("");

    setLoading(true);


    try {

      const data =
        await sendChatMessage(
          text
        );


      const assistantMessage:
        Message = {

        id:
          Date.now() + 1,

        role:
          "assistant",

        content:
          data.response,

        timestamp:
          new Date()

      };


      setMessages(
        previous => [
          ...previous,
          assistantMessage
        ]
      );


    } catch (error) {

      console.error(
        error
      );


      setMessages(
        previous => [

          ...previous,

          {

            id:
              Date.now() + 1,

            role:
              "assistant",

            content:
              `⚠️ **Backend connection failed.**

Please make sure your FastAPI server is running:

\`python -m uvicorn app.main:app --reload\`

Then try again.`,

            timestamp:
              new Date()

          }

        ]
      );

    } finally {

      setLoading(false);

    }

  }


  function handleNewChat() {

    setMessages([

      {

        id:
          Date.now(),

        role:
          "assistant",

        content:
          `## 👋 New Conversation

How can I help with your career today?`,

        timestamp:
          new Date()

      }

    ]);

    setInput("");

  }


  function handleSidebarAction(
    action: string
  ) {

    const prompts: Record<
      string,
      string
    > = {

      chat:
        "Hello CareerAI",

      resume:
        "Analyze my resume",

      career:
        "Recommend career roles for me",

      skills:
        "Analyze my skill gaps",

      interview:
        "Start a mock interview",

      documents:
        "Help me analyze a document"

    };


    if (
      action === "resume" ||
      action === "documents"
    ) {

      setUploadOpen(true);

      return;

    }


    const prompt =
      prompts[action];


    if (prompt) {
      sendMessage(prompt);
    }

  }


  async function handleFileUpload(
    file: File
  ) {

    setUploadedFile(
      file.name
    );

    setUploading(true);


    try {

      const data =
        await uploadDocument(
          file
        );


      setUploadOpen(false);


      const preview =
        data.pages?.[0]?.text
          ?.slice(0, 800) ||
        "";


      setMessages(
        previous => [

          ...previous,

          {

            id:
              Date.now(),

            role:
              "assistant",

            content:
              `## 📄 Document Uploaded

**File:** ${file.name}

The document has been processed successfully.

**Extracted characters:** ${data.characters ?? "N/A"}

${preview
  ? `### Preview\n\n${preview}`
  : ""
}

You can now ask questions about this document.`,

            timestamp:
              new Date()

          }

        ]
      );


    } catch {

      setMessages(
        previous => [

          ...previous,

          {

            id:
              Date.now(),

            role:
              "assistant",

            content:
              `⚠️ I couldn't process **${file.name}**.

Please check that the backend is running and that the file is a PDF or DOCX under 10MB.`,

            timestamp:
              new Date()

          }

        ]
      );

    } finally {

      setUploading(false);

    }

  }


  return (

    <div className="app">

      <Sidebar
        onNewChat={
          handleNewChat
        }
        onAction={
          handleSidebarAction
        }
      />


      <main className="main">

        <Header
          onNewChat={
            handleNewChat
          }
        />


        <section className="chat-area">

          <div className="messages-container">

            {messages.map(
              message => (

                <ChatMessage
                  key={
                    message.id
                  }
                  message={
                    message
                  }
                />

              )
            )}


            {loading && (

              <div className="typing">

                <div className="typing-avatar">
                  🤖
                </div>

                <div className="typing-dots">

                  <span />
                  <span />
                  <span />

                </div>

                CareerAI is thinking...

              </div>

            )}

          </div>

        </section>


        {uploadOpen && (

          <UploadPanel
            fileName={
              uploadedFile
            }
            uploading={
              uploading
            }
            onFileSelect={
              handleFileUpload
            }
            onClose={() =>
              setUploadOpen(false)
            }
          />

        )}


        <QuickActions
          onAction={
            sendMessage
          }
        />


        <ChatInput
          value={
            input
          }
          loading={
            loading
          }
          onChange={
            setInput
          }
          onSend={
            () =>
              sendMessage()
          }
          onFileSelect={
            handleFileUpload
          }
        />

      </main>

    </div>

  );
}


export default App;
