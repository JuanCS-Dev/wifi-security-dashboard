#!/usr/bin/env python3
"""
Teste mínimo py_cui para debug.
Verifica se widgets aparecem corretamente.
"""
import py_cui

# Create small grid
root = py_cui.PyCUI(10, 10)
root.set_title('Teste Minimal py_cui')

# Add text block (has set_text method!)
text_block = root.add_text_block(
    'Test TextBlock',
    row=2,
    column=2,
    row_span=3,
    column_span=5
)
text_block.set_text('Hello from py_cui!\nLine 2\nLine 3')

# Add another label at different position
label2 = root.add_label('Simple Label', row=6, column=2)

print("Widget 1 (TextBlock):", text_block)
print("Widget 2 (Label):", label2)
print("Total widgets:", len(root.get_widgets()))

# Start
root.start()
