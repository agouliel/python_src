# sed -n '20p' dotfiles.txt | hexdump -C
# sed -n '20p': `-n` suppresses default output; `20p` prints only line 20.
# hexdump -C: pipes that line's raw bytes into `hexdump`, `-C` ("canonical") shows each row as: offset, 16 bytes in hex, then their ASCII representation (non-printable bytes shown as `.`).
# This let us see the actual byte sequences (`c2 a0` = UTF-8 for NBSP, `e2 86 92` = UTF-8 for arrow) instead of relying on how a terminal might render them.

with open('file.txt', encoding='utf-8') as f:
    content = f.read()
content = content.replace('\u00a0', '`')   # NBSP -> backtick
content = content.replace('\u2192', '->')  # arrow -> plain ASCII
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write(content)
