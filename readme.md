# 🖱️ BlenderCursor – Talk to Blender with Natural Language

BlenderCursor is a desktop app that turns plain English into Blender scripts using AI. Just say or type commands like **"Create a mountain with trees and a sun"**, and the app translates it into Python code and executes it via Blender’s API.

> ⚠️ **Project Status**: Work in progress. Development has just started and it will take time to complete the core features. Stay tuned for updates as we build!

---

## 🚀 Features (Planned)

- 🧠 **Prompt-to-Script Engine**  
  Interpret natural language and convert it into Blender Python code.

- 🛠 **Script Generator**  
  Automatically generates `bpy` commands based on scene descriptions.

- 🖥️ **Cross-Platform Desktop App**  
  Intuitive UI using Electron, Tauri, or PyQt.

- 🔁 **Live Feedback (Planned)**  
  Show Blender logs, rendered previews, or exported `.blend` files.

- 🎙️ **Voice Input (Optional, Planned)**  
  Hands-free 3D scene creation through speech.

---

## 🧪 Variants & Future Plans

- **MVP**: Text → Script (editable before execution)  
- **Prompt-to-Scene**: Auto-generate terrain, lighting, and objects  
- **Image-to-3D (Advanced)**: Use depth estimation and mesh reconstruction  
- **Voice Control**: Full hands-free 3D prototyping

---

## 💡 Why BlenderCursor?

Blender is powerful but has a steep learning curve. BlenderCursor lowers that barrier, making it easier and more intuitive to create 3D content—perfect for:

- Artists  
- Educators  
- Beginners  
- Rapid prototyping

---

## 🛠 Tech Stack (TBD)

| Component      | Tech Used (Subject to Change)      |
|----------------|------------------------------------|
| Frontend       | Cross-platform desktop frameworks  |
| LLM Integration| To be announced                    |
| Backend        | Blender `bpy` API                  |
| Voice Input    | Optional                           |
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
