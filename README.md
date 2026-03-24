# ComfyUI Conditional Prompt Append

A custom node for ComfyUI that provides advanced, condition-based prompt appending. It allows you to dynamically build prompts based on the presence or absence of specific tags.

## Features
* **Conditional Appending (Core Feature):** Choose exactly when to append your new prompts:
  * `Always`: Appends the prompt regardless of search results.
  * `If Detected`: Appends *only* if the search prompt is found in the base prompt.
  * `If Not Detected`: Appends *only* if the search prompt is missing from the base prompt.
* **Additional Search Logic:** Supports `AND` / `OR` logic when searching for multiple tags.
* **Weight Management:** Automatically groups the appended tags and applies a single weight bracket around them (e.g., `(tag1, tag2:1.2)`).
* **Duplicate Prevention:** Includes a `skip_duplicate` option to prevent adding tags that already exist in the base prompt.
* **Flexible Delimiters:** Fully supports multiline text inputs and custom delimiters (e.g., parsing line breaks into commas automatically).
* **Position Control:** Choose to append new prompts to the `front` or `back` of the base prompt.

## Installation
1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/```
2. Clone this repository:
   ```
   git clone https://github.com/COkedat/comfyui-prompt-append```
3. Restart ComfyUI.
4. You can find the node under the utils/prompt category, named Conditional Prompt Append.

## How to Use
* **base_prompt: Your main prompt text.

* **search_prompt: The tags you want to look for in the base_prompt.

* **append_prompt: The tags you want to add conditionally.

* **prompt (Output): Result prompt text

* **is_detected (Output): Outputs a BOOLEAN (True/False) value indicating if the search prompt was found, which can be routed to other logical nodes.