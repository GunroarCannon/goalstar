import sys

with open('goalstar-recall/js/dreamers/groq.js', 'r', encoding='utf-8') as f:
    content = f.read()

default_key_decl = "const DEFAULT_GROQ_KEY = process.env.GROQ_API_KEY || '';\n\n"
if "DEFAULT_GROQ_KEY" not in content:
    content = content.replace("export default {", default_key_decl + "export default {")

content = content.replace(
    "if (!p.apiKey) throw new Error('No Groq API key (Settings → Dreamer)');",
    "const apiKey = p.apiKey || DEFAULT_GROQ_KEY;\n    if (!apiKey) throw new Error('No Groq API key configured');"
)
content = content.replace(
    "Authorization: `Bearer ${p.apiKey}`",
    "Authorization: `Bearer ${apiKey}`"
)

with open('goalstar-recall/js/dreamers/groq.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("groq.js patched successfully!")

# Now patch js/model.js
with open('goalstar-recall/js/model.js', 'r', encoding='utf-8') as f:
    model_content = f.read()

model_content = model_content.replace(
    "groq: { apiKey: '', model: 'openai/gpt-oss-120b' }",
    "groq: { apiKey: '', model: 'openai/gpt-oss-120b' }"
)

with open('goalstar-recall/js/model.js', 'w', encoding='utf-8') as f:
    f.write(model_content)

print("model.js patched successfully!")
