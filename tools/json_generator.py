"""Generate structured JSON requests for repository updates.

This module defines the expected output contract for automated content
generation. Future integrations should request ONLY JSON matching the
repository schema.
"""

SYSTEM_PROMPT = '''
Return only valid JSON.

Schema:
{
  "files":[
    {
      "path":"relative/path",
      "content":"file contents"
    }
  ]
}
'''

def build_prompt(commit_id:str, task:str)->str:
    return f"{SYSTEM_PROMPT}\n\nCommit: {commit_id}\nTask: {task}"
