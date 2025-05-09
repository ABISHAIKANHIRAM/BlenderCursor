# 🖱️ BlenderCursor – Talk to Blender with Natural Language

BlenderCursor is a desktop app that turns plain English into Blender scripts using AI. Just say or type commands like **"Create a mountain with trees and a sun"**, and the app translates it into Python code and executes it via Blender’s API.

Whether you're a beginner or a pro, BlenderCursor helps you build 3D scenes faster—with zero coding required.

---

## 🚀 Features

- 🧠 **LLM-Powered Prompt Parser**  
  Uses models like GPT-4, Mistral, or WizardCoder to interpret natural language.

- 🛠 **Script Generator**  
  Converts prompts into valid `bpy` Python code (Blender’s scripting language).

- 🖥️ **Cross-Platform Desktop App**  
  Built with Electron, Tauri, or PyQt.

- 🔁 **Live Feedback**  
  Shows Blender logs, preview renders, or exports `.blend` files directly.

- 🎙️ **Voice Input (Optional)**  
  Hands-free scene creation using Whisper or Vosk.

---

## 🧪 Variants & Future Plans

- **MVP**: Text → Script, editable before execution  
- **Prompt-to-Scene**: Auto-generate terrain, lighting, and objects  
- **Image-to-3D (Advanced)**: Use depth estimation (MiDaS, DPT, Luma AI)  
- **Voice-Driven Workflow**: Full hands-free 3D prototyping

---

## 💡 Why BlenderCursor?

Blender is powerful but hard to learn. BlenderCursor makes 3D modeling more accessible, creative, and fun. Ideal for:
- Artists
- Educators
- Hackers and tinkerers
- Anyone scared of `bpy` 😄

---

## 🛠 Tech Stack

| Component      | Tech Used                          |
|----------------|------------------------------------|
| Frontend       | Electron / Tauri / PyQt            |
| AI Model       | GPT-4, Mistral, Dolphin, Ollama     |
| Backend        | Python, Blender `bpy` API          |
| Voice Input    | Whisper / Vosk                     |
| Automation     | Blender subprocess / MCP server    |

---

## 🧩 Example Prompt → Code

Prompt:
> “Add a mountain terrain”

Generated Python:
```python
import bpy

bpy.ops.mesh.primitive_plane_add(size=10)
bpy.ops.object.modifier_add(type='DISPLACE')
bpy.ops.texture.new()
